# PEC Demand Forecasting - Quick Start Guide

## 🚀 Installation & Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Complete Pipeline (Recommended)
This will generate data, train the model, and create all visualizations:
```powershell
python run_pipeline.py
```

## 📊 Individual Components

### Generate Data Only
```powershell
python src/data_generator.py
```

### Feature Engineering Only
```powershell
python src/feature_engineering.py
```

### Train Model Only
```powershell
python src/train_model.py
```

### Generate Visualizations Only
```powershell
# Heatmaps
python visualizations/demand_heatmap.py

# Trend Analysis
python visualizations/trend_analysis.py
```

## 🔮 Making Predictions

### Single Day Prediction
```powershell
python src/predict.py --pincode 110001 --date 2026-03-15
```
Output:
```
✅ PREDICTION RESULT:
  PIN Code:    110001
  District:    Central Delhi, Delhi
  Center Type: Urban
  Date:        2026-03-15
  Predicted:   245 residents
```

### Weekly Forecast
```powershell
python src/predict.py --pincode 562157 --week 2026-03-10
```

### Monthly Forecast
```powershell
python src/predict.py --pincode 400001 --month 6 --year 2026
```

## 📍 Available PIN Codes

The dataset includes 20 major Indian centers:
- **110001** - Central Delhi (Urban)
- **400001** - Mumbai City (Urban)
- **560001** - Bangalore Urban (Urban)
- **562157** - Bangalore Rural (Rural)
- **600001** - Chennai (Urban)
- **700001** - Kolkata (Urban)
- **500001** - Hyderabad (Urban)
- And 13 more...

## 🎯 Key Features

### Model Capabilities
- Predicts footfall ±15-20 residents on average
- Handles seasonal patterns (school enrollment, pension updates)
- Accounts for weekly patterns (Monday peaks, weekend lows)
- Considers holiday impacts and surge effects

### Strategic Insights
- Identifies peak demand periods for manpower allocation
- Highlights underserved areas for mobile van deployment
- Provides district-level comparisons for resource planning
- Shows urban vs rural demand patterns

## 📈 Output Files

After running the pipeline:

```
project/
├── data/
│   ├── raw/pec_footfall_data.csv          # 8,060 records
│   └── processed/pec_features.csv          # 40+ features
├── models/
│   ├── pec_demand_model.json               # Trained XGBoost
│   ├── model_metadata.pkl                  # Feature names
│   ├── feature_importance.png              # Top features chart
│   └── predictions_vs_actual.png           # Accuracy plot
└── visualizations/output/
    ├── demand_heatmap_*.png                # PIN × Day heatmap
    ├── district_comparison_*.png           # District bars
    ├── urban_rural_comparison.png          # Center types
    ├── day_of_week_pattern.png            # Weekly trends
    ├── holiday_impact.png                  # Holiday analysis
    ├── seasonal_trends.png                 # Monthly patterns
    └── comprehensive_dashboard.png         # Full overview
```

## 🏆 Hackathon Presentation Tips

### Key Points to Highlight:
1. **Real-World Impact**: Reduces wait times, optimizes resources
2. **Technical Sophistication**: XGBoost + 40+ engineered features
3. **Actionable Insights**: Mobile van deployment, staff allocation
4. **Citizen-Centric**: Can integrate with MyAadhaar app
5. **Scalability**: Works for all 50,000+ PECs nationwide

### Demo Flow:
1. Show comprehensive dashboard
2. Demonstrate prediction for a rural area in pension month
3. Show urban center during school enrollment season
4. Explain lag features and their importance
5. Present district-level heatmap for resource allocation

## 🔧 Troubleshooting

### Error: "No module named 'xgboost'"
```powershell
pip install xgboost
```

### Error: "No such file or directory: 'data/raw/...'"
Run data generation first:
```powershell
python src/data_generator.py
```

### Error: "Model file not found"
Train the model first:
```powershell
python src/train_model.py
```

## 📝 Customization

### Add New PIN Codes
Edit `src/data_generator.py`, line 18-38, add your PIN in `self.pincodes` dict.

### Change Date Range
Edit `src/data_generator.py`, line 82-83:
```python
start_date='2024-01-01',
end_date='2027-12-31'
```

### Tune Model Parameters
Edit `src/train_model.py`, line 76-88 (XGBoost params).

## 💡 Next Steps

1. **Integrate Real Data**: Replace synthetic data with actual UIDAI footfall
2. **API Development**: Build REST API for real-time predictions
3. **Mobile App**: Connect to MyAadhaar for crowd alerts
4. **Auto-Retraining**: Schedule monthly model updates
5. **Weather Integration**: Add monsoon/temperature effects

## 📧 Support

For UIDAI Data Hackathon 2026 queries, refer to the main [README.md](README.md)
