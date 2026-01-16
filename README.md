# 🏛️ PEC Demand Forecasting Model - UIDAI Data Hackathon 2026

## 📋 Overview
A machine learning solution to predict footfall at Permanent Enrollment Centers (PECs) across India, enabling efficient resource allocation and improved citizen experience.

## 🎯 Problem Statement
Aadhaar centers face two critical issues:
- **Overcrowding**: Long wait times during peak periods (school admissions, scheme deadlines)
- **Under-utilization**: Idle resources at low-footfall centers

## 💡 Solution
XGBoost-based regression model that predicts daily footfall at each PEC, considering:
- Temporal patterns (day of week, holidays, seasons)
- Geographic factors (PIN code, urban/rural classification)
- Historical trends (lag features, moving averages)

## 🏗️ Project Structure
```
pec-demand-forecasting/
├── data/
│   ├── raw/              # Generated synthetic data
│   ├── processed/        # Feature-engineered datasets
│   └── predictions/      # Model outputs
├── src/
│   ├── data_generator.py       # Synthetic data creation
│   ├── feature_engineering.py  # Feature extraction pipeline
│   ├── train_model.py          # XGBoost training script
│   └── predict.py              # Inference interface
├── visualizations/
│   ├── demand_heatmap.py       # Geographic demand visualization
│   └── trend_analysis.py       # Time-series analysis
├── models/                      # Saved model artifacts
└── notebooks/                   # Exploratory analysis
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Synthetic Data
```bash
python src/data_generator.py
```

### 3. Train the Model
```bash
python src/train_model.py
```

### 4. Make Predictions
```bash
python src/predict.py --pincode 562157 --date 2026-03-15
```

## 📊 Key Features

### Temporal Features
- Day of week (Mondays = Higher footfall)
- Holiday flags (Public holidays + Day-after spikes)
- Month/Season (June-July school enrollment, Nov pension updates)
- Week of month

### Geographic Features
- PIN code (Locality-specific patterns)
- Urban/Rural classification
- District-level aggregations

### Lag Features (Time-Series)
- Footfall 7 days ago (Week-over-week comparison)
- 30-day moving average (Trend detection)
- Monthly aggregates (Seasonal patterns)

## 🎖️ Strategic Impact

### For UIDAI
- **Dynamic Manpower Allocation**: Shift operators to predicted hotspots
- **Mobile Van Deployment**: Target high-demand, low-access areas
- **Infrastructure Planning**: Data-driven decisions on new PEC locations

### For Citizens
- **Reduced Wait Times**: Visit during predicted off-peak hours
- **MyAadhaar Integration**: Real-time "Busy-ness Meter" (like Google Maps)
- **Better Accessibility**: Proactive mobile van deployments in underserved areas

## 📈 Model Performance Metrics
- **MAE (Mean Absolute Error)**: Average prediction error in footfall count
- **RMSE (Root Mean Squared Error)**: Handles outliers/spikes better
- **R² Score**: Explains variance in demand patterns
- **MAPE (Mean Absolute Percentage Error)**: Percentage accuracy

## 🛠️ Tech Stack
- **Python 3.10+**: Core language
- **XGBoost**: Gradient boosting for regression
- **Pandas/NumPy**: Data manipulation and lag calculations
- **Matplotlib/Seaborn**: Demand heatmaps and trend visualizations
- **Scikit-learn**: Preprocessing and evaluation metrics

## 📝 Usage Examples

### Example 1: Weekly Demand Forecast
```python
from src.predict import forecast_week
predictions = forecast_week(pincode="110001", start_date="2026-03-10")
```

### Example 2: District-Wide Heatmap
```python
from visualizations.demand_heatmap import create_heatmap
create_heatmap(district="Bangalore Urban", date="2026-03-15")
```

## 🏆 Hackathon Pitch Points
1. **Real Administrative Value**: Not just ML for ML's sake
2. **Scalable Solution**: Works for 50,000+ PECs nationwide
3. **Citizen-Centric**: Directly improves user experience
4. **Data-Driven Governance**: Demonstrates UIDAI's innovation

## 📅 Future Enhancements
- Real-time updates using live footfall APIs
- Integration with MyAadhaar app for crowd notifications
- Weather impact analysis (Monsoon = Lower rural footfall)
- Festival calendar integration (Regional variations)

## 👥 Team
Built for UIDAI Data Hackathon 2026

## 📄 License
Educational Purpose - UIDAI Hackathon 2026
