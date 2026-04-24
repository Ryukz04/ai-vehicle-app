from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# Load vehicle data once when app starts
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vehicles.csv')
df = pd.read_csv(DATA_PATH)


# ── Route 1: Recommend vehicles ──────────────────────────────────────────────
@app.route('/recommend', methods=['GET'])
def recommend():
    """
    Query params:
      vehicle_type  : "car" or "bike"
      fuel_type     : "petrol", "diesel", "hybrid", or "any"
      usage_type    : "city", "highway", "mixed", or "any"
      budget_min    : minimum price in BDT (default 0)
      budget_max    : maximum price in BDT (default 99999999)
      brand         : brand name or "any"
    """
    vehicle_type = request.args.get('vehicle_type', 'any').lower()
    fuel_type    = request.args.get('fuel_type', 'any').lower()
    usage_type   = request.args.get('usage_type', 'any').lower()
    budget_min   = int(request.args.get('budget_min', 0))
    budget_max   = int(request.args.get('budget_max', 99999999))
    brand        = request.args.get('brand', 'any').lower()

    results = df.copy()

    if vehicle_type != 'any':
        results = results[results['type'] == vehicle_type]
    if fuel_type != 'any':
        results = results[results['fuel_type'] == fuel_type]
    if usage_type != 'any':
        results = results[results['usage_type'] == usage_type]
    if brand != 'any':
        results = results[results['brand'].str.lower() == brand]

    results = results[
        (results['price_bdt'] >= budget_min) &
        (results['price_bdt'] <= budget_max)
    ]

    # Simple AI scoring: higher mileage + lower price = better score
    if not results.empty:
        max_price  = results['price_bdt'].max()
        max_mileage = results['mileage_kmpl'].max()
        results = results.copy()
        results['score'] = (
            (results['mileage_kmpl'] / max_mileage) * 0.5 +
            (1 - results['price_bdt'] / max_price) * 0.5
        ).round(2)
        results = results.sort_values('score', ascending=False)

    return jsonify(results.to_dict(orient='records'))


# ── Route 2: Compare vehicles ─────────────────────────────────────────────────
@app.route('/compare', methods=['GET'])
def compare():
    """
    Query param:
      names : comma-separated vehicle names, e.g. "Toyota Corolla 2023,Honda Civic 2023"
    """
    names_param = request.args.get('names', '')
    names = [n.strip() for n in names_param.split(',') if n.strip()]

    if not names:
        return jsonify({'error': 'Provide vehicle names as ?names=Name1,Name2'}), 400

    results = df[df['name'].isin(names)]
    return jsonify(results.to_dict(orient='records'))


# ── Route 3: EMI Calculator ───────────────────────────────────────────────────
@app.route('/emi', methods=['GET'])
def emi():
    """
    Query params:
      price         : total vehicle price in BDT
      down_payment  : amount paid upfront
      interest_rate : annual interest rate in % (e.g. 9.5)
      loan_years    : loan duration in years
    """
    try:
        price         = float(request.args.get('price', 0))
        down_payment  = float(request.args.get('down_payment', 0))
        interest_rate = float(request.args.get('interest_rate', 9.5))
        loan_years    = int(request.args.get('loan_years', 3))
    except ValueError:
        return jsonify({'error': 'Invalid numbers provided'}), 400

    loan_amount   = price - down_payment
    monthly_rate  = (interest_rate / 100) / 12
    n_months      = loan_years * 12

    if monthly_rate == 0:
        monthly_emi = loan_amount / n_months
    else:
        monthly_emi = loan_amount * monthly_rate * (1 + monthly_rate) ** n_months / \
                      ((1 + monthly_rate) ** n_months - 1)

    total_payable = monthly_emi * n_months + down_payment
    total_interest = total_payable - price

    return jsonify({
        'loan_amount':    round(loan_amount),
        'monthly_emi':    round(monthly_emi),
        'total_payable':  round(total_payable),
        'total_interest': round(total_interest),
        'n_months':       n_months
    })


# ── Route 4: Fuel Cost Estimator ─────────────────────────────────────────────
@app.route('/fuel-cost', methods=['GET'])
def fuel_cost():
    """
    Query params:
      mileage_kmpl    : vehicle fuel efficiency
      daily_km        : kilometers driven per day
      fuel_price_ltr  : price per litre in BDT (default 110 for petrol in BD)
    """
    try:
        mileage_kmpl   = float(request.args.get('mileage_kmpl', 15))
        daily_km       = float(request.args.get('daily_km', 30))
        fuel_price_ltr = float(request.args.get('fuel_price_ltr', 110))
    except ValueError:
        return jsonify({'error': 'Invalid numbers provided'}), 400

    daily_cost   = (daily_km / mileage_kmpl) * fuel_price_ltr
    monthly_cost = daily_cost * 30
    yearly_cost  = daily_cost * 365

    return jsonify({
        'daily_cost':   round(daily_cost),
        'monthly_cost': round(monthly_cost),
        'yearly_cost':  round(yearly_cost),
        'litres_per_day': round(daily_km / mileage_kmpl, 2)
    })


# ── Health check ──────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'AI Vehicle API is running', 'routes': ['/recommend', '/compare', '/emi', '/fuel-cost']})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
