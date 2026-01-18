# 🎛️ Data Generator Panel Guide

## Quick Start

Run the panel directly:
```powershell
python data_generator_panel.py
```

Or access it from the main menu:
```powershell
python menu.py
# Choose option 15
```

---

## 📋 Panel Features

### 1. 📍 **Manage PIN Codes**
Control all PEC locations in your dataset:

#### View All PIN Codes
- See complete list of configured locations
- View district, state, type, and base footfall
- Summary statistics by center type

#### Add New PIN Code
```
Example:
PIN Code: 110022
District: North Delhi
State: Delhi
Type: Urban
Base Footfall: 165
```

#### Edit PIN Code
- Modify any existing location details
- Update district, state, type, or base footfall
- Leave blank to keep current values

#### Delete PIN Code
- Remove locations from dataset generation
- Confirmation required before deletion

#### Bulk Import (CSV)
Import multiple PIN codes at once:
```csv
pincode,district,state,center_type,base_footfall
110001,Central Delhi,Delhi,Urban,180
400001,Mumbai City,Maharashtra,Urban,220
```

#### Export (CSV)
- Save current configuration to CSV
- Share with team members
- Backup your setup

---

### 2. 🎉 **Manage Holidays**
Control holiday impact on footfall predictions:

#### View Holidays
- See all configured holidays
- Sorted chronologically
- Shows total count

#### Add Holiday
```
Format: YYYY-MM-DD
Example: 2026-01-26
```

#### Delete Holiday
- Remove specific dates
- Useful for adjusting to regional calendars

#### Import/Export
- CSV format for bulk operations
- One date per line

**Holiday Impact:**
- 80% footfall reduction on holidays
- 40% spike day after holidays
- Applies to all center types

---

### 3. 📅 **Generate Data**
Create synthetic datasets with custom parameters:

```
Start Date: 2025-01-01
End Date: 2026-12-31
Output Directory: data/raw
```

**Calculation:**
- Records = PIN Codes × Days
- Example: 20 PINs × 365 days = 7,300 records

**Generated Patterns:**
- Weekday variations (Monday peak, weekend low)
- Monthly seasonality (June-July school enrollment)
- November pension certificate peak
- Holiday effects
- Urban/Rural differences

---

### 4. 📋 **View Configuration**
Quick overview of current setup:
- Total PIN codes by type
- Total holidays
- Footfall statistics (min/max/avg)

---

### 5. 💾 **Save/Load Configuration**

#### Save Configuration
- Saves to `data_generator_config.json`
- Preserves PIN codes and holidays
- Auto-loads on next run

#### Load Configuration
- Restore previous setup
- Useful for team collaboration

#### Configuration File Format:
```json
{
  "pincodes": {
    "110001": {
      "district": "Central Delhi",
      "state": "Delhi",
      "type": "Urban",
      "base_footfall": 180
    }
  },
  "holidays": ["2025-01-26", "2025-08-15"]
}
```

---

### 6. 🔄 **Reset to Default**
- Restores original 20 PIN codes
- Resets to default holidays
- Requires confirmation

---

### 7. 📊 **Quick Statistics**
Estimated data size and distribution:
- Records per time period
- Center type distribution
- Holiday count
- Footfall ranges

---

## 🎯 Common Use Cases

### Adding New Regions
```
1. Choose: Manage PIN Codes → Add New PIN Code
2. Enter details for each location
3. Generate → Save configuration
```

### Extending Time Range
```
1. Choose: Generate Data
2. Set start_date to earlier date (e.g., 2024-01-01)
3. Set end_date to later date (e.g., 2027-12-31)
4. Generate
```

### Creating Regional Dataset
```
1. Delete unwanted PIN codes
2. Add region-specific PIN codes
3. Adjust holidays for region
4. Generate data
```

### Scaling Up Dataset
```
Current: 20 PINs × 13 months = 9,490 records

To scale:
1. Import CSV with 100+ PIN codes
2. Extend date range to 2+ years
3. Result: 100+ PINs × 730 days = 73,000+ records
```

---

## 📂 File Outputs

### Generated Data
**Location:** `data/raw/pec_footfall_data.csv`

**Format:**
```csv
date,pincode,district,state,center_type,footfall
2025-01-01,110001,Central Delhi,Delhi,Urban,189
2025-01-01,400001,Mumbai City,Maharashtra,Urban,234
```

### Configuration Backup
**Location:** `data_generator_config.json`

**Purpose:** 
- Preserve custom PIN codes
- Share with team
- Version control

---

## 🎨 Center Types & Base Footfall

### Urban Centers
- Base footfall: 115-220
- Higher variance (±15%)
- Steady weekday patterns
- Lower weekend footfall

### Rural Centers
- Base footfall: 85-100
- Higher variance (±25%)
- Strong pension spike in November
- More unpredictable patterns

### Semi-Urban Centers
- Base footfall: 95-110
- Medium variance (±18%)
- Balanced characteristics

---

## 📈 Seasonal Patterns

### Built-in Multipliers

**Monthly:**
- January: 0.95 (post-holiday low)
- April: 1.15 (financial year start)
- June-July: 1.35-1.40 (school enrollment peak)
- October: 1.20 (festival season)
- November: 1.45 (pension certificates)
- December: 1.10 (year-end updates)

**Weekly:**
- Monday: 1.25× (highest)
- Tuesday-Thursday: 1.05-1.15×
- Friday: 1.00×
- Saturday: 0.70× (lower)
- Sunday: 0.50× (lowest)

**Week of Month:**
- Week 1: 1.10× (monthly updates)
- Week 2-3: 1.00×
- Week 4: 0.95× (slight drop)

---

## 🔧 Advanced Customization

### Modifying Patterns
Edit `src/data_generator.py` to customize:
- Seasonal multipliers (lines 133-147)
- Day of week patterns (lines 121-129)
- Holiday impact (lines 132-140)
- Long-term trends (line 174)

### Custom Base Footfall Logic
```python
# Urban tier cities
if info['district'] in ['Mumbai City', 'Bangalore Urban']:
    info['base_footfall'] *= 1.20  # 20% higher
```

---

## 💡 Tips & Best Practices

### Data Quality
✅ **Do:**
- Use realistic base footfall values
- Include mix of urban/rural/semi-urban
- Cover multiple states for diversity
- Keep holidays updated for accuracy

❌ **Don't:**
- Use extremely high/low footfall values
- Forget to save configuration
- Generate overlapping date ranges
- Delete all PIN codes before generating

### Performance
- 20 PINs × 1 year = ~3 seconds
- 50 PINs × 2 years = ~10 seconds
- 100+ PINs × 2+ years = ~30 seconds

### Team Collaboration
1. Export your PIN codes to CSV
2. Share `data_generator_config.json`
3. Team members can import and use same setup
4. Version control the config file

---

## 🐛 Troubleshooting

### Panel won't start
```powershell
# Check dependencies
pip install pandas numpy

# Run directly
python data_generator_panel.py
```

### Import fails
- Check CSV format matches exactly
- Ensure no extra columns
- Verify numeric values for base_footfall

### Generated data looks wrong
1. View Configuration → check PIN codes
2. View Holidays → verify dates
3. Regenerate with correct settings

### File not found errors
- Run from project root directory
- Check `data/raw/` folder exists
- Panel auto-creates directories

---

## 🎓 Example Workflow

### Creating a Custom Dataset

**Step 1: Plan Your Dataset**
- Regions needed: Delhi, Mumbai, Bangalore
- Time period: 2 years (2024-2026)
- Centers: 30 locations

**Step 2: Configure PIN Codes**
```
Menu → 1 (Manage PIN Codes)
→ 2 (Add New PIN Code)
Add 30 PIN codes one by one
Or: 5 (Bulk Import) from CSV
```

**Step 3: Set Holidays**
```
Menu → 2 (Manage Holidays)
→ 4 (Import Holidays) from CSV
```

**Step 4: Generate**
```
Menu → 3 (Generate Data)
Start: 2024-01-01
End: 2026-12-31
Output: data/raw
→ yes (confirm)
```

**Step 5: Save Setup**
```
Menu → 5 (Save Configuration)
```

**Result:**
- 30 PINs × 730 days = 21,900 records
- Configuration saved for reuse
- Ready for feature engineering

---

## 📞 Integration with Pipeline

After generating custom data:

```powershell
python menu.py

# Option 2: Engineer Features
# Option 3: Train Model
# Options 4-7: Make Predictions
```

The entire pipeline automatically uses your custom-generated data!

---

## 🚀 Quick Reference Commands

| Task | Command |
|------|---------|
| Start Panel | `python data_generator_panel.py` |
| Quick Generate | `python src/data_generator.py` |
| From Main Menu | `python menu.py` → Option 15 |
| Export Config | Panel → Option 5 |
| Bulk Add PINs | Panel → Option 1 → Option 5 |
| Reset Everything | Panel → Option 7 |

---

## 📚 Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [REAL_DATA_GUIDE.md](REAL_DATA_GUIDE.md) - Using actual UIDAI data
- [README.md](README.md) - Project overview

---

**Last Updated:** January 18, 2026
**Version:** 1.0
