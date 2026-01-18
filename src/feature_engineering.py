"""
Feature Engineering Pipeline
Extracts temporal, geographic, and lag features from raw footfall data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class FeatureEngineer:
    """Extract and transform features for ML model"""
    
    def __init__(self):
        # Indian public holidays (will be used for is_holiday feature)
        self.holidays = [
            '2025-01-26', '2025-03-14', '2025-03-31', '2025-04-10', '2025-04-14',
            '2025-05-01', '2025-08-15', '2025-08-27', '2025-10-02', '2025-10-24',
            '2025-11-01', '2025-12-25',
            '2026-01-26', '2026-03-03', '2026-03-25', '2026-03-30', '2026-04-14',
            '2026-05-01', '2026-08-15', '2026-08-16', '2026-10-02', '2026-10-13',
            '2026-11-01', '2026-11-14', '2026-12-25'
        ]
    
    def _validate_and_fix_columns(self, df):
        """
        Auto-detect and fix missing or incorrectly named columns
        
        Required columns:
        - date (datetime)
        - pincode (string/int)
        - footfall (numeric)
        - district (string)
        - state (string)
        - center_type (string: Urban/Rural/Semi-Urban)
        """
        print("\n🔍 Validating dataset columns...")
        
        original_cols = df.columns.tolist()
        issues_fixed = 0
        
        # 1. Check required columns
        required_cols = ['date', 'pincode', 'footfall', 'district', 'state', 'center_type']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"⚠️  Missing columns detected: {missing_cols}")
            
            # Try to auto-fix common naming variations
            column_mapping = {
                # Date variations
                'Date': 'date',
                'DATE': 'date',
                'transaction_date': 'date',
                'visit_date': 'date',
                
                # PIN code variations
                'PIN': 'pincode',
                'pin': 'pincode',
                'PIN_code': 'pincode',
                'pin_code': 'pincode',
                'PINCODE': 'pincode',
                'pec_id': 'pincode',
                'center_id': 'pincode',
                
                # Footfall variations
                'Footfall': 'footfall',
                'FOOTFALL': 'footfall',
                'count': 'footfall',
                'visitors': 'footfall',
                'footfall_count': 'footfall',
                'daily_count': 'footfall',
                'transactions': 'footfall',
                'enrollments': 'footfall',
                
                # District variations
                'District': 'district',
                'DISTRICT': 'district',
                'dist': 'district',
                
                # State variations
                'State': 'state',
                'STATE': 'state',
                
                # Center type variations
                'center_type': 'center_type',
                'Center_Type': 'center_type',
                'CENTER_TYPE': 'center_type',
                'type': 'center_type',
                'location_type': 'center_type',
                'pec_type': 'center_type',
            }
            
            # Apply mappings
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns and new_col not in df.columns:
                    df.rename(columns={old_col: new_col}, inplace=True)
                    print(f"  ✅ Renamed '{old_col}' → '{new_col}'")
                    issues_fixed += 1
        
        # 2. Check again for missing columns and infer them
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if 'center_type' not in df.columns:
            print("  ⚠️  'center_type' missing - inferring from PIN code patterns...")
            # Infer center type based on footfall patterns
            if 'footfall' in df.columns:
                df['center_type'] = df['footfall'].apply(lambda x: 
                    'Urban' if x > 150 else ('Rural' if x < 100 else 'Semi-Urban')
                )
                print(f"  ✅ Inferred center_type from footfall patterns")
                issues_fixed += 1
            else:
                # Default to Urban
                df['center_type'] = 'Urban'
                print(f"  ⚠️  Defaulting all to 'Urban' center type")
                issues_fixed += 1
        
        if 'district' not in df.columns:
            print("  ⚠️  'district' missing - using default values...")
            df['district'] = 'Unknown District'
            issues_fixed += 1
        
        if 'state' not in df.columns:
            print("  ⚠️  'state' missing - using default values...")
            df['state'] = 'Unknown State'
            issues_fixed += 1
        
        # 3. Ensure pincode is string type
        if 'pincode' in df.columns:
            df['pincode'] = df['pincode'].astype(str)
        
        # 4. Standardize center_type values
        if 'center_type' in df.columns:
            # Map variations to standard values
            center_type_mapping = {
                'urban': 'Urban',
                'URBAN': 'Urban',
                'U': 'Urban',
                'rural': 'Rural',
                'RURAL': 'Rural',
                'R': 'Rural',
                'semi-urban': 'Semi-Urban',
                'semi urban': 'Semi-Urban',
                'SEMI-URBAN': 'Semi-Urban',
                'SEMI URBAN': 'Semi-Urban',
                'S': 'Semi-Urban',
                'semiurban': 'Semi-Urban',
            }
            
            df['center_type'] = df['center_type'].replace(center_type_mapping)
            
            # Set any unrecognized values to Urban
            valid_types = ['Urban', 'Rural', 'Semi-Urban']
            invalid_mask = ~df['center_type'].isin(valid_types)
            if invalid_mask.any():
                invalid_count = invalid_mask.sum()
                print(f"  ⚠️  Found {invalid_count} invalid center_type values - defaulting to 'Urban'")
                df.loc[invalid_mask, 'center_type'] = 'Urban'
                issues_fixed += 1
        
        # 5. Final validation
        final_missing = [col for col in required_cols if col not in df.columns]
        if final_missing:
            print(f"\n❌ ERROR: Still missing required columns: {final_missing}")
            print(f"   Available columns: {df.columns.tolist()}")
            raise ValueError(f"Cannot proceed without required columns: {final_missing}")
        
        if issues_fixed > 0:
            print(f"\n✅ Auto-fixed {issues_fixed} column issues")
        else:
            print("✅ All required columns present")
        
        print(f"📊 Final columns: {df.columns.tolist()}")
        
        return df
    
    def engineer_features(self, input_path='data/raw/pec_footfall_data.csv', 
                         output_dir='data/processed'):
        """
        Create all features from raw data
        
        Args:
            input_path: Path to raw CSV file
            output_dir: Directory to save processed data
        """
        print("🔧 Starting Feature Engineering...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(input_path)
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"📊 Loaded {len(df):,} records")
        
        # AUTO-FIX: Validate and correct column names
        df = self._validate_and_fix_columns(df)
        
        # Sort by pincode and date (essential for lag features)
        df = df.sort_values(['pincode', 'date']).reset_index(drop=True)
        
        # 1. TEMPORAL FEATURES
        print("\n⏰ Creating temporal features...")
        df = self._add_temporal_features(df)
        
        # 2. GEOGRAPHIC FEATURES
        print("🗺️  Creating geographic features...")
        df = self._add_geographic_features(df)
        
        # 3. LAG FEATURES (Time-Series)
        print("📈 Creating lag features...")
        df = self._add_lag_features(df)
        
        # 4. INTERACTION FEATURES
        print("🔗 Creating interaction features...")
        df = self._add_interaction_features(df)
        
        # Remove rows with NaN (due to lag feature calculation)
        initial_count = len(df)
        df = df.dropna()
        print(f"\n🧹 Removed {initial_count - len(df):,} rows with missing lag values")
        
        # Save processed data
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'pec_features.csv')
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ Feature engineering complete!")
        print(f"📁 Saved to: {output_path}")
        print(f"📊 Final dataset: {len(df):,} records with {len(df.columns)} features")
        
        # Show feature list
        print("\n🔍 Created Features:")
        feature_cols = [col for col in df.columns if col not in ['date', 'footfall']]
        for i, col in enumerate(feature_cols, 1):
            print(f"   {i:2d}. {col}")
        
        return df
    
    def _add_temporal_features(self, df):
        """Add date-based temporal features"""
        
        # Day of week (0=Monday, 6=Sunday)
        df['day_of_week'] = df['date'].dt.dayofweek
        
        # Day name (for readability)
        df['day_name'] = df['date'].dt.day_name()
        
        # Is weekend
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Is Monday (typically highest footfall)
        df['is_monday'] = (df['day_of_week'] == 0).astype(int)
        
        # Month (1-12)
        df['month'] = df['date'].dt.month
        
        # Quarter
        df['quarter'] = df['date'].dt.quarter
        
        # Week of month (1-5)
        df['week_of_month'] = ((df['date'].dt.day - 1) // 7 + 1)
        
        # Day of month
        df['day_of_month'] = df['date'].dt.day
        
        # Is first week of month (bill payments, updates)
        df['is_first_week'] = (df['week_of_month'] == 1).astype(int)
        
        # Is holiday
        df['is_holiday'] = df['date'].dt.strftime('%Y-%m-%d').isin(self.holidays).astype(int)
        
        # Is day after holiday (spike effect)
        df['is_day_after_holiday'] = df.groupby('pincode')['is_holiday'].shift(1).fillna(0).astype(int)
        
        # Peak enrollment months (June-July for schools)
        df['is_enrollment_season'] = df['month'].isin([6, 7]).astype(int)
        
        # Pension update month (November)
        df['is_pension_month'] = (df['month'] == 11).astype(int)
        
        # Festival season (October)
        df['is_festival_season'] = (df['month'] == 10).astype(int)
        
        # Days since year start (trend feature)
        df['day_of_year'] = df['date'].dt.dayofyear
        
        return df
    
    def _add_geographic_features(self, df):
        """Add location-based features"""
        
        # Encode center type as numeric
        type_mapping = {'Rural': 0, 'Semi-Urban': 1, 'Urban': 2}
        df['center_type_encoded'] = df['center_type'].map(type_mapping)
        
        # Is urban center
        df['is_urban'] = (df['center_type'] == 'Urban').astype(int)
        
        # Is rural center
        df['is_rural'] = (df['center_type'] == 'Rural').astype(int)
        
        # State-level encoding (using label encoding for simplicity)
        df['state_encoded'] = pd.factorize(df['state'])[0]
        
        # District-level encoding
        df['district_encoded'] = pd.factorize(df['district'])[0]
        
        # PIN code as category (XGBoost can handle this with enable_categorical)
        df['pincode_category'] = df['pincode'].astype('category')
        
        return df
    
    def _add_lag_features(self, df):
        """Add time-series lag features (CRITICAL for forecasting)"""
        
        # For each PIN code, calculate lags
        
        # 1. Lag 7 days (same day last week)
        df['footfall_lag_7'] = df.groupby('pincode')['footfall'].shift(7)
        
        # 2. Lag 14 days (two weeks ago)
        df['footfall_lag_14'] = df.groupby('pincode')['footfall'].shift(14)
        
        # 3. Lag 30 days (approximately a month ago)
        df['footfall_lag_30'] = df.groupby('pincode')['footfall'].shift(30)
        
        # 4. Rolling mean - last 7 days
        df['footfall_rolling_mean_7'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
            .shift(1)  # Shift to avoid data leakage
        )
        
        # 5. Rolling mean - last 14 days
        df['footfall_rolling_mean_14'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=14, min_periods=1).mean())
            .shift(1)
        )
        
        # 6. Rolling mean - last 30 days
        df['footfall_rolling_mean_30'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=30, min_periods=1).mean())
            .shift(1)
        )
        
        # 7. Rolling standard deviation (volatility measure)
        df['footfall_rolling_std_7'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=7, min_periods=1).std())
            .shift(1)
        )
        
        # 8. Week-over-week change
        df['footfall_change_7d'] = df['footfall'] - df['footfall_lag_7']
        
        # 9. Month-over-month trend
        df['footfall_change_30d'] = df['footfall'] - df['footfall_lag_30']
        
        # 10. Rolling max (peak demand indicator)
        df['footfall_rolling_max_30'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=30, min_periods=1).max())
            .shift(1)
        )
        
        # 11. Rolling min (low demand indicator)
        df['footfall_rolling_min_30'] = (
            df.groupby('pincode')['footfall']
            .transform(lambda x: x.rolling(window=30, min_periods=1).min())
            .shift(1)
        )
        
        return df
    
    def _add_interaction_features(self, df):
        """Create interaction features between different categories"""
        
        # 1. Rural + Pension Month (strong interaction)
        df['rural_pension_interaction'] = df['is_rural'] * df['is_pension_month']
        
        # 2. Urban + Enrollment Season
        df['urban_enrollment_interaction'] = df['is_urban'] * df['is_enrollment_season']
        
        # 3. Monday + First Week (double peak effect)
        df['monday_first_week'] = df['is_monday'] * df['is_first_week']
        
        # 4. Weekend + Holiday (extra low demand)
        df['weekend_holiday'] = df['is_weekend'] * df['is_holiday']
        
        # 5. Lag ratio (current trend vs historical average)
        df['lag_ratio_7_to_30'] = df['footfall_lag_7'] / (df['footfall_rolling_mean_30'] + 1)
        
        return df

def main():
    """Main execution function"""
    print("🏛️  PEC Demand Forecasting - Feature Engineering")
    print("=" * 60)
    
    engineer = FeatureEngineer()
    
    # Process the data
    df = engineer.engineer_features()
    
    print("\n✨ Feature engineering complete!")
    print("\n🔍 Sample processed records:")
    print(df[['date', 'pincode', 'footfall', 'day_of_week', 'is_holiday', 
              'footfall_lag_7', 'footfall_rolling_mean_30']].head(10))

if __name__ == "__main__":
    main()
