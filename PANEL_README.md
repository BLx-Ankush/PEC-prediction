# 🎛️ Data Generator Panel - Quick Reference

## 🚀 Launch Panel

### Option 1: Direct Launch
```powershell
python data_generator_panel.py
```

### Option 2: From Main Menu
```powershell
python menu.py
# Select option 15
```

---

## 📁 Included Sample Files

### `sample_pincodes_import.csv`
- **Purpose:** Example bulk import template
- **Contains:** 50 PIN codes across India
- **Mix:** Urban, Rural, and Semi-Urban centers
- **Usage:** Panel → Manage PIN Codes → Bulk Import

### `sample_holidays_import.csv`
- **Purpose:** Indian national holidays template
- **Contains:** 2025-2026 holiday dates
- **Usage:** Panel → Manage Holidays → Import

---

## 🎯 Quick Actions

| What You Want | How To Do It |
|---------------|--------------|
| **See all locations** | Option 1 → 1 |
| **Add one PIN code** | Option 1 → 2 |
| **Add many PIN codes** | Option 1 → 5 (use sample_pincodes_import.csv) |
| **Edit location details** | Option 1 → 3 |
| **Remove location** | Option 1 → 4 |
| **Add holidays** | Option 2 → 4 (use sample_holidays_import.csv) |
| **Generate data** | Option 3 |
| **Save your setup** | Option 5 |
| **Reset to default** | Option 7 |

---

## 📊 Panel Features

### 1. Manage PIN Codes (Option 1)
- View all configured locations
- Add/Edit/Delete individual PIN codes
- Bulk import from CSV (50+ locations at once)
- Export current setup to CSV

### 2. Manage Holidays (Option 2)
- View all configured holidays
- Add/Delete specific dates
- Import holidays from CSV
- Export for backup

### 3. Generate Data (Option 3)
- Set custom date ranges
- Choose output directory
- Generates realistic synthetic data
- Shows generation statistics

### 4. View Configuration (Option 4)
- Quick overview of current setup
- Center type distribution
- Footfall statistics
- Holiday count

### 5. Save Configuration (Option 5)
- Saves to `data_generator_config.json`
- Preserves all customizations
- Auto-loads next time

### 6. Load Configuration (Option 6)
- Restore from saved file
- Useful after reset

### 7. Reset to Default (Option 7)
- Restores original 20 PIN codes
- Resets holidays
- Requires confirmation

### 8. Quick Statistics (Option 8)
- Estimated data size
- Center type breakdown
- Footfall ranges

### 9. Exit (Option 9)
- Returns to main menu (if launched from menu)
- Exits completely (if launched directly)

---

## 💡 Example Workflow

### Scenario: Create dataset for 50 locations

**Step 1:** Launch panel
```powershell
python data_generator_panel.py
```

**Step 2:** Import PIN codes
```
→ 1 (Manage PIN Codes)
→ 5 (Bulk Import)
→ Enter: sample_pincodes_import.csv
```

**Step 3:** Import holidays
```
→ 2 (Manage Holidays)
→ 4 (Import Holidays)
→ Enter: sample_holidays_import.csv
```

**Step 4:** Review setup
```
→ 4 (View Configuration)
```

**Step 5:** Generate data
```
→ 3 (Generate Data)
→ Start: 2024-01-01
→ End: 2026-12-31
→ Output: data/raw
→ yes (confirm)
```

**Result:**
- 50 locations × 1,096 days = 54,800 records!
- Saved to `data/raw/pec_footfall_data.csv`

**Step 6:** Save configuration
```
→ 5 (Save Configuration)
```

---

## 📋 Data Format

### Generated CSV Output
```csv
date,pincode,district,state,center_type,footfall
2024-01-01,110001,Central Delhi,Delhi,Urban,189
2024-01-01,400001,Mumbai City,Maharashtra,Urban,234
...
```

### Configuration Backup
Location: `data_generator_config.json`
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
  "holidays": ["2025-01-26", ...]
}
```

---

## 🎨 Customization Tips

### Base Footfall Guidelines
- **Major Urban:** 180-220
- **Urban:** 115-180
- **Semi-Urban:** 95-115
- **Rural:** 75-100

### Center Type Impact
- **Urban:** Lower weekend footfall, consistent patterns
- **Rural:** Higher variance, strong November pension spike
- **Semi-Urban:** Balanced characteristics

---

## 🐛 Troubleshooting

**Panel won't start:**
```powershell
pip install pandas numpy
```

**Import fails:**
- Check CSV format matches templates
- No extra columns allowed
- Verify numeric values

**"File not found" during import:**
- Use full path: `D:\ALICE(NEW)\New folder\sample_pincodes_import.csv`
- Or relative: `sample_pincodes_import.csv` (from project root)

---

## 🔗 Next Steps

After generating data:

1. **Engineer Features:**
   ```powershell
   python menu.py → Option 2
   ```

2. **Train Model:**
   ```powershell
   python menu.py → Option 3
   ```

3. **Make Predictions:**
   ```powershell
   python menu.py → Option 4-7
   ```

---

## 📚 Full Documentation

See [DATA_GENERATOR_PANEL_GUIDE.md](DATA_GENERATOR_PANEL_GUIDE.md) for:
- Complete feature explanations
- Advanced customization
- Seasonal pattern details
- Team collaboration workflows

---

**Quick Help:**
- Press `Ctrl+C` to interrupt (returns to main menu)
- All changes require saving (Option 5)
- Configuration auto-loads on next launch
- Generated data overwrites existing files

---

**Version:** 1.0  
**Last Updated:** January 18, 2026
