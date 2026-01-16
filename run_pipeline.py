"""
Master Pipeline Script
Runs the complete end-to-end PEC demand forecasting pipeline
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import PECDataGenerator
from feature_engineering import FeatureEngineer
from train_model import PECDemandModel
from visualizations.demand_heatmap import DemandHeatmapGenerator
from visualizations.trend_analysis import TrendAnalyzer

def run_complete_pipeline():
    """Execute the complete forecasting pipeline"""
    
    print("=" * 70)
    print(" PEC DEMAND FORECASTING - COMPLETE PIPELINE")
    print(" UIDAI Data Hackathon 2026")
    print("=" * 70)
    
    # Step 1: Generate Data
    print("\n" + "=" * 70)
    print("STEP 1: GENERATING SYNTHETIC PEC FOOTFALL DATA")
    print("=" * 70)
    generator = PECDataGenerator()
    df_raw = generator.generate_footfall_data()
    
    # Step 2: Feature Engineering
    print("\n" + "=" * 70)
    print("STEP 2: FEATURE ENGINEERING")
    print("=" * 70)
    engineer = FeatureEngineer()
    df_features = engineer.engineer_features()
    
    # Step 3: Train Model
    print("\n" + "=" * 70)
    print("STEP 3: TRAINING XGBOOST MODEL")
    print("=" * 70)
    trainer = PECDemandModel()
    model = trainer.train_model()
    
    # Step 4: Generate Visualizations
    print("\n" + "=" * 70)
    print("STEP 4: GENERATING VISUALIZATIONS")
    print("=" * 70)
    
    print("\n📊 Creating heatmaps...")
    heatmap_gen = DemandHeatmapGenerator()
    heatmap_gen.create_weekly_heatmap()
    heatmap_gen.create_district_comparison()
    heatmap_gen.create_urban_rural_comparison()
    
    print("\n📈 Creating trend analyses...")
    trend_analyzer = TrendAnalyzer()
    trend_analyzer.analyze_day_of_week_pattern()
    trend_analyzer.analyze_holiday_impact()
    trend_analyzer.analyze_seasonal_trends()
    trend_analyzer.create_comprehensive_dashboard()
    
    # Final Summary
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 70)
    
    print("\n📁 Generated Files:")
    print("  Data:")
    print("    └─ data/raw/pec_footfall_data.csv")
    print("    └─ data/processed/pec_features.csv")
    print("\n  Models:")
    print("    └─ models/pec_demand_model.json")
    print("    └─ models/model_metadata.pkl")
    print("    └─ models/feature_importance.png")
    print("    └─ models/predictions_vs_actual.png")
    print("\n  Visualizations:")
    print("    └─ visualizations/output/demand_heatmap_*.png")
    print("    └─ visualizations/output/district_comparison_*.png")
    print("    └─ visualizations/output/urban_rural_comparison.png")
    print("    └─ visualizations/output/day_of_week_pattern.png")
    print("    └─ visualizations/output/holiday_impact.png")
    print("    └─ visualizations/output/seasonal_trends.png")
    print("    └─ visualizations/output/comprehensive_dashboard.png")
    
    print("\n🔮 Making Predictions:")
    print("  Single day:  python src/predict.py --pincode 110001 --date 2026-03-15")
    print("  Weekly:      python src/predict.py --pincode 562157 --week 2026-03-10")
    print("  Monthly:     python src/predict.py --pincode 400001 --month 6 --year 2026")
    
    print("\n🏆 READY FOR UIDAI HACKATHON SUBMISSION!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        run_complete_pipeline()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
