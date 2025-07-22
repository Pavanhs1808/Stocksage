# StockSense: AI-Powered Stock & News Trend Analyzer

StockSense is a web application that leverages Llama 3.2 (via Ollama) to analyze stock market data and recent news headlines, providing intelligent predictions and insights for your chosen company. By combining historical price trends with the latest news sentiment, StockSense offers a holistic view of potential stock movements.

## Features

- 📈 **Upload or Enter Stock Data:**  
  Upload a CSV or manually enter Open, High, Low, Close, and Volume for your company.

- 📰 **News Integration:**  
  Paste recent news headlines or automatically load them from a CSV file to include market sentiment in the analysis.

- 🤖 **AI-Powered Predictions:**  
  Uses Llama 3.2 to analyze both numerical data and news, providing a trend prediction and reasoning.

- 📊 **Automated Data Analysis:**  
  See key statistics, moving averages, and volume changes compared to historical data.

- 🌐 **Modern Web UI:**  
  Clean, responsive Bootstrap interface for easy use on desktop and mobile.

## How It Works

1. **Prepare your data:**
   - Place your historical stock data as `data.csv` in the project folder.
   - Place your recent news headlines as `newsdata.csv` (with a `headline` column) in the same folder.

2. **Run the app:**
   ```bash
   pip install flask pandas requests
   # (Optional: pip install yfinance if you want to add live scraping)
   python app.py
   ```

3. **Open your browser:**  
   Go to [http://localhost:5000](http://localhost:5000)

4. **Upload or enter stock data and news:**  
   - Upload a CSV or fill in the form fields.
   - Paste news headlines or let the app load them from `newsdata.csv`.

5. **Get predictions:**  
   - View automated analysis, news context, and the Llama 3.2 prediction with reasoning.

## Example Prompt to Llama 3.2

```
Historical stock features from 2015-2023:
Mean Open: 12405.98
Mean Close: 12396.52
...
Current company data:
{'Date': '2025-07-23', 'Open': 1435.8, ...}
Recent news headlines:
Company achieves record profits
CEO announces new strategy

Based on the historical data, current data, and recent news, predict the likely trend for the next week and explain your reasoning.
```

## Requirements

- Python 3.8+
- Flask
- pandas
- requests
- Ollama running Llama 3.2 locally

## Customization

- **News scraping:**  
  Integrate with a news API or web scraper for live headlines.
- **More analytics:**  
  Add technical indicators or charting with matplotlib or plotly.

## License

MIT License

---

**Disclaimer:**  
This tool is for educational and informational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions.
