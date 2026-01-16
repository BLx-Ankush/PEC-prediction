# 🏛️ Using Real UIDAI Data - Integration Guide

## 📥 **Step 1: Obtain UIDAI Data**

Contact UIDAI for historical PEC footfall data through:
- **UIDAI Data Portal**: https://uidai.gov.in
- **API Access**: Request API credentials for real-time data
- **Data Dumps**: Request historical CSV/Excel exports
- **Hackathon Dataset**: Use official hackathon dataset if provided

### **Required Data Fields**

| Field | Description | Example |
|-------|-------------|---------|
| Date | Transaction/Visit date | 2025-01-15 |
| PEC ID / PIN Code | Center identifier | 110001 |
| Location | District, State | Central Delhi, Delhi |
| Center Type | Urban/Rural/Semi-Urban | Urban |
| Footfall Count | Daily visitors/enrollments | 245 |

## 🔄 **Step 2: Data Integration Methods**

### **Method A: Direct CSV Replacement (Simplest)**

If UIDAI data already matches the expected format:

1. Place UIDAI CSV file at: `data/raw/pec_footfall_data.csv`
2. Ensure columns are named: `date, pincode, district, state, center_type, footfall`
3. Run training:
   ```powershell
   python menu.py
   # Choose option 2: Engineer Features
   # Choose option 3: Train Model
   ```

### **Method B: Using Data Adapter (Recommended)**

If UIDAI data has different column names or needs transformation:

```powershell
# Load and transform UIDAI data
python src/load_real_data.py path/to/uidai_data.csv

# This will:
# - Map UIDAI columns to expected format
# - Clean and validate data
# - Save to data/raw/pec_footfall_data.csv
```

### **Method C: Custom API Integration**

For real-time UIDAI API data:

```python
# Create src/fetch_uidai_api.py
import requests
import pandas as pd

def fetch_uidai_footfall(api_key, start_date, end_date):
    """Fetch data from UIDAI API"""
    
    headers = {'Authorization': f'Bearer {api_key}'}
    
    response = requests.get(
        'https://api.uidai.gov.in/footfall',
        headers=headers,
        params={'start': start_date, 'end': end_date}
    )
    
    data = response.json()
    
    # Transform to expected format
    df = pd.DataFrame(data['records'])
    df = transform_api_data(df)
    
    return df
```

## 🔧 **Step 3: Customize Data Adapter**

Edit `src/load_real_data.py` to match UIDAI's actual column names:

```python
# Line 43-50: Modify column_mapping
column_mapping = {
    # Change LEFT side to match UIDAI columns
    'enrollment_date': 'date',           # ← UIDAI's date column name
    'pec_pincode': 'pincode',            # ← UIDAI's PIN column name
    'pec_district': 'district',          # ← UIDAI's district column
    'pec_state': 'state',                # ← UIDAI's state column
    'location_type': 'center_type',      # ← UIDAI's type column
    'daily_transactions': 'footfall',    # ← UIDAI's count column
}
```

## ✅ **Step 4: Data Quality Requirements**

For accurate predictions, ensure:

### **Minimum Requirements:**
- ✅ **At least 60 days** of historical data (for lag features)
- ✅ **Multiple PECs** (at least 10+ centers)
- ✅ **Complete records** (no large gaps in dates)
- ✅ **Recent data** (preferably within last 3 months)

### **Optimal Requirements:**
- ⭐ **12+ months** of data (captures full seasonal cycles)
- ⭐ **50+ PECs** (better geographic diversity)
- ⭐ **Daily records** with minimal missing days
- ⭐ **Current data** (updated weekly/monthly)

## 📊 **Step 5: Validate Real Data**

After loading UIDAI data:

```powershell
python src/load_real_data.py path/to/uidai_data.csv
```

Check the validation output:
```
🔍 Data Quality Checks:
✅ No missing values
📅 Date range: 2024-01-01 to 2025-12-31
📅 Total days: 730
📍 Unique PIN codes: 150
👥 Footfall range: 12 to 450
👥 Average footfall: 165
```

## 🎯 **Step 6: Re-train Model with Real Data**

Once real data is loaded:

```powershell
python menu.py
# Choose: 11 - Run Complete Pipeline
```

Or step-by-step:
```powershell
# 1. Features (synthetic data generation is skipped)
python src/feature_engineering.py

# 2. Train with real data
python src/train_model.py

# 3. Make real predictions
python src/predict.py --pincode 110001 --date 2026-03-15
```

## 🔐 **Data Privacy & Security**

### **For UIDAI Data:**
- ✅ Use **aggregated counts only** (no individual PII)
- ✅ Anonymize PEC identifiers if needed
- ✅ Follow UIDAI's data handling guidelines
- ✅ Ensure compliance with DPDP Act 2023

### **What Data is Safe to Use:**
- ✅ Daily footfall counts per PEC
- ✅ Geographic metadata (PIN, district, state)
- ✅ Center classification (urban/rural)
- ✅ Service type statistics

### **What to NEVER Use:**
- ❌ Individual Aadhaar numbers
- ❌ Biometric data
- ❌ Resident names or personal details
- ❌ Demographic information of residents

## 🔄 **Continuous Updates**

### **Monthly Retraining:**
```powershell
# Automated monthly update script
# Add to cron/Task Scheduler

# 1. Fetch latest data
python src/fetch_uidai_api.py --last-month

# 2. Append to existing data
python src/append_new_data.py

# 3. Retrain model
python src/train_model.py
```

### **Real-time Predictions:**
```python
# For live integration with MyAadhaar app
from src.predict import PECPredictor

predictor = PECPredictor()

# API endpoint
@app.route('/predict/<pincode>/<date>')
def get_prediction(pincode, date):
    footfall = predictor.predict_single_day(pincode, date)
    return {'pincode': pincode, 'date': date, 'predicted_footfall': footfall}
```

## 📞 **UIDAI Data Access Contacts**

For official data access during hackathon:
- **UIDAI Hackathon Portal**: Check official announcement
- **Technical Support**: hackathon-support@uidai.gov.in (hypothetical)
- **Data Access**: data-requests@uidai.gov.in (hypothetical)

## 🎓 **Example: Converting Common UIDAI Formats**

### **Format 1: UIDAI Transaction Log**
```csv
transaction_id,enrollment_center,enrollment_date,service_type,count
TXN001,PEC_110001_Delhi,2025-01-15,New_Enrollment,45
TXN002,PEC_110001_Delhi,2025-01-15,Update,30
```

**Transform to:**
```python
# Group by center and date
df_grouped = df.groupby(['enrollment_center', 'enrollment_date'])['count'].sum()
df_grouped['pincode'] = df_grouped['enrollment_center'].str.extract(r'PEC_(\d+)')
```

### **Format 2: UIDAI Center Daily Summary**
```csv
center_id,reporting_date,total_visitors,location,category
C001,2025-01-15,245,Central Delhi|Delhi,Urban
```

**Transform to:**
```python
df[['district', 'state']] = df['location'].str.split('|', expand=True)
df = df.rename(columns={'total_visitors': 'footfall', 'category': 'center_type'})
```

## 🚀 **Quick Start with Sample Real Data**

If you have UIDAI data right now:

```powershell
# 1. Save UIDAI data as: uidai_real_data.csv

# 2. Transform it
python src/load_real_data.py uidai_real_data.csv

# 3. Check if it worked
python -c "import pandas as pd; df=pd.read_csv('data/raw/pec_footfall_data.csv'); print(df.head())"

# 4. Train with real data
python menu.py
# Choose option 11
```

## 💡 **Tips for Hackathon**

1. **If no real data yet**: Use synthetic data to build/demo the model
2. **During presentation**: Explain how real data integration works
3. **Show adaptability**: Demonstrate the data adapter script
4. **Emphasize privacy**: Highlight that only aggregate counts are used
5. **Future roadmap**: Mention API integration for production

## ✨ **You're Ready!**

The system is designed to work with:
- ✅ Synthetic data (for development/demo)
- ✅ Real UIDAI data (for production)
- ✅ API streams (for real-time predictions)
- ✅ Any PEC footfall data (with minimal adaptation)

Just plug in real data and retrain - the model architecture remains the same! 🎯
