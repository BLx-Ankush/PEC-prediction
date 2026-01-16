"""
Time-Series Trend Analysis
Analyze and visualize temporal patterns in PEC demand
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class TrendAnalyzer:
    """Analyze temporal trends and patterns in PEC footfall"""
    
    def analyze_day_of_week_pattern(self, data_path='data/processed/pec_features.csv',
                                   output_dir='visualizations/output'):
        """
        Analyze demand patterns by day of week
        
        Args:
            data_path: Path to features CSV
            output_dir: Directory to save visualization
        """
        print("📅 Analyzing Day-of-Week Patterns...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Add day name
        df['day_name'] = df['date'].dt.day_name()
        
        # Calculate average by day of week and center type
        day_stats = df.groupby(['day_name', 'center_type'])['footfall'].agg(['mean', 'std']).reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_stats['day_name'] = pd.Categorical(day_stats['day_name'], categories=day_order, ordered=True)
        day_stats = day_stats.sort_values('day_name')
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Group by center type
        for center_type in ['Urban', 'Semi-Urban', 'Rural']:
            subset = day_stats[day_stats['center_type'] == center_type]
            if len(subset) > 0:
                ax.plot(
                    subset['day_name'],
                    subset['mean'],
                    marker='o',
                    linewidth=2.5,
                    label=center_type,
                    markersize=10
                )
                # Add error bars
                ax.fill_between(
                    range(len(subset)),
                    subset['mean'] - subset['std'],
                    subset['mean'] + subset['std'],
                    alpha=0.2
                )
        
        ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Footfall', fontsize=12, fontweight='bold')
        ax.set_title('PEC Demand by Day of Week', fontsize=16, fontweight='bold')
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        # Highlight weekends
        ax.axvspan(5, 7, alpha=0.1, color='red', label='Weekend')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, 'day_of_week_pattern.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Day-of-week analysis saved to: {save_path}")
        
        # Print insights
        overall_daily = df.groupby('day_name')['footfall'].mean()
        overall_daily = overall_daily.reindex(day_order)
        
        print("\n📊 Average Footfall by Day:")
        for day, footfall in overall_daily.items():
            print(f"  {day:10s}: {footfall:6.0f} residents")
    
    def analyze_holiday_impact(self, data_path='data/processed/pec_features.csv',
                              output_dir='visualizations/output'):
        """
        Analyze the impact of holidays on PEC demand
        
        Args:
            data_path: Path to features CSV
            output_dir: Directory to save visualization
        """
        print("\n🎉 Analyzing Holiday Impact...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        
        # Group by holiday status
        holiday_stats = df.groupby(['is_holiday', 'center_type'])['footfall'].agg(['mean', 'count']).reset_index()
        
        # Create comparison visualization
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Chart 1: Average footfall comparison
        pivot = holiday_stats.pivot(index='center_type', columns='is_holiday', values='mean')
        pivot.columns = ['Regular Day', 'Holiday']
        
        pivot.plot(kind='bar', ax=axes[0], color=['#2E86AB', '#F18F01'], width=0.7)
        axes[0].set_xlabel('Center Type', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Average Footfall', fontsize=12, fontweight='bold')
        axes[0].set_title('Holiday vs Regular Day Demand', fontsize=14, fontweight='bold')
        axes[0].legend(fontsize=11)
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
        
        # Chart 2: Day-after-holiday spike
        day_after_stats = df.groupby(['is_day_after_holiday', 'center_type'])['footfall'].mean().reset_index()
        pivot2 = day_after_stats.pivot(index='center_type', columns='is_day_after_holiday', values='footfall')
        pivot2.columns = ['Regular Day', 'Day After Holiday']
        
        pivot2.plot(kind='bar', ax=axes[1], color=['#2E86AB', '#C73E1D'], width=0.7)
        axes[1].set_xlabel('Center Type', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Average Footfall', fontsize=12, fontweight='bold')
        axes[1].set_title('Post-Holiday Surge Effect', fontsize=14, fontweight='bold')
        axes[1].legend(fontsize=11)
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
        
        plt.tight_layout()
        
        # Save
        save_path = os.path.join(output_dir, 'holiday_impact.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Holiday impact analysis saved to: {save_path}")
        
        # Calculate percentage changes
        overall_holiday = df.groupby('is_holiday')['footfall'].mean()
        if len(overall_holiday) == 2:
            pct_drop = ((overall_holiday[0] - overall_holiday[1]) / overall_holiday[0]) * 100
            print(f"\n💡 On holidays, demand drops by {pct_drop:.1f}%")
        
        day_after = df.groupby('is_day_after_holiday')['footfall'].mean()
        if len(day_after) == 2:
            pct_surge = ((day_after[1] - day_after[0]) / day_after[0]) * 100
            print(f"💡 Day after holidays, demand surges by {pct_surge:.1f}%")
    
    def analyze_seasonal_trends(self, data_path='data/processed/pec_features.csv',
                               output_dir='visualizations/output'):
        """
        Analyze monthly and seasonal demand trends
        
        Args:
            data_path: Path to features CSV
            output_dir: Directory to save visualization
        """
        print("\n🌡️  Analyzing Seasonal Trends...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        df['year_month'] = df['date'].dt.to_period('M')
        
        # Monthly aggregation
        monthly = df.groupby('year_month')['footfall'].agg(['mean', 'sum', 'count']).reset_index()
        monthly['year_month'] = monthly['year_month'].astype(str)
        
        # Create multi-panel plot
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Plot 1: Average daily footfall by month
        axes[0].plot(
            monthly['year_month'],
            monthly['mean'],
            marker='o',
            linewidth=2.5,
            color='#2E86AB',
            markersize=8
        )
        axes[0].fill_between(range(len(monthly)), monthly['mean'], alpha=0.3, color='#2E86AB')
        axes[0].set_ylabel('Avg Daily Footfall', fontsize=12, fontweight='bold')
        axes[0].set_title('Monthly Average PEC Demand', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Highlight peak seasons
        for idx, row in monthly.iterrows():
            month_num = int(row['year_month'].split('-')[1])
            if month_num in [6, 7]:  # School enrollment
                axes[0].axvspan(idx-0.4, idx+0.4, alpha=0.2, color='blue')
            elif month_num == 11:  # Pension
                axes[0].axvspan(idx-0.4, idx+0.4, alpha=0.2, color='green')
        
        # Plot 2: Total monthly footfall
        axes[1].bar(monthly['year_month'], monthly['sum'], color='#A23B72', alpha=0.7)
        axes[1].set_ylabel('Total Monthly Footfall', fontsize=12, fontweight='bold')
        axes[1].set_title('Total Monthly PEC Traffic', fontsize=14, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Box plot by month (across all years)
        df['month'] = df['date'].dt.month
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        sns.boxplot(
            data=df,
            x='month',
            y='footfall',
            palette='Set2',
            ax=axes[2]
        )
        axes[2].set_xlabel('Month', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('Footfall Distribution', fontsize=12, fontweight='bold')
        axes[2].set_title('Demand Variability by Month', fontsize=14, fontweight='bold')
        axes[2].set_xticklabels(month_names)
        axes[2].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save
        save_path = os.path.join(output_dir, 'seasonal_trends.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Seasonal trends analysis saved to: {save_path}")
        
        # Print peak months
        month_avg = df.groupby('month')['footfall'].mean().sort_values(ascending=False)
        print("\n🏆 Top 5 Busiest Months:")
        for month, footfall in month_avg.head(5).items():
            print(f"  {month_names[month-1]:10s}: {footfall:6.0f} avg residents/day")
    
    def create_comprehensive_dashboard(self, data_path='data/processed/pec_features.csv',
                                      output_dir='visualizations/output'):
        """
        Create a comprehensive dashboard with multiple metrics
        
        Args:
            data_path: Path to features CSV
            output_dir: Directory to save visualization
        """
        print("\n📊 Creating Comprehensive Dashboard...")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Create figure with subplots
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Overall time series
        ax1 = fig.add_subplot(gs[0, :])
        daily_total = df.groupby('date')['footfall'].sum()
        ax1.plot(daily_total.index, daily_total.values, linewidth=1.5, color='#2E86AB')
        ax1.fill_between(daily_total.index, daily_total.values, alpha=0.3, color='#2E86AB')
        ax1.set_title('Total Daily PEC Footfall Across All Centers', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Total Footfall', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        # 2. Center type distribution
        ax2 = fig.add_subplot(gs[1, 0])
        type_avg = df.groupby('center_type')['footfall'].mean().sort_values(ascending=False)
        ax2.bar(type_avg.index, type_avg.values, color=['#2E86AB', '#A23B72', '#F18F01'])
        ax2.set_title('Avg Demand by Center Type', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Avg Footfall', fontsize=10)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Top 10 districts
        ax3 = fig.add_subplot(gs[1, 1])
        district_avg = df.groupby('district')['footfall'].mean().sort_values(ascending=False).head(10)
        ax3.barh(district_avg.index, district_avg.values, color='#C73E1D')
        ax3.set_title('Top 10 Districts by Demand', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Avg Footfall', fontsize=10)
        
        # 4. Day of week pattern
        ax4 = fig.add_subplot(gs[1, 2])
        df['day_name'] = df['date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_avg = df.groupby('day_name')['footfall'].mean().reindex(day_order)
        ax4.plot(day_avg.values, marker='o', linewidth=2, markersize=8, color='#2E86AB')
        ax4.set_title('Weekly Pattern', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(7))
        ax4.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
        ax4.grid(True, alpha=0.3)
        
        # 5. Monthly trend
        ax5 = fig.add_subplot(gs[2, 0])
        df['month'] = df['date'].dt.month
        month_avg = df.groupby('month')['footfall'].mean()
        month_names = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        ax5.bar(month_avg.index, month_avg.values, color='#A23B72')
        ax5.set_title('Monthly Demand Pattern', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Month', fontsize=10)
        ax5.set_xticks(range(1, 13))
        ax5.set_xticklabels(month_names)
        
        # 6. Demand distribution
        ax6 = fig.add_subplot(gs[2, 1])
        ax6.hist(df['footfall'], bins=50, color='#F18F01', alpha=0.7, edgecolor='black')
        ax6.set_title('Footfall Distribution', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Footfall', fontsize=10)
        ax6.set_ylabel('Frequency', fontsize=10)
        
        # 7. Key statistics box
        ax7 = fig.add_subplot(gs[2, 2])
        ax7.axis('off')
        
        stats_text = f"""
        KEY STATISTICS
        ─────────────────────
        Total Records: {len(df):,}
        Date Range: {df['date'].min().date()} 
                    to {df['date'].max().date()}
        
        Avg Daily Footfall: {df['footfall'].mean():.0f}
        Median: {df['footfall'].median():.0f}
        Std Dev: {df['footfall'].std():.0f}
        
        Peak Day: {df['footfall'].max():.0f} residents
        Low Day: {df['footfall'].min():.0f} residents
        
        Total PINs: {df['pincode'].nunique()}
        Total Districts: {df['district'].nunique()}
        """
        
        ax7.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.suptitle('PEC Demand Forecasting - Comprehensive Dashboard', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        # Save
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, 'comprehensive_dashboard.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Comprehensive dashboard saved to: {save_path}")

def main():
    """Main execution function"""
    print("🏛️  PEC Demand Forecasting - Trend Analysis")
    print("=" * 60)
    
    analyzer = TrendAnalyzer()
    
    # Run all analyses
    analyzer.analyze_day_of_week_pattern()
    analyzer.analyze_holiday_impact()
    analyzer.analyze_seasonal_trends()
    analyzer.create_comprehensive_dashboard()
    
    print("\n✨ All trend analyses complete!")

if __name__ == "__main__":
    main()
