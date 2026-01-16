"""
Prediction Interface
Make predictions for future PEC demand using trained model
"""

import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from datetime import datetime, timedelta
import argparse
import os

class PECPredictor:
    """Interface for making PEC demand predictions"""
    
    def __init__(self, model_path='models/pec_demand_model.json',
                 metadata_path='models/model_metadata.pkl',
                 data_path='data/processed/pec_features.csv'):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to saved XGBoost model
            metadata_path: Path to model metadata
            data_path: Path to historical data (for lag features)
        """
        # Load model
        self.model = xgb.XGBRegressor()
        self.model.load_model(model_path)
        
        # Load metadata
        metadata = joblib.load(metadata_path)
        self.feature_names = metadata['feature_names']
        
        # Load historical data (needed for lag features)
        self.historical_data = pd.read_csv(data_path, dtype={'pincode': str})
        self.historical_data['date'] = pd.to_datetime(self.historical_data['date'])
        
        # Ensure pincode is string type
        self.historical_data['pincode'] = self.historical_data['pincode'].astype(str)
        
        print("✅ Model loaded successfully")
        print(f"📊 Features: {len(self.feature_names)}")
        print(f"📅 Historical data: {len(self.historical_data):,} records")
        
        # PIN code info
        self.pincode_info = self._get_pincode_info()
    
    def predict_single_day(self, pincode, date_str):
        """
        Predict footfall for a specific PIN code and date
        
        Args:
            pincode: PIN code (e.g., '110001')
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            Predicted footfall (integer)
        """
        target_date = pd.to_datetime(date_str)
        
        # Ensure pincode is string
        pincode = str(pincode)
        
        # Get PIN code info
        if pincode not in self.pincode_info:
            print(f"❌ PIN code {pincode} not found in database")
            available_pins = [str(p) for p in list(self.pincode_info.keys())[:5]]
            print(f"Available PINs: {', '.join(available_pins)}...")
            return None
        
        # Build features for prediction
        features = self._build_features(pincode, target_date)
        
        if features is None:
            return None
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        prediction = max(0, int(round(prediction)))  # Ensure non-negative integer
        
        return prediction
    
    def predict_week(self, pincode, start_date_str):
        """
        Predict footfall for a week (7 days)
        
        Args:
            pincode: PIN code (e.g., '110001')
            start_date_str: Start date in YYYY-MM-DD format
            
        Returns:
            DataFrame with daily predictions
        """
        start_date = pd.to_datetime(start_date_str)
        
        predictions = []
        
        for day_offset in range(7):
            current_date = start_date + timedelta(days=day_offset)
            pred = self.predict_single_day(pincode, current_date.strftime('%Y-%m-%d'))
            
            if pred is not None:
                predictions.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day_name': current_date.strftime('%A'),
                    'predicted_footfall': pred
                })
        
        return pd.DataFrame(predictions)
    
    def predict_month(self, pincode, year, month):
        """
        Predict footfall for an entire month
        
        Args:
            pincode: PIN code (e.g., '110001')
            year: Year (e.g., 2026)
            month: Month (1-12)
            
        Returns:
            DataFrame with daily predictions
        """
        # Get number of days in month
        start_date = datetime(year, month, 1)
        
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        predictions = []
        
        current_date = start_date
        while current_date <= end_date:
            pred = self.predict_single_day(pincode, current_date.strftime('%Y-%m-%d'))
            
            if pred is not None:
                predictions.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day_name': current_date.strftime('%A'),
                    'predicted_footfall': pred
                })
            
            current_date += timedelta(days=1)
        
        df = pd.DataFrame(predictions)
        
        # Add summary statistics
        if len(df) > 0:
            print(f"\n📊 Monthly Summary for {pincode}:")
            print(f"  Total predicted footfall: {df['predicted_footfall'].sum():,} residents")
            print(f"  Average daily footfall:   {df['predicted_footfall'].mean():.0f} residents")
            print(f"  Peak day:                 {df['predicted_footfall'].max():,} residents")
            print(f"  Lowest day:               {df['predicted_footfall'].min():,} residents")
        
        return df
    
    def compare_pincodes(self, pincodes, date_str):
        """
        Compare predicted demand across multiple PIN codes for a specific date
        
        Args:
            pincodes: List of PIN codes
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            DataFrame with comparison
        """
        results = []
        
        for pincode in pincodes:
            pred = self.predict_single_day(pincode, date_str)
            
            if pred is not None and pincode in self.pincode_info:
                info = self.pincode_info[pincode]
                results.append({
                    'pincode': pincode,
                    'district': info['district'],
                    'state': info['state'],
                    'center_type': info['center_type'],
                    'predicted_footfall': pred
                })
        
        df = pd.DataFrame(results).sort_values('predicted_footfall', ascending=False)
        
        return df
    
    def _build_features(self, pincode, target_date):
        """Build feature vector for prediction"""
        
        # Ensure pincode is string
        pincode = str(pincode)
        
        # Get PIN info
        info = self.pincode_info[pincode]
        
        # Get historical data for this PIN (for lag features)
        pin_history = self.historical_data[
            self.historical_data['pincode'] == pincode
        ].sort_values('date')
        
        if len(pin_history) == 0:
            print(f"❌ No historical data found for PIN {pincode}")
            return None
        
        # Check if we can calculate lag features
        max_hist_date = pin_history['date'].max()
        if target_date <= max_hist_date:
            print(f"⚠️  Target date {target_date.date()} is in training data. Using existing features.")
            existing = self.historical_data[
                (self.historical_data['pincode'] == pincode) &
                (self.historical_data['date'] == target_date)
            ]
            if len(existing) > 0:
                return existing[self.feature_names].iloc[[0]]
        
        # Build features manually
        features = {}
        
        # Temporal features
        features['day_of_week'] = target_date.dayofweek
        features['is_weekend'] = int(target_date.dayofweek >= 5)
        features['is_monday'] = int(target_date.dayofweek == 0)
        features['month'] = target_date.month
        features['quarter'] = (target_date.month - 1) // 3 + 1
        features['week_of_month'] = (target_date.day - 1) // 7 + 1
        features['day_of_month'] = target_date.day
        features['is_first_week'] = int(features['week_of_month'] == 1)
        features['day_of_year'] = target_date.timetuple().tm_yday
        
        # Holiday features (simplified - would need actual holiday calendar)
        features['is_holiday'] = 0
        features['is_day_after_holiday'] = 0
        
        # Season indicators
        features['is_enrollment_season'] = int(target_date.month in [6, 7])
        features['is_pension_month'] = int(target_date.month == 11)
        features['is_festival_season'] = int(target_date.month == 10)
        
        # Geographic features
        type_mapping = {'Rural': 0, 'Semi-Urban': 1, 'Urban': 2}
        features['center_type_encoded'] = type_mapping.get(info['center_type'], 1)
        features['is_urban'] = int(info['center_type'] == 'Urban')
        features['is_rural'] = int(info['center_type'] == 'Rural')
        
        # State and district encoding (using same encoding from training)
        features['state_encoded'] = self._encode_categorical(info['state'], 'state')
        features['district_encoded'] = self._encode_categorical(info['district'], 'district')
        
        # Lag features (most critical!)
        features = self._calculate_lag_features(features, pin_history, target_date)
        
        # Interaction features
        features['rural_pension_interaction'] = features['is_rural'] * features['is_pension_month']
        features['urban_enrollment_interaction'] = features['is_urban'] * features['is_enrollment_season']
        features['monday_first_week'] = features['is_monday'] * features['is_first_week']
        features['weekend_holiday'] = features['is_weekend'] * features['is_holiday']
        
        if 'footfall_lag_7' in features and 'footfall_rolling_mean_30' in features:
            features['lag_ratio_7_to_30'] = features['footfall_lag_7'] / (features['footfall_rolling_mean_30'] + 1)
        else:
            features['lag_ratio_7_to_30'] = 1.0
        
        # Pincode category (need to match training format)
        features['pincode_category'] = pincode
        
        # Convert to DataFrame with correct column order
        feature_df = pd.DataFrame([features])
        
        # Ensure all required features exist
        for feat in self.feature_names:
            if feat not in feature_df.columns:
                feature_df[feat] = 0
        
        return feature_df[self.feature_names]
    
    def _calculate_lag_features(self, features, pin_history, target_date):
        """Calculate lag features from historical data"""
        
        # Get recent history
        recent = pin_history[pin_history['date'] < target_date].tail(60)
        
        if len(recent) == 0:
            # No history - use defaults
            features['footfall_lag_7'] = 100
            features['footfall_lag_14'] = 100
            features['footfall_lag_30'] = 100
            features['footfall_rolling_mean_7'] = 100
            features['footfall_rolling_mean_14'] = 100
            features['footfall_rolling_mean_30'] = 100
            features['footfall_rolling_std_7'] = 10
            features['footfall_rolling_max_30'] = 150
            features['footfall_rolling_min_30'] = 50
            return features
        
        # Calculate lags
        if len(recent) >= 7:
            features['footfall_lag_7'] = recent.iloc[-7]['footfall']
        else:
            features['footfall_lag_7'] = recent['footfall'].mean()
        
        if len(recent) >= 14:
            features['footfall_lag_14'] = recent.iloc[-14]['footfall']
        else:
            features['footfall_lag_14'] = recent['footfall'].mean()
        
        if len(recent) >= 30:
            features['footfall_lag_30'] = recent.iloc[-30]['footfall']
        else:
            features['footfall_lag_30'] = recent['footfall'].mean()
        
        # Rolling statistics
        features['footfall_rolling_mean_7'] = recent.tail(7)['footfall'].mean()
        features['footfall_rolling_mean_14'] = recent.tail(14)['footfall'].mean()
        features['footfall_rolling_mean_30'] = recent.tail(30)['footfall'].mean()
        features['footfall_rolling_std_7'] = recent.tail(7)['footfall'].std() or 10
        features['footfall_rolling_max_30'] = recent.tail(30)['footfall'].max()
        features['footfall_rolling_min_30'] = recent.tail(30)['footfall'].min()
        
        return features
    
    def _encode_categorical(self, value, column_type):
        """Encode categorical values consistently with training"""
        unique_values = self.historical_data[column_type].unique()
        if value in unique_values:
            return list(unique_values).index(value)
        return 0
    
    def _get_pincode_info(self):
        """Extract PIN code information from historical data"""
        info = {}
        for pincode in self.historical_data['pincode'].unique():
            pincode_str = str(pincode)  # Ensure string type
            pin_data = self.historical_data[self.historical_data['pincode'] == pincode].iloc[0]
            info[pincode_str] = {
                'district': pin_data['district'],
                'state': pin_data['state'],
                'center_type': pin_data['center_type']
            }
        return info

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='PEC Demand Forecasting - Prediction Interface')
    parser.add_argument('--pincode', type=str, required=True, help='PIN code (e.g., 110001)')
    parser.add_argument('--date', type=str, help='Date (YYYY-MM-DD) for single prediction')
    parser.add_argument('--week', type=str, help='Start date (YYYY-MM-DD) for weekly prediction')
    parser.add_argument('--month', type=int, help='Month (1-12) for monthly prediction')
    parser.add_argument('--year', type=int, help='Year for monthly prediction')
    
    args = parser.parse_args()
    
    print("🏛️  PEC Demand Forecasting - Prediction Interface")
    print("=" * 60)
    
    # Initialize predictor
    predictor = PECPredictor()
    
    # Single day prediction
    if args.date:
        print(f"\n🔮 Predicting for PIN {args.pincode} on {args.date}...")
        prediction = predictor.predict_single_day(args.pincode, args.date)
        
        if prediction is not None:
            info = predictor.pincode_info[args.pincode]
            print(f"\n✅ PREDICTION RESULT:")
            print(f"  PIN Code:    {args.pincode}")
            print(f"  District:    {info['district']}, {info['state']}")
            print(f"  Center Type: {info['center_type']}")
            print(f"  Date:        {args.date}")
            print(f"  Predicted:   {prediction:,} residents")
    
    # Weekly prediction
    elif args.week:
        print(f"\n🔮 Predicting week starting {args.week} for PIN {args.pincode}...")
        predictions = predictor.predict_week(args.pincode, args.week)
        
        print("\n📅 WEEKLY FORECAST:")
        print(predictions.to_string(index=False))
        print(f"\nWeekly total: {predictions['predicted_footfall'].sum():,} residents")
    
    # Monthly prediction
    elif args.month and args.year:
        print(f"\n🔮 Predicting {args.year}-{args.month:02d} for PIN {args.pincode}...")
        predictions = predictor.predict_month(args.pincode, args.year, args.month)
        
        if len(predictions) > 0:
            print("\n📅 MONTHLY FORECAST:")
            print(predictions.to_string(index=False))
    
    else:
        print("\n❌ Please specify --date, --week, or --month/--year")
        print("\nExamples:")
        print("  python src/predict.py --pincode 110001 --date 2026-03-15")
        print("  python src/predict.py --pincode 562157 --week 2026-03-10")
        print("  python src/predict.py --pincode 400001 --month 6 --year 2026")

if __name__ == "__main__":
    main()
