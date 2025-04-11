from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return 'EPS API is running!'

@app.route('/get_eps', methods=['POST'])
def get_eps():
    data = request.json
    tickers = data.get("tickers", [])
    years = data.get("years", [])

    result = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            financials = stock.financials.T
            eps_by_year = {}

            for fecha in financials.index:
                año = fecha.year
                if año in years:
                    eps = financials.loc[fecha].get('Diluted EPS', 'No disponible')
                    if pd.notna(eps):
                        eps_by_year[año] = float(eps)
                    else:
                        eps_by_year[año] = "No disponible"

            result[ticker] = eps_by_year
        except Exception as e:
            result[ticker] = f"Error: {str(e)}"

    return jsonify(result)
