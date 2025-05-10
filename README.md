# 📈 Investment Tracker & Portfolio Performance Dashboard
This repository contains a Streamlit-based web application designed to help track investments and visualize key statistics comparing expected vs. actual portfolio performance.

Whether you're a personal investor or just curious about your portfolio evolution, this tool provides insights into how your investments are performing against your expectations.

## 🚀 Features
#### 📊 Track Investment Performance
Log and monitor the performance of your investments over time.

#### 📈 Expected vs Actual Statistics
Compare your projected performance with the real data using clear visualizations.

#### 🧮 Streamlit-Powered Dashboard
A fast, interactive, and lightweight web interface using Streamlit.

## 🛠️ Project Structure
```
portfolio-performance/
├── app/ # Streamlit application scripts 
│ └── main.py # Main app entry point 
│ └── orchestrator.py # Main Calculation entry point
│ └── assets_handler.py # Input data Processing and helper functions  
│ └── processor.py # Data Processor
│ └── visualiser.py # Data Visualiser 
├── data/ # Portfolio data (input/output) 
│ ├── Assets.xslx 
│ └── inflation-rate-hicp.csv  
├── requirements.txt # Python dependencies 
├── .gitignore 
└── README.md # Project overview 
```

🧪 How to Run
1. **Clone the repository**

```
git clone https://github.com/ErikPillon/portfolio-performance
cd portfolio-performance
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Launch the app**

```
streamlit run app/main.py
```

## 🔮 Future Plans

#### 💵 Bond Portfolio Tracking
Include tracking and statistics for fixed-income assets.

#### 🧠 Sentiment Analysis Tool
Inspired by CNN's Fear & Greed Index, integrate a sentiment-based indicator for smarter investment decisions.

#### 📊 Enhanced Visualizations
More interactive charts, dashboards, and possibly benchmarking tools.

#### 💬 Custom Alerts / Notifications
Add triggers or flags for underperformance or deviation from expected returns.

## 🤝 Contributing
Pull requests and suggestions are welcome! If you’d like to help expand the dashboard, please fork the repo and submit a PR.

## 📜 License
This project is licensed under the MIT License.