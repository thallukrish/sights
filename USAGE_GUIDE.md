# Sights - Usage Guide

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/thallukrish/sights.git
cd sights

# Install dependencies
pip install -r requirements.txt
```

### 2. Track Your First Product

To start tracking an Amazon product, use the `track` command with the product URL:

```bash
python price_tracker.py track https://www.amazon.com/dp/B08N5WRWNW
```

**Output:**
```
Fetching price data for https://www.amazon.com/dp/B08N5WRWNW...
Successfully tracked: Sony Wireless Headphones
Current Price: $89.99
ASIN: B08N5WRWNW
```

### 3. View Insights

After tracking a product for some time, view detailed insights:

```bash
python price_tracker.py insights B08N5WRWNW
```

**Output:**
```
============================================================
Product: Sony Wireless Headphones
ASIN: B08N5WRWNW

Current Price: $89.99
Price Range: $89.99 - $100.00
Average Price: $95.14

Price Trend: DECREASING
Recent Change: $-2.01 (-2.2%)

Buying Recommendation:
  ✓ Current price is at the lowest recorded! Good time to buy.

Data Points: 7
============================================================
```

### 4. List All Tracked Products

```bash
python price_tracker.py list
```

**Output:**
```
Tracking 3 product(s):
  - B08N5WRWNW: Sony Wireless Headphones
  - B09GAMING1: Gaming Console
  - B07KITCHEN: Kitchen Appliance Set
```

## Understanding Price Trends

### Trend Types

1. **DECREASING** 📉
   - Price is going down
   - Usually a good time to buy or wait a bit more

2. **INCREASING** 📈
   - Price is going up
   - May indicate high demand or limited stock
   - Consider buying soon if you need the product

3. **STABLE** ➡️
   - Price stays relatively constant
   - Good for planning purchases

### Buying Recommendations

The tool provides smart recommendations:

- **✓ Good time to buy**: Price at or near historical low
- **⚠ Consider waiting**: Price is significantly above lowest recorded
- **→ Close to lowest**: Price is near the best deal

## Best Practices

### Tracking Frequency
- **Daily tracking**: Best for volatile products or time-sensitive purchases
- **Weekly tracking**: Good for most products
- **Monthly tracking**: Sufficient for stable products

### Building History
Track products for at least:
- **1 week** for quick trends
- **1 month** for reliable insights
- **3+ months** for comprehensive analysis

### What to Track
Ideal products to track:
- Electronics (prices fluctuate frequently)
- Seasonal items (track before peak season)
- High-value purchases (maximize savings)
- Products with price history of drops

## Advanced Usage

### Automating Price Checks

Create a simple script to check all tracked products daily:

```bash
#!/bin/bash
# daily_check.sh

for asin in $(python price_tracker.py list | grep "^  -" | cut -d: -f1 | cut -d- -f2 | xargs); do
    # Re-track to update price
    # Note: You'll need to store URLs or fetch them from history
    echo "Checking $asin..."
done
```

### Setting Up Cron Job (Linux/Mac)

Check prices automatically every day at 9 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 9 * * * cd /path/to/sights && python price_tracker.py track <URL>
```

## Data Management

### Data Location
Price history is stored in `price_history/` directory as JSON files:
- One file per product
- Named by ASIN (e.g., `B08N5WRWNW.json`)
- Contains full price history with timestamps

### Backup Your Data
```bash
# Backup price history
tar -czf price_history_backup.tar.gz price_history/

# Restore from backup
tar -xzf price_history_backup.tar.gz
```

### Export Price History
```python
import json

# Read a product's history
with open('price_history/B08N5WRWNW.json', 'r') as f:
    history = json.load(f)
    
# Convert to CSV
import csv
with open('prices.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Price'])
    for point in history['price_history']:
        writer.writerow([point['timestamp'], point['price']])
```

## Troubleshooting

### "Could not extract product ID from URL"
- Ensure you're using a valid Amazon product URL
- URL should contain `/dp/` or `/gp/product/` followed by 10-character ASIN
- Example: `https://www.amazon.com/dp/B08N5WRWNW`

### "Could not extract price from page"
- Amazon's page structure may have changed
- Product may be out of stock
- Your IP may be rate-limited (wait and try again)

### "Insufficient data for analysis"
- Need at least 2 price points for trend analysis
- Track the product again to add more data points

## Demo Mode

Test the application without tracking real products:

```bash
python example.py
```

This creates sample data and demonstrates all features.

## Tips for Maximum Savings

1. **Track Early**: Start tracking products well before you plan to buy
2. **Check Patterns**: Look for recurring patterns (weekly drops, holiday sales)
3. **Set Expectations**: Use average and min prices to set a target price
4. **Be Patient**: If not urgent, wait for price drops
5. **Compare Trends**: Track similar products to find the best deal

## API Integration (Advanced)

The `AmazonPriceTracker` class can be integrated into your own Python applications:

```python
from price_tracker import AmazonPriceTracker

# Initialize tracker
tracker = AmazonPriceTracker(data_dir="my_data")

# Fetch and save price
product_data = tracker.fetch_price(url)
if product_data:
    tracker.save_price_data(product_data)

# Get analysis
analysis = tracker.analyze_trends(asin)
print(f"Current price: ${analysis['current_price']}")
print(f"Trend: {analysis['trend']}")

# Get human-readable insights
insights = tracker.get_insights(asin)
print(insights)
```

## Support

For issues, feature requests, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Check existing documentation

## Legal Notice

This tool is for personal use only. Always respect:
- Amazon's Terms of Service
- robots.txt guidelines
- Rate limiting (don't make excessive requests)

Price data is fetched from publicly available product pages.
