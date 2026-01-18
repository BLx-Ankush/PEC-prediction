"""
Interactive Data Generator Panel
Allows full control over PEC data generation through a user-friendly interface
"""

import os
import sys
import json
from datetime import datetime
from src.data_generator import PECDataGenerator
import pandas as pd

class DataGeneratorPanel:
    """Interactive panel for managing PEC data generation"""
    
    def __init__(self):
        self.generator = PECDataGenerator()
        self.config_file = 'data_generator_config.json'
        self.load_config()
    
    def load_config(self):
        """Load saved configuration if exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.generator.pincodes = config.get('pincodes', self.generator.pincodes)
                    self.generator.holidays = config.get('holidays', self.generator.holidays)
                print("✅ Loaded saved configuration")
            except:
                print("⚠️  Using default configuration")
    
    def save_config(self):
        """Save current configuration"""
        config = {
            'pincodes': self.generator.pincodes,
            'holidays': self.generator.holidays
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration saved!")
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Display panel header"""
        self.clear_screen()
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 20 + "PEC DATA GENERATOR PANEL" + " " * 34 + "║")
        print("╚" + "=" * 78 + "╝")
        print()
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.show_header()
            print("📊 MAIN MENU")
            print("-" * 80)
            print("1.  📍 Manage PIN Codes (View/Add/Edit/Delete)")
            print("2.  🎉 Manage Holidays")
            print("3.  📅 Generate Data")
            print("4.  📋 View Current Configuration")
            print("5.  💾 Save Configuration")
            print("6.  📂 Load Configuration")
            print("7.  🔄 Reset to Default")
            print("8.  📊 Quick Statistics")
            print("9.  🚪 Exit")
            print("-" * 80)
            
            choice = input("\n👉 Enter your choice (1-9): ").strip()
            
            if choice == '1':
                self.manage_pincodes_menu()
            elif choice == '2':
                self.manage_holidays_menu()
            elif choice == '3':
                self.generate_data_menu()
            elif choice == '4':
                self.view_configuration()
            elif choice == '5':
                self.save_config()
                input("\nPress Enter to continue...")
            elif choice == '6':
                self.load_config()
                input("\nPress Enter to continue...")
            elif choice == '7':
                self.reset_to_default()
            elif choice == '8':
                self.show_statistics()
            elif choice == '9':
                print("\n👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice! Please try again.")
                input("\nPress Enter to continue...")
    
    def manage_pincodes_menu(self):
        """PIN code management submenu"""
        while True:
            self.show_header()
            print("📍 PIN CODE MANAGEMENT")
            print("-" * 80)
            print("1. View All PIN Codes")
            print("2. Add New PIN Code")
            print("3. Edit PIN Code")
            print("4. Delete PIN Code")
            print("5. Bulk Import PIN Codes (CSV)")
            print("6. Export PIN Codes (CSV)")
            print("7. Back to Main Menu")
            print("-" * 80)
            
            choice = input("\n👉 Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.view_pincodes()
            elif choice == '2':
                self.add_pincode()
            elif choice == '3':
                self.edit_pincode()
            elif choice == '4':
                self.delete_pincode()
            elif choice == '5':
                self.bulk_import_pincodes()
            elif choice == '6':
                self.export_pincodes()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
    
    def view_pincodes(self):
        """Display all configured PIN codes"""
        self.show_header()
        print("📍 CONFIGURED PIN CODES")
        print("-" * 80)
        
        # Convert to DataFrame for better display
        data = []
        for pin, info in sorted(self.generator.pincodes.items()):
            data.append({
                'PIN Code': pin,
                'District': info['district'],
                'State': info['state'],
                'Type': info['type'],
                'Base Footfall': info['base_footfall']
            })
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        
        print(f"\n📊 Total PIN Codes: {len(self.generator.pincodes)}")
        print(f"🏙️  Urban: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Urban')}")
        print(f"🌾 Rural: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Rural')}")
        print(f"🏘️  Semi-Urban: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Semi-Urban')}")
        
        input("\nPress Enter to continue...")
    
    def add_pincode(self):
        """Add a new PIN code"""
        self.show_header()
        print("➕ ADD NEW PIN CODE")
        print("-" * 80)
        
        pincode = input("Enter PIN Code (6 digits): ").strip()
        
        if pincode in self.generator.pincodes:
            print(f"❌ PIN Code {pincode} already exists!")
            input("\nPress Enter to continue...")
            return
        
        if len(pincode) != 6 or not pincode.isdigit():
            print("❌ Invalid PIN code! Must be 6 digits.")
            input("\nPress Enter to continue...")
            return
        
        district = input("Enter District: ").strip()
        state = input("Enter State: ").strip()
        
        print("\nCenter Type:")
        print("1. Urban")
        print("2. Rural")
        print("3. Semi-Urban")
        type_choice = input("Choose type (1-3): ").strip()
        
        center_types = {'1': 'Urban', '2': 'Rural', '3': 'Semi-Urban'}
        center_type = center_types.get(type_choice, 'Urban')
        
        try:
            base_footfall = int(input("Enter Base Footfall (e.g., 150): ").strip())
        except ValueError:
            print("❌ Invalid footfall value! Using default 100.")
            base_footfall = 100
        
        self.generator.pincodes[pincode] = {
            'district': district,
            'state': state,
            'type': center_type,
            'base_footfall': base_footfall
        }
        
        print(f"\n✅ PIN Code {pincode} added successfully!")
        input("\nPress Enter to continue...")
    
    def edit_pincode(self):
        """Edit an existing PIN code"""
        self.show_header()
        print("✏️  EDIT PIN CODE")
        print("-" * 80)
        
        pincode = input("Enter PIN Code to edit: ").strip()
        
        if pincode not in self.generator.pincodes:
            print(f"❌ PIN Code {pincode} not found!")
            input("\nPress Enter to continue...")
            return
        
        info = self.generator.pincodes[pincode]
        print(f"\nCurrent Details:")
        print(f"District: {info['district']}")
        print(f"State: {info['state']}")
        print(f"Type: {info['type']}")
        print(f"Base Footfall: {info['base_footfall']}")
        
        print("\nLeave blank to keep current value")
        
        district = input(f"New District [{info['district']}]: ").strip()
        state = input(f"New State [{info['state']}]: ").strip()
        
        print("\nCenter Type:")
        print("1. Urban")
        print("2. Rural")
        print("3. Semi-Urban")
        type_choice = input(f"Choose type [{info['type']}] (1-3 or Enter): ").strip()
        
        footfall = input(f"New Base Footfall [{info['base_footfall']}]: ").strip()
        
        # Update only if new values provided
        if district:
            info['district'] = district
        if state:
            info['state'] = state
        if type_choice in ['1', '2', '3']:
            center_types = {'1': 'Urban', '2': 'Rural', '3': 'Semi-Urban'}
            info['type'] = center_types[type_choice]
        if footfall:
            try:
                info['base_footfall'] = int(footfall)
            except ValueError:
                print("⚠️  Invalid footfall, keeping current value")
        
        print(f"\n✅ PIN Code {pincode} updated successfully!")
        input("\nPress Enter to continue...")
    
    def delete_pincode(self):
        """Delete a PIN code"""
        self.show_header()
        print("🗑️  DELETE PIN CODE")
        print("-" * 80)
        
        pincode = input("Enter PIN Code to delete: ").strip()
        
        if pincode not in self.generator.pincodes:
            print(f"❌ PIN Code {pincode} not found!")
            input("\nPress Enter to continue...")
            return
        
        info = self.generator.pincodes[pincode]
        print(f"\nPIN Code: {pincode}")
        print(f"District: {info['district']}, {info['state']}")
        
        confirm = input("\n⚠️  Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            del self.generator.pincodes[pincode]
            print(f"\n✅ PIN Code {pincode} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def bulk_import_pincodes(self):
        """Import PIN codes from CSV"""
        self.show_header()
        print("📥 BULK IMPORT PIN CODES")
        print("-" * 80)
        print("CSV Format: pincode,district,state,center_type,base_footfall")
        print("Example: 110001,Central Delhi,Delhi,Urban,180")
        print()
        
        file_path = input("Enter CSV file path: ").strip()
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            input("\nPress Enter to continue...")
            return
        
        try:
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                pincode = str(row['pincode']).strip()
                self.generator.pincodes[pincode] = {
                    'district': str(row['district']),
                    'state': str(row['state']),
                    'type': str(row['center_type']),
                    'base_footfall': int(row['base_footfall'])
                }
                count += 1
            
            print(f"\n✅ Imported {count} PIN codes successfully!")
        except Exception as e:
            print(f"❌ Error importing: {e}")
        
        input("\nPress Enter to continue...")
    
    def export_pincodes(self):
        """Export PIN codes to CSV"""
        self.show_header()
        print("📤 EXPORT PIN CODES")
        print("-" * 80)
        
        file_path = input("Enter output file path [pincodes_export.csv]: ").strip()
        if not file_path:
            file_path = 'pincodes_export.csv'
        
        data = []
        for pin, info in self.generator.pincodes.items():
            data.append({
                'pincode': pin,
                'district': info['district'],
                'state': info['state'],
                'center_type': info['type'],
                'base_footfall': info['base_footfall']
            })
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        
        print(f"\n✅ Exported {len(data)} PIN codes to {file_path}")
        input("\nPress Enter to continue...")
    
    def manage_holidays_menu(self):
        """Holiday management submenu"""
        while True:
            self.show_header()
            print("🎉 HOLIDAY MANAGEMENT")
            print("-" * 80)
            print("1. View All Holidays")
            print("2. Add Holiday")
            print("3. Delete Holiday")
            print("4. Import Holidays (CSV)")
            print("5. Export Holidays (CSV)")
            print("6. Back to Main Menu")
            print("-" * 80)
            
            choice = input("\n👉 Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.view_holidays()
            elif choice == '2':
                self.add_holiday()
            elif choice == '3':
                self.delete_holiday()
            elif choice == '4':
                self.import_holidays()
            elif choice == '5':
                self.export_holidays()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
    
    def view_holidays(self):
        """Display all holidays"""
        self.show_header()
        print("🎉 CONFIGURED HOLIDAYS")
        print("-" * 80)
        
        sorted_holidays = sorted(self.generator.holidays)
        
        for i, holiday in enumerate(sorted_holidays, 1):
            print(f"{i:3}. {holiday}")
        
        print(f"\n📊 Total Holidays: {len(self.generator.holidays)}")
        input("\nPress Enter to continue...")
    
    def add_holiday(self):
        """Add a new holiday"""
        self.show_header()
        print("➕ ADD HOLIDAY")
        print("-" * 80)
        
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            
            if date_str in self.generator.holidays:
                print(f"⚠️  Holiday {date_str} already exists!")
            else:
                self.generator.holidays.append(date_str)
                print(f"\n✅ Holiday {date_str} added successfully!")
        except ValueError:
            print("❌ Invalid date format! Use YYYY-MM-DD")
        
        input("\nPress Enter to continue...")
    
    def delete_holiday(self):
        """Delete a holiday"""
        self.show_header()
        print("🗑️  DELETE HOLIDAY")
        print("-" * 80)
        
        date_str = input("Enter date to delete (YYYY-MM-DD): ").strip()
        
        if date_str in self.generator.holidays:
            self.generator.holidays.remove(date_str)
            print(f"\n✅ Holiday {date_str} deleted successfully!")
        else:
            print(f"❌ Holiday {date_str} not found!")
        
        input("\nPress Enter to continue...")
    
    def import_holidays(self):
        """Import holidays from CSV"""
        self.show_header()
        print("📥 IMPORT HOLIDAYS")
        print("-" * 80)
        print("CSV Format: date")
        print("Example: 2025-01-26")
        print()
        
        file_path = input("Enter CSV file path: ").strip()
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            input("\nPress Enter to continue...")
            return
        
        try:
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                date_str = str(row['date']).strip()
                if date_str not in self.generator.holidays:
                    self.generator.holidays.append(date_str)
                    count += 1
            
            print(f"\n✅ Imported {count} holidays successfully!")
        except Exception as e:
            print(f"❌ Error importing: {e}")
        
        input("\nPress Enter to continue...")
    
    def export_holidays(self):
        """Export holidays to CSV"""
        self.show_header()
        print("📤 EXPORT HOLIDAYS")
        print("-" * 80)
        
        file_path = input("Enter output file path [holidays_export.csv]: ").strip()
        if not file_path:
            file_path = 'holidays_export.csv'
        
        df = pd.DataFrame({'date': sorted(self.generator.holidays)})
        df.to_csv(file_path, index=False)
        
        print(f"\n✅ Exported {len(self.generator.holidays)} holidays to {file_path}")
        input("\nPress Enter to continue...")
    
    def generate_data_menu(self):
        """Data generation menu"""
        self.show_header()
        print("📅 GENERATE DATA")
        print("-" * 80)
        
        print("Enter date range for data generation:")
        start_date = input("Start date (YYYY-MM-DD) [2025-01-01]: ").strip()
        if not start_date:
            start_date = '2025-01-01'
        
        end_date = input("End date (YYYY-MM-DD) [2026-01-31]: ").strip()
        if not end_date:
            end_date = '2026-01-31'
        
        output_dir = input("Output directory [data/raw]: ").strip()
        if not output_dir:
            output_dir = 'data/raw'
        
        print("\n" + "=" * 80)
        print("📊 Generation Summary:")
        print(f"Date Range: {start_date} to {end_date}")
        print(f"PIN Codes: {len(self.generator.pincodes)}")
        print(f"Output: {output_dir}/pec_footfall_data.csv")
        print("=" * 80)
        
        confirm = input("\n🚀 Generate data? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print("\n⏳ Generating data...\n")
            try:
                df = self.generator.generate_footfall_data(start_date, end_date, output_dir)
                print("\n✨ Data generation complete!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n❌ Generation cancelled.")
        
        input("\nPress Enter to continue...")
    
    def view_configuration(self):
        """View current configuration"""
        self.show_header()
        print("📋 CURRENT CONFIGURATION")
        print("-" * 80)
        
        print(f"📍 Total PIN Codes: {len(self.generator.pincodes)}")
        print(f"   - Urban: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Urban')}")
        print(f"   - Rural: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Rural')}")
        print(f"   - Semi-Urban: {sum(1 for p in self.generator.pincodes.values() if p['type'] == 'Semi-Urban')}")
        
        print(f"\n🎉 Total Holidays: {len(self.generator.holidays)}")
        
        print(f"\n📊 Base Footfall Range:")
        footfalls = [info['base_footfall'] for info in self.generator.pincodes.values()]
        if footfalls:
            print(f"   - Minimum: {min(footfalls)}")
            print(f"   - Maximum: {max(footfalls)}")
            print(f"   - Average: {sum(footfalls) / len(footfalls):.1f}")
        
        input("\nPress Enter to continue...")
    
    def reset_to_default(self):
        """Reset to default configuration"""
        self.show_header()
        print("🔄 RESET TO DEFAULT")
        print("-" * 80)
        
        confirm = input("⚠️  This will erase all custom changes. Continue? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.generator = PECDataGenerator()
            print("\n✅ Configuration reset to default!")
        else:
            print("\n❌ Reset cancelled.")
        
        input("\nPress Enter to continue...")
    
    def show_statistics(self):
        """Show quick statistics"""
        self.show_header()
        print("📊 QUICK STATISTICS")
        print("-" * 80)
        
        # Calculate estimated records
        start = datetime(2025, 1, 1)
        end = datetime(2026, 1, 31)
        days = (end - start).days + 1
        total_records = len(self.generator.pincodes) * days
        
        print(f"📅 Days per year: 365")
        print(f"📍 Configured PECs: {len(self.generator.pincodes)}")
        print(f"📊 Estimated records (1 year): {len(self.generator.pincodes) * 365:,}")
        print(f"📊 Estimated records (13 months): {total_records:,}")
        
        print(f"\n🎉 Configured holidays: {len(self.generator.holidays)}")
        print(f"📈 Average holiday impact: ~80% footfall reduction")
        
        print("\n🏙️  Center Type Distribution:")
        for center_type in ['Urban', 'Rural', 'Semi-Urban']:
            count = sum(1 for p in self.generator.pincodes.values() if p['type'] == center_type)
            percent = (count / len(self.generator.pincodes) * 100) if self.generator.pincodes else 0
            print(f"   - {center_type}: {count} ({percent:.1f}%)")
        
        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    panel = DataGeneratorPanel()
    panel.main_menu()


if __name__ == "__main__":
    main()
