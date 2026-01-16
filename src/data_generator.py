"""
PEC Footfall Data Generator
Generates synthetic but realistic Aadhaar center footfall data for model training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

class PECDataGenerator:
    """Generate synthetic PEC footfall data with realistic patterns"""
    
    def __init__(self):
        # Indian PIN codes (sample from different regions)
        self.pincodes = {
            '110001': {'district': 'Central Delhi', 'state': 'Delhi', 'type': 'Urban', 'base_footfall': 180},
            '400001': {'district': 'Mumbai City', 'state': 'Maharashtra', 'type': 'Urban', 'base_footfall': 220},
            '560001': {'district': 'Bangalore Urban', 'state': 'Karnataka', 'type': 'Urban', 'base_footfall': 200},
            '600001': {'district': 'Chennai', 'state': 'Tamil Nadu', 'type': 'Urban', 'base_footfall': 190},
            '700001': {'district': 'Kolkata', 'state': 'West Bengal', 'type': 'Urban', 'base_footfall': 175},
            '500001': {'district': 'Hyderabad', 'state': 'Telangana', 'type': 'Urban', 'base_footfall': 185},
            '411001': {'district': 'Pune', 'state': 'Maharashtra', 'type': 'Urban', 'base_footfall': 165},
            '380001': {'district': 'Ahmedabad', 'state': 'Gujarat', 'type': 'Urban', 'base_footfall': 170},
            '562157': {'district': 'Bangalore Rural', 'state': 'Karnataka', 'type': 'Rural', 'base_footfall': 85},
            '431001': {'district': 'Aurangabad', 'state': 'Maharashtra', 'type': 'Semi-Urban', 'base_footfall': 110},
            '226001': {'district': 'Lucknow', 'state': 'Uttar Pradesh', 'type': 'Urban', 'base_footfall': 160},
            '302001': {'district': 'Jaipur', 'state': 'Rajasthan', 'type': 'Urban', 'base_footfall': 155},
            '160001': {'district': 'Chandigarh', 'state': 'Chandigarh', 'type': 'Urban', 'base_footfall': 140},
            '682001': {'district': 'Ernakulam', 'state': 'Kerala', 'type': 'Urban', 'base_footfall': 135},
            '800001': {'district': 'Patna', 'state': 'Bihar', 'type': 'Urban', 'base_footfall': 125},
            '751001': {'district': 'Khordha', 'state': 'Odisha', 'type': 'Urban', 'base_footfall': 115},
            '641001': {'district': 'Coimbatore', 'state': 'Tamil Nadu', 'type': 'Urban', 'base_footfall': 145},
            '530001': {'district': 'Visakhapatnam', 'state': 'Andhra Pradesh', 'type': 'Urban', 'base_footfall': 130},
            '784001': {'district': 'Sonitpur', 'state': 'Assam', 'type': 'Semi-Urban', 'base_footfall': 95},
            '361001': {'district': 'Jamnagar', 'state': 'Gujarat', 'type': 'Semi-Urban', 'base_footfall': 100},
        }
        
        # Indian public holidays (2025-2026)
        self.holidays = [
            '2025-01-26', '2025-03-14', '2025-03-31', '2025-04-10', '2025-04-14',
            '2025-05-01', '2025-08-15', '2025-08-27', '2025-10-02', '2025-10-24',
            '2025-11-01', '2025-12-25',
            '2026-01-26', '2026-03-03', '2026-03-25', '2026-03-30', '2026-04-14',
            '2026-05-01', '2026-08-15', '2026-08-16', '2026-10-02', '2026-10-13',
            '2026-11-01', '2026-11-14', '2026-12-25'
        ]
        
    def generate_footfall_data(self, start_date='2025-01-01', end_date='2026-01-31', 
                               output_dir='data/raw'):
        """
        Generate synthetic footfall data with realistic patterns
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            output_dir: Directory to save the generated data
        """
        # Create date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate data for all PEC locations
        all_data = []
        
        for pincode, info in self.pincodes.items():
            for date in dates:
                footfall = self._calculate_footfall(date, pincode, info)
                
                record = {
                    'date': date.strftime('%Y-%m-%d'),
                    'pincode': pincode,
                    'district': info['district'],
                    'state': info['state'],
                    'center_type': info['type'],
                    'footfall': max(0, footfall)  # Ensure non-negative
                }
                
                all_data.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(all_data)
        
        # Save to CSV
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'pec_footfall_data.csv')
        df.to_csv(output_path, index=False)
        
        print(f"✅ Generated {len(df):,} records")
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"📍 PIN codes: {len(df['pincode'].unique())}")
        print(f"💾 Saved to: {output_path}")
        
        # Print summary statistics
        print("\n📊 Summary Statistics:")
        print(df.groupby('center_type')['footfall'].describe())
        
        return df
    
    def _calculate_footfall(self, date, pincode, info):
        """Calculate footfall for a specific date and location"""
        base = info['base_footfall']
        
        # 1. Day of week pattern (Monday peak, weekend low)
        day_multipliers = {
            0: 1.25,  # Monday (highest)
            1: 1.15,  # Tuesday
            2: 1.10,  # Wednesday
            3: 1.05,  # Thursday
            4: 1.00,  # Friday
            5: 0.70,  # Saturday (lower)
            6: 0.50   # Sunday (lowest)
        }
        day_mult = day_multipliers.get(date.weekday(), 1.0)
        
        # 2. Holiday effect (sharp drop on holiday, spike next day)
        is_holiday = date.strftime('%Y-%m-%d') in self.holidays
        if is_holiday:
            day_mult *= 0.20  # 80% drop on holidays
        else:
            # Check if yesterday was a holiday (spike effect)
            yesterday = (date - timedelta(days=1)).strftime('%Y-%m-%d')
            if yesterday in self.holidays:
                day_mult *= 1.40  # 40% spike after holiday
        
        # 3. Monthly patterns (seasonal effects)
        month_multipliers = {
            1: 0.95,   # January
            2: 0.90,   # February
            3: 1.00,   # March
            4: 1.15,   # April (new financial year, updates)
            5: 1.10,   # May
            6: 1.35,   # June (SCHOOL ENROLLMENT PEAK)
            7: 1.40,   # July (SCHOOL ENROLLMENT PEAK)
            8: 1.05,   # August
            9: 1.00,   # September
            10: 1.20,  # October (festival season, scheme registrations)
            11: 1.45,  # November (PENSION LIFE CERTIFICATE PEAK)
            12: 1.10   # December
        }
        month_mult = month_multipliers.get(date.month, 1.0)
        
        # 4. Special rural pattern for pension updates
        if info['type'] == 'Rural' and date.month == 11:
            month_mult *= 1.60  # Extra spike for rural pension updates
        
        # 5. Week of month pattern (first week often busy for monthly updates)
        week_of_month = (date.day - 1) // 7 + 1
        if week_of_month == 1:
            week_mult = 1.10
        elif week_of_month == 4:
            week_mult = 0.95  # Slight drop in last week
        else:
            week_mult = 1.00
        
        # 6. Urban vs Rural patterns
        if info['type'] == 'Urban':
            type_variance = np.random.normal(1.0, 0.15)  # Higher variance
        elif info['type'] == 'Rural':
            type_variance = np.random.normal(1.0, 0.25)  # More unpredictable
        else:  # Semi-Urban
            type_variance = np.random.normal(1.0, 0.18)
        
        # 7. Long-term trend (slight increase over time for Aadhaar updates)
        days_from_start = (date - pd.to_datetime('2025-01-01')).days
        trend = 1.0 + (days_from_start / 365) * 0.05  # 5% annual growth
        
        # Calculate final footfall
        footfall = base * day_mult * month_mult * week_mult * type_variance * trend
        
        # Add some noise
        noise = np.random.normal(0, base * 0.08)
        footfall += noise
        
        return int(round(footfall))

def main():
    """Main execution function"""
    print("🏛️  PEC Demand Forecasting - Data Generator")
    print("=" * 60)
    
    generator = PECDataGenerator()
    
    # Generate 13 months of data (Jan 2025 - Jan 2026)
    df = generator.generate_footfall_data(
        start_date='2025-01-01',
        end_date='2026-01-31'
    )
    
    print("\n✨ Data generation complete!")
    print("\n🔍 Sample records:")
    print(df.head(10))

if __name__ == "__main__":
    main()
