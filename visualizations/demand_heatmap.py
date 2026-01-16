"""
Demand Heatmap Visualization
Create geographic heatmaps of predicted PEC demand
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

class DemandHeatmapGenerator:
    """Generate demand heatmaps for strategic planning"""
    
    def create_weekly_heatmap(self, data_path='data/processed/pec_features.csv',
                             start_date=None, output_dir='visualizations/output'):
        """
        Create a heatmap showing demand across PINs for a week
        
        Args:
            data_path: Path to features CSV
            start_date: Start date (YYYY-MM-DD), defaults to latest available
            output_dir: Directory to save visualization
        """
        print("🗺️  Generating Weekly Demand Heatmap...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Use latest week if no date provided
        if start_date is None:
            start_date = df['date'].max() - timedelta(days=6)
        else:
            start_date = pd.to_datetime(start_date)
        
        end_date = start_date + timedelta(days=6)
        
        # Filter to date range
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        week_df = df[mask].copy()
        
        if len(week_df) == 0:
            print(f"❌ No data found for date range {start_date.date()} to {end_date.date()}")
            return
        
        print(f"📅 Date range: {start_date.date()} to {end_date.date()}")
        print(f"📊 Records: {len(week_df):,}")
        
        # Pivot for heatmap: rows=PINs, columns=days
        week_df['day_name'] = week_df['date'].dt.strftime('%a %m/%d')
        pivot = week_df.pivot_table(
            index='pincode',
            columns='day_name',
            values='footfall',
            aggfunc='mean'
        )
        
        # Sort by average demand (highest first)
        pivot['avg_demand'] = pivot.mean(axis=1)
        pivot = pivot.sort_values('avg_demand', ascending=False).drop('avg_demand', axis=1)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create heatmap
        sns.heatmap(
            pivot,
            annot=True,
            fmt='.0f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Footfall (residents)'},
            linewidths=0.5,
            linecolor='gray',
            ax=ax
        )
        
        plt.title(
            f'PEC Demand Heatmap: {start_date.strftime("%b %d")} - {end_date.strftime("%b %d, %Y")}',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        plt.xlabel('Day', fontsize=12, fontweight='bold')
        plt.ylabel('PIN Code', fontsize=12, fontweight='bold')
        plt.tight_layout()
        
        # Save
        os.makedirs(output_dir, exist_ok=True)
        filename = f"demand_heatmap_{start_date.strftime('%Y%m%d')}.png"
        save_path = os.path.join(output_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✅ Heatmap saved to: {save_path}")
        
        # Print insights
        self._print_insights(pivot)
    
    def create_district_comparison(self, data_path='data/processed/pec_features.csv',
                                  date_str=None, output_dir='visualizations/output'):
        """
        Compare demand across districts for a specific date
        
        Args:
            data_path: Path to features CSV
            date_str: Date (YYYY-MM-DD), defaults to latest
            output_dir: Directory to save visualization
        """
        print("\n🏙️  Generating District Comparison...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Use latest date if not provided
        if date_str is None:
            target_date = df['date'].max()
        else:
            target_date = pd.to_datetime(date_str)
        
        # Filter to specific date
        day_df = df[df['date'] == target_date].copy()
        
        if len(day_df) == 0:
            print(f"❌ No data found for {target_date.date()}")
            return
        
        print(f"📅 Date: {target_date.date()}")
        
        # Aggregate by district
        district_stats = day_df.groupby('district').agg({
            'footfall': ['sum', 'mean', 'max'],
            'pincode': 'count'
        }).reset_index()
        
        district_stats.columns = ['district', 'total_footfall', 'avg_footfall', 'max_footfall', 'num_centers']
        district_stats = district_stats.sort_values('total_footfall', ascending=False)
        
        # Create bar chart
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Total footfall by district
        axes[0].barh(district_stats['district'], district_stats['total_footfall'], color='#2E86AB')
        axes[0].set_xlabel('Total Footfall', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('District', fontsize=12, fontweight='bold')
        axes[0].set_title('Total Footfall by District', fontsize=14, fontweight='bold')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Average footfall per center
        axes[1].barh(district_stats['district'], district_stats['avg_footfall'], color='#A23B72')
        axes[1].set_xlabel('Average Footfall per Center', fontsize=12, fontweight='bold')
        axes[1].set_title('Average Demand per PEC', fontsize=14, fontweight='bold')
        axes[1].grid(axis='x', alpha=0.3)
        
        plt.suptitle(
            f'District-wise PEC Demand Comparison - {target_date.strftime("%B %d, %Y")}',
            fontsize=16,
            fontweight='bold',
            y=1.00
        )
        plt.tight_layout()
        
        # Save
        os.makedirs(output_dir, exist_ok=True)
        filename = f"district_comparison_{target_date.strftime('%Y%m%d')}.png"
        save_path = os.path.join(output_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✅ District comparison saved to: {save_path}")
        
        # Print top districts
        print("\n🏆 Top 5 Districts by Total Demand:")
        for i, row in district_stats.head(5).iterrows():
            print(f"  {i+1}. {row['district']:25s} - {row['total_footfall']:,.0f} residents ({row['num_centers']} centers)")
    
    def create_urban_rural_comparison(self, data_path='data/processed/pec_features.csv',
                                     output_dir='visualizations/output'):
        """
        Compare demand patterns between Urban, Rural, and Semi-Urban centers
        
        Args:
            data_path: Path to features CSV
            output_dir: Directory to save visualization
        """
        print("\n🏘️  Generating Urban-Rural Comparison...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        
        # Monthly aggregation by center type
        monthly_stats = df.groupby(['month', 'center_type'])['footfall'].mean().reset_index()
        
        # Pivot for plotting
        pivot = monthly_stats.pivot(index='month', columns='center_type', values='footfall')
        
        # Create line plot
        fig, ax = plt.subplots(figsize=(14, 8))
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for center_type in ['Urban', 'Semi-Urban', 'Rural']:
            if center_type in pivot.columns:
                ax.plot(
                    pivot.index,
                    pivot[center_type],
                    marker='o',
                    linewidth=2.5,
                    label=center_type,
                    markersize=8
                )
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Daily Footfall', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Demand Patterns: Urban vs Rural vs Semi-Urban Centers', 
                    fontsize=16, fontweight='bold')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names)
        ax.legend(fontsize=12, loc='best')
        ax.grid(True, alpha=0.3)
        
        # Highlight key months
        ax.axvspan(6, 7, alpha=0.1, color='blue', label='School Enrollment')
        ax.axvspan(11, 11, alpha=0.1, color='green', label='Pension Updates')
        
        plt.tight_layout()
        
        # Save
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, 'urban_rural_comparison.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✅ Urban-Rural comparison saved to: {save_path}")
        
        # Print key insights
        print("\n💡 Key Insights:")
        print(f"  • Urban centers average:      {pivot['Urban'].mean():.0f} residents/day")
        if 'Semi-Urban' in pivot.columns:
            print(f"  • Semi-Urban centers average: {pivot['Semi-Urban'].mean():.0f} residents/day")
        if 'Rural' in pivot.columns:
            print(f"  • Rural centers average:      {pivot['Rural'].mean():.0f} residents/day")
    
    def _print_insights(self, pivot_df):
        """Print strategic insights from heatmap data"""
        
        print("\n💡 Strategic Insights:")
        
        # Busiest day across all PINs
        daily_avg = pivot_df.mean()
        busiest_day = daily_avg.idxmax()
        busiest_avg = daily_avg.max()
        print(f"  • Busiest day: {busiest_day} (avg {busiest_avg:.0f} residents)")
        
        # Quietest day
        quietest_day = daily_avg.idxmin()
        quietest_avg = daily_avg.min()
        print(f"  • Quietest day: {quietest_day} (avg {quietest_avg:.0f} residents)")
        
        # Busiest PIN code
        pin_avg = pivot_df.mean(axis=1)
        busiest_pin = pin_avg.idxmax()
        busiest_pin_avg = pin_avg.max()
        print(f"  • Highest demand PIN: {busiest_pin} (avg {busiest_pin_avg:.0f} residents/day)")
        
        # Variance (identify volatile centers)
        pin_variance = pivot_df.var(axis=1)
        most_volatile_pin = pin_variance.idxmax()
        print(f"  • Most volatile demand: {most_volatile_pin} (high day-to-day variation)")

def main():
    """Main execution function"""
    print("🏛️  PEC Demand Forecasting - Visualization Suite")
    print("=" * 60)
    
    generator = DemandHeatmapGenerator()
    
    # Generate all visualizations
    generator.create_weekly_heatmap()
    generator.create_district_comparison()
    generator.create_urban_rural_comparison()
    
    print("\n✨ All visualizations generated successfully!")

if __name__ == "__main__":
    main()
