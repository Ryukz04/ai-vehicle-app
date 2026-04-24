# AI Vehicle Finder — Bangladesh 🚗🏍️

An AI-powered web application that recommends cars and bikes to users based on their budget, preferences, and usage patterns — with financial tools like EMI Calculator and Fuel Cost Estimator.

Built for students and first-time vehicle buyers in Bangladesh.

## Features

- **Smart Recommendations** — Filter by budget, fuel type, usage, and brand with an AI scoring engine
- **EMI Calculator** — Calculate monthly loan payments and total cost
- **Fuel Cost Estimator** — Estimate daily, monthly, and yearly fuel expenses
- **Vehicle Data** — 20 popular cars and bikes available in Bangladesh

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Backend  | Python + Flask      |
| Frontend | HTML, CSS, JavaScript |
| Data     | CSV (pandas)        |
| Deploy   | Render (backend) + GitHub Pages (frontend) |

## Project Structure

```
ai-vehicle-app/
├── backend/
│   ├── app.py              ← Flask API with 4 routes
│   └── requirements.txt    ← Python dependencies
├── frontend/
│   └── index.html          ← Full frontend UI
├── data/
│   └── vehicles.csv        ← Vehicle dataset (20 vehicles)
└── README.md
```

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/recommend` | GET | Get vehicle recommendations |
| `/compare` | GET | Compare multiple vehicles |
| `/emi` | GET | Calculate EMI |
| `/fuel-cost` | GET | Estimate fuel expenses |

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-vehicle-app.git
cd ai-vehicle-app

# 2. Set up Python environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Start the Flask server
cd backend
python app.py

# 5. Open frontend
# Open frontend/index.html in your browser
```

## Live Demo

- Frontend: [GitHub Pages link here]
- Backend API: [Render link here]

---

Made with ❤️ by [Your Name] | Student Project
