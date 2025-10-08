#!/usr/bin/env python3
"""
Example usage of the Amazon Price Tracker.
This demonstrates the main features without requiring actual Amazon URLs.
"""

from price_tracker import AmazonPriceTracker
from datetime import datetime, timedelta
import json
import os


def create_demo_data():
    """Create sample price history data for demonstration."""
    tracker = AmazonPriceTracker()
    
    # Create demo product data
    demo_asin = "B08N5WRWNW"
    demo_filepath = os.path.join(tracker.data_dir, f"{demo_asin}.json")
    
    # Simulate price history over 7 days
    base_price = 100.0
    demo_history = {
        'asin': demo_asin,
        'title': 'Demo Wireless Headphones - Premium Sound Quality',
        'url': 'https://www.amazon.com/dp/B08N5WRWNW',
        'price_history': []
    }
    
    # Generate historical prices with a downward trend
    prices = [100.0, 98.5, 97.0, 95.0, 93.5, 92.0, 89.99]
    
    for i, price in enumerate(prices):
        timestamp = (datetime.now() - timedelta(days=len(prices)-i-1)).isoformat()
        demo_history['price_history'].append({
            'price': price,
            'timestamp': timestamp,
            'currency': 'USD'
        })
    
    # Save demo data
    with open(demo_filepath, 'w') as f:
        json.dump(demo_history, f, indent=2)
    
    print(f"Created demo data for ASIN: {demo_asin}")
    return demo_asin


def demo_analysis():
    """Demonstrate the analysis features."""
    print("="*70)
    print("Amazon Price Tracker - Demo")
    print("="*70)
    print()
    
    # Create demo data
    demo_asin = create_demo_data()
    
    # Initialize tracker
    tracker = AmazonPriceTracker()
    
    # Show insights
    print("\nGenerating insights for demo product...\n")
    insights = tracker.get_insights(demo_asin)
    print(insights)
    print()
    
    # Show raw analysis
    print("\n" + "="*70)
    print("Detailed Analysis Data:")
    print("="*70)
    analysis = tracker.analyze_trends(demo_asin)
    if analysis:
        print(f"\nASIN: {analysis['asin']}")
        print(f"Title: {analysis['title']}")
        print(f"\nPrice Statistics:")
        print(f"  Current: ${analysis['current_price']:.2f}")
        print(f"  Minimum: ${analysis['min_price']:.2f}")
        print(f"  Maximum: ${analysis['max_price']:.2f}")
        print(f"  Average: ${analysis['avg_price']:.2f}")
        print(f"\nTrend Information:")
        print(f"  Trend: {analysis['trend']}")
        print(f"  Price Change: ${analysis['price_change']:.2f}")
        print(f"  Change Percent: {analysis['price_change_percent']:.1f}%")
        print(f"\nSavings Opportunity:")
        print(f"  Potential Savings: ${analysis['potential_savings']:.2f}")
        print(f"  Savings Percent: {analysis['savings_percent']:.1f}%")
        print(f"\nData Points: {analysis['num_data_points']}")
    
    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nTo track real products, use:")
    print("  python price_tracker.py track <amazon_url>")
    print("\nTo view insights for the demo product:")
    print(f"  python price_tracker.py insights {demo_asin}")


if __name__ == "__main__":
    demo_analysis()
