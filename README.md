# Sights - Amazon Price Tracker

Get insights into price trends of items on Amazon. Track products, monitor price changes, and make informed buying decisions.

## Features

- 🔍 **Track Products**: Monitor Amazon products by URL
- 📊 **Price History**: Store and analyze historical price data
- 📈 **Trend Analysis**: Identify price trends (increasing, decreasing, stable)
- 💰 **Savings Insights**: Get recommendations on when to buy
- 📋 **Multiple Products**: Track unlimited products simultaneously

## Installation

1. Clone this repository:
```bash
git clone https://github.com/thallukrish/sights.git
cd sights
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Track a Product

Start tracking an Amazon product by providing its URL:

```bash
python price_tracker.py track https://www.amazon.com/dp/B08N5WRWNW
```

The tracker will fetch the current price and save it to the price history.

### View Insights

Get detailed insights about a tracked product using its ASIN:

```bash
python price_tracker.py insights B08N5WRWNW
```

This will display:
- Current price
- Price range (minimum and maximum)
- Average price
- Price trend (increasing/decreasing/stable)
- Recent price changes
- Buying recommendations

### List Tracked Products

See all products you're currently tracking:

```bash
python price_tracker.py list
```

## How It Works

1. **Data Collection**: When you track a product, the tool fetches the current price from Amazon
2. **Storage**: Price data is stored locally in JSON format with timestamps
3. **Analysis**: The tool analyzes price history to identify trends and patterns
4. **Insights**: Based on historical data, it provides recommendations on buying decisions

## Example Output

```
============================================================
Product: Example Wireless Headphones
ASIN: B08N5WRWNW

Current Price: $79.99
Price Range: $69.99 - $89.99
Average Price: $77.49

Price Trend: DECREASING
Recent Change: -$5.00 (-5.9%)

Buying Recommendation:
  → Price is close to the lowest recorded.

Data Points: 5
============================================================
```

## Price History Storage

Price data is stored in the `price_history/` directory as JSON files, one per product (named by ASIN). Each file contains:
- Product information (title, URL, ASIN)
- Complete price history with timestamps
- Currency information

## Tips for Best Results

- Track products regularly (daily or weekly) to build a comprehensive history
- The more data points collected, the more accurate the trend analysis
- Use the insights to identify the best time to purchase

## Privacy & Data

- All data is stored locally on your machine
- No data is sent to third-party services
- Amazon's robots.txt and Terms of Service should be respected

## Limitations

- Requires active internet connection to fetch prices
- Amazon's page structure may change, affecting price extraction
- Rate limiting may apply if checking too many products too quickly
- Some products may have multiple price variations (used, new, etc.)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.