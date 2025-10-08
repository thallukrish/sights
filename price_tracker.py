#!/usr/bin/env python3
"""
Amazon Price Tracker - Provides insights into price trends of items on Amazon.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class AmazonPriceTracker:
    """Track and analyze Amazon product prices over time."""
    
    def __init__(self, data_dir: str = "price_history"):
        """
        Initialize the price tracker.
        
        Args:
            data_dir: Directory to store price history data
        """
        self.data_dir = data_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        os.makedirs(data_dir, exist_ok=True)
    
    def extract_product_id(self, url: str) -> Optional[str]:
        """
        Extract ASIN (Amazon Standard Identification Number) from URL.
        
        Args:
            url: Amazon product URL
            
        Returns:
            ASIN if found, None otherwise
        """
        # Match patterns like /dp/B08N5WRWNW/ or /gp/product/B08N5WRWNW/
        match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        return None
    
    def fetch_price(self, url: str) -> Optional[Dict]:
        """
        Fetch current price and product details from Amazon.
        
        Args:
            url: Amazon product URL
            
        Returns:
            Dictionary with product details and price, or None if failed
        """
        asin = self.extract_product_id(url)
        if not asin:
            print("Error: Could not extract product ID from URL")
            return None
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product title
            title_elem = soup.find('span', {'id': 'productTitle'})
            title = title_elem.text.strip() if title_elem else "Unknown Product"
            
            # Try to extract price from various possible locations
            price = None
            price_selectors = [
                ('span', {'class': 'a-price-whole'}),
                ('span', {'class': 'a-offscreen'}),
                ('span', {'id': 'priceblock_ourprice'}),
                ('span', {'id': 'priceblock_dealprice'}),
            ]
            
            for tag, attrs in price_selectors:
                price_elem = soup.find(tag, attrs)
                if price_elem:
                    price_text = price_elem.text.strip()
                    # Extract numeric value
                    match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if match:
                        price = float(match.group().replace(',', ''))
                        break
            
            if price is None:
                print("Warning: Could not extract price from page")
                return None
            
            return {
                'asin': asin,
                'title': title,
                'price': price,
                'currency': 'USD',  # Default to USD
                'timestamp': datetime.now().isoformat(),
                'url': url
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product data: {e}")
            return None
    
    def save_price_data(self, product_data: Dict) -> None:
        """
        Save product price data to history.
        
        Args:
            product_data: Dictionary containing product and price information
        """
        asin = product_data['asin']
        filepath = os.path.join(self.data_dir, f"{asin}.json")
        
        # Load existing history or create new
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                history = json.load(f)
        else:
            history = {
                'asin': asin,
                'title': product_data['title'],
                'url': product_data['url'],
                'price_history': []
            }
        
        # Add new price point
        history['price_history'].append({
            'price': product_data['price'],
            'timestamp': product_data['timestamp'],
            'currency': product_data.get('currency', 'USD')
        })
        
        # Save updated history
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"Saved price data for {asin}")
    
    def get_price_history(self, asin: str) -> Optional[Dict]:
        """
        Get price history for a product.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            Dictionary with price history, or None if not found
        """
        filepath = os.path.join(self.data_dir, f"{asin}.json")
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def analyze_trends(self, asin: str) -> Optional[Dict]:
        """
        Analyze price trends for a product.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            Dictionary with trend analysis, or None if insufficient data
        """
        history = self.get_price_history(asin)
        if not history or len(history['price_history']) < 2:
            return None
        
        prices = [p['price'] for p in history['price_history']]
        current_price = prices[-1]
        
        analysis = {
            'asin': asin,
            'title': history['title'],
            'current_price': current_price,
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'num_data_points': len(prices),
        }
        
        # Calculate trend
        if len(prices) >= 2:
            price_change = current_price - prices[-2]
            price_change_pct = (price_change / prices[-2]) * 100
            analysis['price_change'] = price_change
            analysis['price_change_percent'] = price_change_pct
            
            if price_change > 0:
                analysis['trend'] = 'increasing'
            elif price_change < 0:
                analysis['trend'] = 'decreasing'
            else:
                analysis['trend'] = 'stable'
        
        # Calculate savings opportunity
        analysis['potential_savings'] = current_price - analysis['min_price']
        analysis['savings_percent'] = ((current_price - analysis['min_price']) / current_price) * 100 if current_price > 0 else 0
        
        return analysis
    
    def get_insights(self, asin: str) -> str:
        """
        Generate human-readable insights for a product.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            Formatted string with insights
        """
        analysis = self.analyze_trends(asin)
        if not analysis:
            return "Insufficient data for analysis. Track the product for more insights."
        
        insights = []
        insights.append(f"Product: {analysis['title']}")
        insights.append(f"ASIN: {analysis['asin']}")
        insights.append(f"\nCurrent Price: ${analysis['current_price']:.2f}")
        insights.append(f"Price Range: ${analysis['min_price']:.2f} - ${analysis['max_price']:.2f}")
        insights.append(f"Average Price: ${analysis['avg_price']:.2f}")
        
        if 'trend' in analysis:
            insights.append(f"\nPrice Trend: {analysis['trend'].upper()}")
            if analysis['price_change'] != 0:
                change_symbol = "+" if analysis['price_change'] > 0 else ""
                insights.append(f"Recent Change: {change_symbol}${analysis['price_change']:.2f} ({change_symbol}{analysis['price_change_percent']:.1f}%)")
        
        if analysis['potential_savings'] > 0:
            insights.append(f"\nBuying Recommendation:")
            if analysis['current_price'] == analysis['min_price']:
                insights.append("  ✓ Current price is at the lowest recorded! Good time to buy.")
            elif analysis['savings_percent'] > 10:
                insights.append(f"  ⚠ Price is {analysis['savings_percent']:.1f}% above lowest. Consider waiting.")
            else:
                insights.append("  → Price is close to the lowest recorded.")
        
        insights.append(f"\nData Points: {analysis['num_data_points']}")
        
        return "\n".join(insights)
    
    def list_tracked_products(self) -> List[str]:
        """
        List all tracked product ASINs.
        
        Returns:
            List of ASINs
        """
        if not os.path.exists(self.data_dir):
            return []
        
        return [f.replace('.json', '') for f in os.listdir(self.data_dir) 
                if f.endswith('.json')]


def main():
    """Main entry point for the price tracker."""
    import sys
    
    if len(sys.argv) < 2:
        print("Amazon Price Tracker - Get insights into price trends")
        print("\nUsage:")
        print("  python price_tracker.py track <amazon_url>    - Track a product")
        print("  python price_tracker.py insights <asin>       - View insights for a product")
        print("  python price_tracker.py list                  - List all tracked products")
        print("\nExample:")
        print("  python price_tracker.py track https://www.amazon.com/dp/B08N5WRWNW")
        print("  python price_tracker.py insights B08N5WRWNW")
        return
    
    tracker = AmazonPriceTracker()
    command = sys.argv[1].lower()
    
    if command == "track":
        if len(sys.argv) < 3:
            print("Error: Please provide an Amazon product URL")
            return
        
        url = sys.argv[2]
        print(f"Fetching price data for {url}...")
        product_data = tracker.fetch_price(url)
        
        if product_data:
            tracker.save_price_data(product_data)
            print(f"Successfully tracked: {product_data['title']}")
            print(f"Current Price: ${product_data['price']:.2f}")
            print(f"ASIN: {product_data['asin']}")
        else:
            print("Failed to fetch price data")
    
    elif command == "insights":
        if len(sys.argv) < 3:
            print("Error: Please provide a product ASIN")
            return
        
        asin = sys.argv[2]
        insights = tracker.get_insights(asin)
        print("\n" + "="*60)
        print(insights)
        print("="*60)
    
    elif command == "list":
        products = tracker.list_tracked_products()
        if not products:
            print("No products are currently being tracked.")
        else:
            print(f"Tracking {len(products)} product(s):")
            for asin in products:
                history = tracker.get_price_history(asin)
                if history:
                    print(f"  - {asin}: {history['title']}")
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'track', 'insights', or 'list'")


if __name__ == "__main__":
    main()
