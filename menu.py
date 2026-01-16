"""
Interactive Terminal Menu for PEC Demand Forecasting
Execute all functions through a user-friendly interface
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    clear_screen()
    print("=" * 70)
    print(" 🏛️  PEC DEMAND FORECASTING SYSTEM")
    print(" UIDAI Data Hackathon 2026")
    print("=" * 70)
    print()

def print_menu():
    """Display main menu options"""
    print("📋 MAIN MENU")
    print("-" * 70)
    print()
    print("  DATA GENERATION & PROCESSING:")
    print("    1️⃣  Generate Synthetic PEC Footfall Data")
    print("    2️⃣  Engineer Features from Raw Data")
    print()
    print("  MODEL TRAINING & EVALUATION:")
    print("    3️⃣  Train XGBoost Forecasting Model")
    print("    🔬 Validate Model Robustness (For Jury)")
    print()
    print("  PREDICTIONS:")
    print("    4️⃣  Predict Single Day Footfall")
    print("    5️⃣  Predict Weekly Footfall")
    print("    6️⃣  Predict Monthly Footfall")
    print("    7️⃣  Compare Multiple PIN Codes")
    print()
    print("  VISUALIZATIONS:")
    print("    8️⃣  Generate Demand Heatmaps")
    print("    9️⃣  Generate Trend Analysis Charts")
    print("    🔟 Generate ALL Visualizations")
    print()
    print("  COMPLETE PIPELINE:")
    print("    11 Run Complete End-to-End Pipeline")
    print()
    print("  OTHER:")
    print("    12 View Available PIN Codes")
    print("    13 Check System Status")
    print()
    print("    14 🔬 Validate Model Robustness (For Jury Presentation)")
    print()
    print("    0️⃣  Exit")
    print()
    print("-" * 70)

def generate_data():
    """Execute data generation"""
    print_header()
    print("🔄 GENERATING SYNTHETIC PEC FOOTFALL DATA...")
    print("=" * 70)
    print()
    
    try:
        from data_generator import PECDataGenerator
        generator = PECDataGenerator()
        df = generator.generate_footfall_data()
        
        print()
        print("✅ Data generation completed successfully!")
        print(f"📁 File saved: data/raw/pec_footfall_data.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\n\nPress Enter to return to main menu...")

def engineer_features():
    """Execute feature engineering"""
    print_header()
    print("🔧 ENGINEERING FEATURES...")
    print("=" * 70)
    print()
    
    try:
        from feature_engineering import FeatureEngineer
        engineer = FeatureEngineer()
        df = engineer.engineer_features()
        
        print()
        print("✅ Feature engineering completed successfully!")
        print(f"📁 File saved: data/processed/pec_features.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def train_model():
    """Execute model training"""
    print_header()
    print("🤖 TRAINING XGBOOST MODEL...")
    print("=" * 70)
    print()
    
    try:
        from train_model import PECDemandModel
        trainer = PECDemandModel()
        model = trainer.train_model()
        
        print()
        print("✅ Model training completed successfully!")
        print(f"📁 Model saved: models/pec_demand_model.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def predict_single_day():
    """Make single day prediction"""
    print_header()
    print("🔮 PREDICT SINGLE DAY FOOTFALL")
    print("=" * 70)
    print()
    
    try:
        from predict import PECPredictor
        
        # Get user input
        pincode = input("Enter PIN Code (e.g., 110001): ").strip()
        date_str = input("Enter Date (YYYY-MM-DD, e.g., 2026-03-15): ").strip()
        
        print()
        print("⏳ Making prediction...")
        print()
        
        predictor = PECPredictor()
        prediction = predictor.predict_single_day(pincode, date_str)
        
        if prediction is not None:
            info = predictor.pincode_info.get(pincode, {})
            print()
            print("✅ PREDICTION RESULT:")
            print("-" * 70)
            print(f"  📍 PIN Code:         {pincode}")
            print(f"  🏙️  District:         {info.get('district', 'N/A')}, {info.get('state', 'N/A')}")
            print(f"  🏢 Center Type:      {info.get('center_type', 'N/A')}")
            print(f"  📅 Date:             {date_str}")
            print(f"  👥 Predicted:        {prediction:,} residents")
            print("-" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def predict_weekly():
    """Make weekly prediction"""
    print_header()
    print("🔮 PREDICT WEEKLY FOOTFALL")
    print("=" * 70)
    print()
    
    try:
        from predict import PECPredictor
        
        # Get user input
        pincode = input("Enter PIN Code (e.g., 110001): ").strip()
        start_date = input("Enter Start Date (YYYY-MM-DD, e.g., 2026-03-10): ").strip()
        
        print()
        print("⏳ Making weekly predictions...")
        print()
        
        predictor = PECPredictor()
        predictions = predictor.predict_week(pincode, start_date)
        
        if len(predictions) > 0:
            print()
            print("✅ WEEKLY FORECAST:")
            print("-" * 70)
            print(predictions.to_string(index=False))
            print("-" * 70)
            print(f"📊 Weekly Total:     {predictions['predicted_footfall'].sum():,} residents")
            print(f"📊 Daily Average:    {predictions['predicted_footfall'].mean():.0f} residents")
            print("-" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def predict_monthly():
    """Make monthly prediction"""
    print_header()
    print("🔮 PREDICT MONTHLY FOOTFALL")
    print("=" * 70)
    print()
    
    try:
        from predict import PECPredictor
        
        # Get user input
        pincode = input("Enter PIN Code (e.g., 110001): ").strip()
        year = int(input("Enter Year (e.g., 2026): ").strip())
        month = int(input("Enter Month (1-12): ").strip())
        
        print()
        print("⏳ Making monthly predictions...")
        print()
        
        predictor = PECPredictor()
        predictions = predictor.predict_month(pincode, year, month)
        
        if len(predictions) > 0:
            print()
            print("✅ MONTHLY FORECAST:")
            print("-" * 70)
            print(predictions.to_string(index=False))
            print("-" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def compare_pincodes():
    """Compare multiple PIN codes"""
    print_header()
    print("🔮 COMPARE MULTIPLE PIN CODES")
    print("=" * 70)
    print()
    
    try:
        from predict import PECPredictor
        
        # Get user input
        pincodes_str = input("Enter PIN Codes (comma-separated, e.g., 110001,400001,560001): ").strip()
        pincodes = [p.strip() for p in pincodes_str.split(',')]
        date_str = input("Enter Date (YYYY-MM-DD, e.g., 2026-03-15): ").strip()
        
        print()
        print("⏳ Comparing PIN codes...")
        print()
        
        predictor = PECPredictor()
        comparison = predictor.compare_pincodes(pincodes, date_str)
        
        if len(comparison) > 0:
            print()
            print("✅ COMPARISON RESULT:")
            print("-" * 70)
            print(comparison.to_string(index=False))
            print("-" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def generate_heatmaps():
    """Generate demand heatmaps"""
    print_header()
    print("🗺️  GENERATING DEMAND HEATMAPS...")
    print("=" * 70)
    print()
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'visualizations'))
        from demand_heatmap import DemandHeatmapGenerator
        
        generator = DemandHeatmapGenerator()
        
        print("Creating weekly heatmap...")
        generator.create_weekly_heatmap()
        
        print("\nCreating district comparison...")
        generator.create_district_comparison()
        
        print("\nCreating urban-rural comparison...")
        generator.create_urban_rural_comparison()
        
        print()
        print("✅ All heatmaps generated successfully!")
        print(f"📁 Files saved: visualizations/output/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def generate_trends():
    """Generate trend analysis charts"""
    print_header()
    print("📈 GENERATING TREND ANALYSIS CHARTS...")
    print("=" * 70)
    print()
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'visualizations'))
        from trend_analysis import TrendAnalyzer
        
        analyzer = TrendAnalyzer()
        
        print("Analyzing day-of-week patterns...")
        analyzer.analyze_day_of_week_pattern()
        
        print("\nAnalyzing holiday impacts...")
        analyzer.analyze_holiday_impact()
        
        print("\nAnalyzing seasonal trends...")
        analyzer.analyze_seasonal_trends()
        
        print("\nCreating comprehensive dashboard...")
        analyzer.create_comprehensive_dashboard()
        
        print()
        print("✅ All trend analyses generated successfully!")
        print(f"📁 Files saved: visualizations/output/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def generate_all_visualizations():
    """Generate all visualizations"""
    print_header()
    print("📊 GENERATING ALL VISUALIZATIONS...")
    print("=" * 70)
    print()
    
    generate_heatmaps()
    generate_trends()

def run_complete_pipeline():
    """Run complete end-to-end pipeline"""
    print_header()
    print("🚀 RUNNING COMPLETE PIPELINE...")
    print("=" * 70)
    print()
    
    confirm = input("This will run all steps (data generation → training → visualizations). Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("❌ Cancelled.")
        input("\n\nPress Enter to return to main menu...")
        return
    
    try:
        # Step 1: Generate Data
        print("\n" + "=" * 70)
        print("STEP 1/4: GENERATING DATA...")
        print("=" * 70)
        from data_generator import PECDataGenerator
        generator = PECDataGenerator()
        generator.generate_footfall_data()
        
        # Step 2: Engineer Features
        print("\n" + "=" * 70)
        print("STEP 2/4: ENGINEERING FEATURES...")
        print("=" * 70)
        from feature_engineering import FeatureEngineer
        engineer = FeatureEngineer()
        engineer.engineer_features()
        
        # Step 3: Train Model
        print("\n" + "=" * 70)
        print("STEP 3/4: TRAINING MODEL...")
        print("=" * 70)
        from train_model import PECDemandModel
        trainer = PECDemandModel()
        trainer.train_model()
        
        # Step 4: Generate Visualizations
        print("\n" + "=" * 70)
        print("STEP 4/4: GENERATING VISUALIZATIONS...")
        print("=" * 70)
        
        sys.path.append(os.path.join(os.path.dirname(__file__), 'visualizations'))
        from demand_heatmap import DemandHeatmapGenerator
        from trend_analysis import TrendAnalyzer
        
        heatmap_gen = DemandHeatmapGenerator()
        heatmap_gen.create_weekly_heatmap()
        heatmap_gen.create_district_comparison()
        heatmap_gen.create_urban_rural_comparison()
        
        trend_analyzer = TrendAnalyzer()
        trend_analyzer.analyze_day_of_week_pattern()
        trend_analyzer.analyze_holiday_impact()
        trend_analyzer.analyze_seasonal_trends()
        trend_analyzer.create_comprehensive_dashboard()
        
        print("\n" + "=" * 70)
        print("✅ COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
        print("=" * 70)
        print("\n🎉 All data generated, model trained, and visualizations created!")
        print("📁 Check the following directories:")
        print("   • data/raw/")
        print("   • data/processed/")
        print("   • models/")
        print("   • visualizations/output/")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def view_pincodes():
    """Display available PIN codes"""
    print_header()
    print("📍 AVAILABLE PIN CODES")
    print("=" * 70)
    print()
    
    pincodes = {
        '110001': {'district': 'Central Delhi', 'state': 'Delhi', 'type': 'Urban'},
        '400001': {'district': 'Mumbai City', 'state': 'Maharashtra', 'type': 'Urban'},
        '560001': {'district': 'Bangalore Urban', 'state': 'Karnataka', 'type': 'Urban'},
        '600001': {'district': 'Chennai', 'state': 'Tamil Nadu', 'type': 'Urban'},
        '700001': {'district': 'Kolkata', 'state': 'West Bengal', 'type': 'Urban'},
        '500001': {'district': 'Hyderabad', 'state': 'Telangana', 'type': 'Urban'},
        '411001': {'district': 'Pune', 'state': 'Maharashtra', 'type': 'Urban'},
        '380001': {'district': 'Ahmedabad', 'state': 'Gujarat', 'type': 'Urban'},
        '562157': {'district': 'Bangalore Rural', 'state': 'Karnataka', 'type': 'Rural'},
        '431001': {'district': 'Aurangabad', 'state': 'Maharashtra', 'type': 'Semi-Urban'},
        '226001': {'district': 'Lucknow', 'state': 'Uttar Pradesh', 'type': 'Urban'},
        '302001': {'district': 'Jaipur', 'state': 'Rajasthan', 'type': 'Urban'},
        '160001': {'district': 'Chandigarh', 'state': 'Chandigarh', 'type': 'Urban'},
        '682001': {'district': 'Ernakulam', 'state': 'Kerala', 'type': 'Urban'},
        '800001': {'district': 'Patna', 'state': 'Bihar', 'type': 'Urban'},
        '751001': {'district': 'Khordha', 'state': 'Odisha', 'type': 'Urban'},
        '641001': {'district': 'Coimbatore', 'state': 'Tamil Nadu', 'type': 'Urban'},
        '530001': {'district': 'Visakhapatnam', 'state': 'Andhra Pradesh', 'type': 'Urban'},
        '784001': {'district': 'Sonitpur', 'state': 'Assam', 'type': 'Semi-Urban'},
        '361001': {'district': 'Jamnagar', 'state': 'Gujarat', 'type': 'Semi-Urban'},
    }
    
    print(f"{'PIN Code':<12} {'District':<25} {'State':<20} {'Type':<12}")
    print("-" * 70)
    
    for pin, info in sorted(pincodes.items()):
        print(f"{pin:<12} {info['district']:<25} {info['state']:<20} {info['type']:<12}")
    
    print()
    print(f"Total: {len(pincodes)} PIN codes available")
    
    input("\n\nPress Enter to return to main menu...")

def check_status():
    """Check system status and file availability"""
    print_header()
    print("🔍 SYSTEM STATUS CHECK")
    print("=" * 70)
    print()
    
    # Check files
    files_to_check = [
        ('data/raw/pec_footfall_data.csv', 'Raw Data'),
        ('data/processed/pec_features.csv', 'Processed Features'),
        ('models/pec_demand_model.json', 'Trained Model'),
        ('models/model_metadata.pkl', 'Model Metadata'),
    ]
    
    print("📁 File Status:")
    print("-" * 70)
    
    for filepath, description in files_to_check:
        full_path = os.path.join(os.path.dirname(__file__), filepath)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            size_kb = size / 1024
            print(f"  ✅ {description:<25} {filepath:<40} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {description:<25} {filepath:<40} (Not Found)")
    
    print()
    print("📊 Visualization Status:")
    print("-" * 70)
    
    viz_dir = os.path.join(os.path.dirname(__file__), 'visualizations', 'output')
    if os.path.exists(viz_dir):
        viz_files = [f for f in os.listdir(viz_dir) if f.endswith('.png')]
        if viz_files:
            print(f"  ✅ {len(viz_files)} visualization(s) found")
            for vf in viz_files[:5]:  # Show first 5
                print(f"     • {vf}")
            if len(viz_files) > 5:
                print(f"     ... and {len(viz_files) - 5} more")
        else:
            print(f"  ❌ No visualizations found")
    else:
        print(f"  ❌ Visualization directory not found")
    
    print()
    print("💡 Recommendations:")
    print("-" * 70)
    
    raw_exists = os.path.exists(os.path.join(os.path.dirname(__file__), 'data/raw/pec_footfall_data.csv'))
    features_exist = os.path.exists(os.path.join(os.path.dirname(__file__), 'data/processed/pec_features.csv'))
    model_exists = os.path.exists(os.path.join(os.path.dirname(__file__), 'models/pec_demand_model.json'))
    
    if not raw_exists:
        print("  → Run 'Generate Synthetic Data' (Option 1)")
    if raw_exists and not features_exist:
        print("  → Run 'Engineer Features' (Option 2)")
    if features_exist and not model_exists:
        print("  → Run 'Train Model' (Option 3)")
    if model_exists:
        print("  ✅ System is fully operational! You can make predictions.")
    
    input("\n\nPress Enter to return to main menu...")

def validate_robustness():
    """Run model robustness validation for jury presentation"""
    print_header()
    print("🔬 MODEL ROBUSTNESS VALIDATION (FOR JURY PRESENTATION)")
    print("=" * 70)
    print()
    
    print("This validation demonstrates model performance across different scenarios:")
    print("  • Performance by center type (Urban/Rural/Semi-Urban)")
    print("  • Seasonal pattern accuracy")
    print("  • Day-of-week predictions")
    print("  • Edge case handling")
    print()
    
    confirm = input("This will generate a comprehensive validation report. Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        print("❌ Cancelled.")
        input("\n\nPress Enter to return to main menu...")
        return
    
    try:
        from validate_robustness import validate_model_robustness
        validate_model_robustness()
        
        print()
        print("=" * 70)
        print("✅ VALIDATION COMPLETE!")
        print("=" * 70)
        print()
        print("📊 Validation report generated:")
        print("   visualizations/output/validation_report.png")
        print()
        print("💡 Use this report in your jury presentation to prove:")
        print("   • Model works consistently across all center types")
        print("   • Predictions are operationally accurate")
        print("   • System handles edge cases and seasonal patterns")
        print()
        print("📖 See JURY_RESPONSE_STRATEGY.md for presentation tips")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n\nPress Enter to return to main menu...")

def main():
    """Main menu loop"""
    
    while True:
        print_header()
        print_menu()
        
        choice = input("Enter your choice (0-14): ").strip()
        
        if choice == '0':
            print_header()
            print("👋 Thank you for using PEC Demand Forecasting System!")
            print("🏆 Good luck with UIDAI Data Hackathon 2026!")
            print()
            sys.exit(0)
        
        elif choice == '1':
            generate_data()
        
        elif choice == '2':
            engineer_features()
        
        elif choice == '3':
            train_model()
        
        elif choice == '4':
            predict_single_day()
        
        elif choice == '5':
            predict_weekly()
        
        elif choice == '6':
            predict_monthly()
        
        elif choice == '7':
            compare_pincodes()
        
        elif choice == '8':
            generate_heatmaps()
        
        elif choice == '9':
            generate_trends()
        
        elif choice == '10':
            generate_all_visualizations()
        
        elif choice == '11':
            run_complete_pipeline()
        
        elif choice == '12':
            view_pincodes()
        
        elif choice == '13':
            check_status()
        
        elif choice == '14':
            validate_robustness()
        
        else:
            print()
            print("❌ Invalid choice. Please enter a number between 0 and 14.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
