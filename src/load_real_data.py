"""
UIDAI Real Data Adapter
Converts UIDAI raw data format to the format expected by the forecasting model
"""

import pandas as pd
import os

def load_uidai_data(uidai_file_path, output_path='data/raw/pec_footfall_data.csv'):
    """
    Load and transform UIDAI data to expected format
    
    Args:
        uidai_file_path: Path to UIDAI raw data file (CSV/Excel/JSON)
        output_path: Where to save transformed data
        
    Expected UIDAI columns (modify as per actual UIDAI data):
        - visit_date / transaction_date / date
        - center_pincode / pin_code / pincode
        - center_district / district
        - center_state / state
        - center_category / type / center_type
        - total_enrollments / footfall / visitors
        
    Returns:
        Transformed DataFrame
    """
    
    print("📥 Loading UIDAI data...")
    print("=" * 60)
    
    # Load data (supports CSV, Excel, JSON)
    if uidai_file_path.endswith('.csv'):
        df = pd.read_csv(uidai_file_path)
    elif uidai_file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(uidai_file_path)
    elif uidai_file_path.endswith('.json'):
        df = pd.read_json(uidai_file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV, Excel, or JSON")
    
    print(f"✅ Loaded {len(df):,} records")
    print(f"📊 Columns: {list(df.columns)}")
    
    # ============================================
    # COLUMN MAPPING - MODIFY THIS SECTION
    # Map UIDAI column names to expected names
    # ============================================
    
    column_mapping = {
        # UIDAI column name : Expected column name
        'visit_date': 'date',              # Or 'transaction_date', 'enrollment_date'
        'center_pincode': 'pincode',       # Or 'pin_code', 'postal_code'
        'center_district': 'district',     # Or 'district_name'
        'center_state': 'state',           # Or 'state_name'
        'center_category': 'center_type',  # Or 'type', 'category'
        'total_enrollments': 'footfall',   # Or 'visitors', 'transactions'
    }
    
    # Rename columns
    df = df.rename(columns=column_mapping)
    
    # ============================================
    # DATA TRANSFORMATIONS
    # ============================================
    
    # 1. Ensure date is in YYYY-MM-DD format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # 2. Ensure pincode is string with leading zeros
    df['pincode'] = df['pincode'].astype(str).str.zfill(6)
    
    # 3. Standardize center_type values
    # UIDAI might use different labels - map them
    center_type_mapping = {
        'URBAN': 'Urban',
        'RURAL': 'Rural',
        'SEMI_URBAN': 'Semi-Urban',
        'SEMI-URBAN': 'Semi-Urban',
        'U': 'Urban',
        'R': 'Rural',
        'SU': 'Semi-Urban',
        # Add more mappings as needed
    }
    
    df['center_type'] = df['center_type'].str.upper().map(center_type_mapping)
    df['center_type'] = df['center_type'].fillna('Urban')  # Default to Urban if unknown
    
    # 4. Clean district and state names
    df['district'] = df['district'].str.strip().str.title()
    df['state'] = df['state'].str.strip().str.title()
    
    # 5. Aggregate by date + pincode (in case of multiple entries per day)
    df = df.groupby(['date', 'pincode', 'district', 'state', 'center_type'], as_index=False).agg({
        'footfall': 'sum'
    })
    
    # ============================================
    # DATA QUALITY CHECKS
    # ============================================
    
    print("\n🔍 Data Quality Checks:")
    print("-" * 60)
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print("⚠️  Missing values detected:")
        print(missing[missing > 0])
    else:
        print("✅ No missing values")
    
    # Check date range
    df_dates = pd.to_datetime(df['date'])
    print(f"📅 Date range: {df_dates.min()} to {df_dates.max()}")
    print(f"📅 Total days: {(df_dates.max() - df_dates.min()).days + 1}")
    
    # Check PIN codes
    print(f"📍 Unique PIN codes: {df['pincode'].nunique()}")
    print(f"📍 Sample PINs: {', '.join(df['pincode'].unique()[:5].tolist())}")
    
    # Check footfall distribution
    print(f"👥 Footfall range: {df['footfall'].min()} to {df['footfall'].max()}")
    print(f"👥 Average footfall: {df['footfall'].mean():.0f}")
    
    # Check center types
    print(f"🏢 Center types: {df['center_type'].value_counts().to_dict()}")
    
    # ============================================
    # MINIMUM DATA REQUIREMENTS
    # ============================================
    
    # Check if we have enough data for training
    min_days = 60  # Need at least 60 days for lag features
    actual_days = df_dates.nunique()
    
    if actual_days < min_days:
        print(f"\n⚠️  WARNING: Only {actual_days} days of data found.")
        print(f"   Model requires at least {min_days} days for accurate lag features.")
        print(f"   Predictions may be less accurate.")
    
    # ============================================
    # SAVE PROCESSED DATA
    # ============================================
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Data transformation complete!")
    print(f"📁 Saved to: {output_path}")
    print(f"📊 Final dataset: {len(df):,} records")
    
    return df

def validate_data_for_modeling(data_path='data/raw/pec_footfall_data.csv'):
    """
    Validate that the data meets modeling requirements
    
    Args:
        data_path: Path to transformed data
        
    Returns:
        True if valid, False otherwise
    """
    
    print("\n🔬 Validating data for modeling...")
    print("=" * 60)
    
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    issues = []
    
    # Check 1: Required columns
    required_cols = ['date', 'pincode', 'district', 'state', 'center_type', 'footfall']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")
    
    # Check 2: Data coverage per PIN
    pin_coverage = df.groupby('pincode')['date'].nunique()
    low_coverage_pins = pin_coverage[pin_coverage < 30].index.tolist()
    if low_coverage_pins:
        issues.append(f"{len(low_coverage_pins)} PINs have <30 days of data")
    
    # Check 3: Recent data availability
    latest_date = df['date'].max()
    data_age = (pd.Timestamp.now() - latest_date).days
    if data_age > 90:
        issues.append(f"Latest data is {data_age} days old (may affect predictions)")
    
    # Check 4: Negative footfall
    if (df['footfall'] < 0).any():
        issues.append("Negative footfall values found")
    
    # Print results
    if issues:
        print("⚠️  Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n⚠️  Data may work but predictions could be less accurate")
        return False
    else:
        print("✅ All validation checks passed!")
        print("✅ Data is ready for model training")
        return True

# ============================================
# USAGE EXAMPLES
# ============================================

def example_usage():
    """Show how to use this adapter"""
    
    print("=" * 60)
    print("EXAMPLE USAGE - UIDAI Data Adapter")
    print("=" * 60)
    
    print("""
    # Example 1: Load from CSV
    from src.load_real_data import load_uidai_data
    
    df = load_uidai_data(
        uidai_file_path='path/to/uidai_raw_data.csv',
        output_path='data/raw/pec_footfall_data.csv'
    )
    
    # Example 2: Validate before training
    from src.load_real_data import validate_data_for_modeling
    
    is_valid = validate_data_for_modeling('data/raw/pec_footfall_data.csv')
    
    if is_valid:
        # Proceed with training
        from src.feature_engineering import FeatureEngineer
        engineer = FeatureEngineer()
        engineer.engineer_features()
    """)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("UIDAI Real Data Adapter")
        print("=" * 60)
        print("\nUsage:")
        print("  python src/load_real_data.py <path_to_uidai_data.csv>")
        print("\nExample:")
        print("  python src/load_real_data.py C:/Downloads/uidai_footfall_2025.csv")
        print("\n" + "=" * 60)
        example_usage()
    else:
        uidai_file = sys.argv[1]
        
        # Load and transform
        df = load_uidai_data(uidai_file)
        
        # Validate
        validate_data_for_modeling()
        
        print("\n✨ Ready for model training!")
        print("Next steps:")
        print("  1. python src/feature_engineering.py")
        print("  2. python src/train_model.py")
