from flask import Flask, render_template, request
import pandas as pd
import requests
import os

app = Flask(__name__)

# Path to your historical dataset
DATA_PATH = r"e:\stock\data.csv"
OLLAMA_URL = "http://localhost:11434/api/generate"

def query_llama(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    return response.json()['response']

def get_historical_features(df):
    features = {}
    features['mean_open'] = df['Open'].mean()
    features['mean_close'] = df['Close'].mean()
    features['mean_volume'] = df['Volume'].mean()
    features['std_volume'] = df['Volume'].std()
    features['ma_5'] = df['Close'].rolling(window=5).mean().iloc[-1] if len(df) >= 5 else df['Close'].mean()
    features['ma_10'] = df['Close'].rolling(window=10).mean().iloc[-1] if len(df) >= 10 else df['Close'].mean()
    return features

def parse_float(val):
    try:
        return float(str(val).replace(',', '').replace('\t', '').strip())
    except Exception:
        return 0.0

# Load news headlines from newsdata.csv
NEWS_PATH = r"e:\stock\newsdata.csv"

def get_news_headlines(news_path, max_headlines=5):
    try:
        news_df = pd.read_csv(news_path)
        # Assume the headlines are in a column named 'headline' or similar
        if 'headline' in news_df.columns:
            headlines = news_df['headline'].dropna().astype(str).tolist()
        else:
            # If the column name is different, use the first column
            headlines = news_df.iloc[:, 0].dropna().astype(str).tolist()
        # Limit to the most recent N headlines
        return "\n".join(headlines[:max_headlines])
    except Exception as e:
        return "No news headlines available."

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Get uploaded file or form data
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            current_df = pd.read_csv(file)
            current_data = current_df.head(1).to_dict(orient='records')[0]
        else:
            # Get data from form fields
            current_data = {
                "Date": request.form.get("date"),
                "Open": parse_float(request.form.get("open", 0)),
                "High": parse_float(request.form.get("high", 0)),
                "Low": parse_float(request.form.get("low", 0)),
                "Close": parse_float(request.form.get("close", 0)),
                "Volume": parse_float(request.form.get("volume", 0))
            }

        # Summarize historical data and extract features
        df = pd.read_csv(DATA_PATH)
        features = get_historical_features(df)
        summary = (
            f"Mean Open: {features['mean_open']:.2f}\n"
            f"Mean Close: {features['mean_close']:.2f}\n"
            f"Mean Volume: {features['mean_volume']:.2f}\n"
            f"Std Volume: {features['std_volume']:.2f}\n"
            f"5-day MA: {features['ma_5']:.2f}\n"
            f"10-day MA: {features['ma_10']:.2f}\n"
        )

        # Calculate differences and percentage changes
        mean_close = features['mean_close']
        mean_open = features['mean_open']
        mean_volume = features['mean_volume']
        ma_5 = features['ma_5']
        ma_10 = features['ma_10']

        current_close = float(current_data['Close'])
        current_open = float(current_data['Open'])
        current_volume = float(current_data['Volume'])

        close_diff = current_close - mean_close
        open_diff = current_open - mean_open
        volume_pct = (current_volume / mean_volume) * 100 if mean_volume else 0

        # Build analysis string
        analysis = (
            f"Mean Close: {mean_close:.2f}\n"
            f"Current Close: {current_close:.2f}\n"
            f"Difference: {close_diff:.2f}\n\n"
            f"Mean Open: {mean_open:.2f}\n"
            f"Current Open: {current_open:.2f}\n"
            f"Difference: {open_diff:.2f}\n\n"
            f"Mean Volume: {mean_volume:.2f}\n"
            f"Current Volume: {current_volume:.2f}\n"
            f"Percentage Change: {volume_pct:.2f}%\n\n"
            f"5-day MA: {ma_5:.2f}\n"
            f"10-day MA: {ma_10:.2f}\n"
        )

        # Compose prompt
        manual_news = request.form.get("manual_news", "").strip()
        if manual_news:
            news_headlines = manual_news
        else:
            news_headlines = get_news_headlines(NEWS_PATH)

        prompt = (
            f"Historical stock features from 2015-2023:\n{summary}\n"
            f"Current company data:\n{current_data}\n"
            f"Recent news headlines:\n{news_headlines}\n\n"
            "Based on the historical data, current data, and recent news, predict the likely trend for the next week and explain your reasoning."
        )

        # Query Llama 3.2
        result = query_llama(prompt)

        # Pass analysis to template
        return render_template('index.html', result=result, analysis=analysis, news_headlines=news_headlines)

    news_headlines = get_news_headlines(NEWS_PATH)
    return render_template('index.html', result=result, news_headlines=news_headlines)

if __name__ == '__main__':
    app.run(debug=True)