#!/usr/bin/env python3
"""
Simple tests for the Amazon Price Tracker.
"""

import os
import json
import tempfile
import shutil
from datetime import datetime
from price_tracker import AmazonPriceTracker


def test_extract_product_id():
    """Test ASIN extraction from various URL formats."""
    tracker = AmazonPriceTracker()
    
    # Test standard dp URL
    asin1 = tracker.extract_product_id('https://www.amazon.com/dp/B08N5WRWNW')
    assert asin1 == 'B08N5WRWNW', f"Expected B08N5WRWNW, got {asin1}"
    
    # Test gp/product URL
    asin2 = tracker.extract_product_id('https://www.amazon.com/gp/product/B08N5WRWNW/ref=ppx_yo')
    assert asin2 == 'B08N5WRWNW', f"Expected B08N5WRWNW, got {asin2}"
    
    # Test invalid URL
    asin3 = tracker.extract_product_id('https://www.amazon.com/')
    assert asin3 is None, f"Expected None, got {asin3}"
    
    print("✓ test_extract_product_id passed")


def test_save_and_load_price_data():
    """Test saving and loading price history."""
    # Create temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    
    try:
        tracker = AmazonPriceTracker(data_dir=temp_dir)
        
        # Create test product data
        product_data = {
            'asin': 'B08N5TEST',
            'title': 'Test Product',
            'price': 99.99,
            'currency': 'USD',
            'timestamp': datetime.now().isoformat(),
            'url': 'https://www.amazon.com/dp/B08N5TEST'
        }
        
        # Save data
        tracker.save_price_data(product_data)
        
        # Load data
        history = tracker.get_price_history('B08N5TEST')
        
        assert history is not None, "History should not be None"
        assert history['asin'] == 'B08N5TEST', f"Expected B08N5TEST, got {history['asin']}"
        assert history['title'] == 'Test Product', f"Expected Test Product, got {history['title']}"
        assert len(history['price_history']) == 1, f"Expected 1 price point, got {len(history['price_history'])}"
        assert history['price_history'][0]['price'] == 99.99, f"Expected 99.99, got {history['price_history'][0]['price']}"
        
        print("✓ test_save_and_load_price_data passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def test_analyze_trends():
    """Test price trend analysis."""
    # Create temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    
    try:
        tracker = AmazonPriceTracker(data_dir=temp_dir)
        
        # Create test data with multiple price points
        asin = 'B08N5TREND'
        filepath = os.path.join(temp_dir, f"{asin}.json")
        
        test_history = {
            'asin': asin,
            'title': 'Trending Test Product',
            'url': 'https://www.amazon.com/dp/B08N5TREND',
            'price_history': [
                {'price': 100.0, 'timestamp': '2024-01-01T00:00:00', 'currency': 'USD'},
                {'price': 95.0, 'timestamp': '2024-01-02T00:00:00', 'currency': 'USD'},
                {'price': 90.0, 'timestamp': '2024-01-03T00:00:00', 'currency': 'USD'},
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(test_history, f)
        
        # Analyze trends
        analysis = tracker.analyze_trends(asin)
        
        assert analysis is not None, "Analysis should not be None"
        assert analysis['current_price'] == 90.0, f"Expected 90.0, got {analysis['current_price']}"
        assert analysis['min_price'] == 90.0, f"Expected 90.0, got {analysis['min_price']}"
        assert analysis['max_price'] == 100.0, f"Expected 100.0, got {analysis['max_price']}"
        assert analysis['avg_price'] == 95.0, f"Expected 95.0, got {analysis['avg_price']}"
        assert analysis['trend'] == 'decreasing', f"Expected decreasing, got {analysis['trend']}"
        assert analysis['num_data_points'] == 3, f"Expected 3, got {analysis['num_data_points']}"
        
        print("✓ test_analyze_trends passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def test_list_tracked_products():
    """Test listing tracked products."""
    # Create temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    
    try:
        tracker = AmazonPriceTracker(data_dir=temp_dir)
        
        # Initially should be empty
        products = tracker.list_tracked_products()
        assert len(products) == 0, f"Expected 0 products, got {len(products)}"
        
        # Add some test products
        for i in range(3):
            product_data = {
                'asin': f'B08N5TEST{i}',
                'title': f'Test Product {i}',
                'price': 99.99,
                'currency': 'USD',
                'timestamp': datetime.now().isoformat(),
                'url': f'https://www.amazon.com/dp/B08N5TEST{i}'
            }
            tracker.save_price_data(product_data)
        
        # Should now have 3 products
        products = tracker.list_tracked_products()
        assert len(products) == 3, f"Expected 3 products, got {len(products)}"
        
        print("✓ test_list_tracked_products passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def test_get_insights():
    """Test insights generation."""
    # Create temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    
    try:
        tracker = AmazonPriceTracker(data_dir=temp_dir)
        
        # Create test data
        asin = 'B08N5INSGT'
        filepath = os.path.join(temp_dir, f"{asin}.json")
        
        test_history = {
            'asin': asin,
            'title': 'Insight Test Product',
            'url': 'https://www.amazon.com/dp/B08N5INSGT',
            'price_history': [
                {'price': 100.0, 'timestamp': '2024-01-01T00:00:00', 'currency': 'USD'},
                {'price': 90.0, 'timestamp': '2024-01-02T00:00:00', 'currency': 'USD'},
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(test_history, f)
        
        # Get insights
        insights = tracker.get_insights(asin)
        
        assert insights is not None, "Insights should not be None"
        assert 'Insight Test Product' in insights, "Product title should be in insights"
        assert '$90.00' in insights, "Current price should be in insights"
        assert 'DECREASING' in insights, "Trend should be in insights"
        
        print("✓ test_get_insights passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def run_all_tests():
    """Run all tests."""
    print("\nRunning Amazon Price Tracker Tests...")
    print("="*60)
    
    test_extract_product_id()
    test_save_and_load_price_data()
    test_analyze_trends()
    test_list_tracked_products()
    test_get_insights()
    
    print("="*60)
    print("All tests passed! ✓\n")


if __name__ == "__main__":
    run_all_tests()
