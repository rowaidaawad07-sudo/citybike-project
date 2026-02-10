# main.py
"""
CityBike - Bike Sharing Analytics Platform
Main entry point for the capstone project.
"""

import sys
import os
from pathlib import Path

# Add citybike to path
sys.path.insert(0, str(Path(__file__).parent / 'citybike'))

from analyzer import BikeShareSystem
from visualization import create_all_visualizations

def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = ['data', 'output/figures', 'output/reports']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def print_banner():
    """Print project banner."""
    banner = """
    ====================================================
    🚴 CITYBIKE - BIKE SHARING ANALYTICS PLATFORM
    ====================================================
    Capstone Project - Python Programming & Data Analysis
    ====================================================
    """
    print(banner)

def main():
    """Main execution pipeline."""
    try:
        # 1. Setup
        print_banner()
        ensure_directories()
        
        # 2. Initialize system
        print("\n📦 Initializing BikeShareSystem...")
        system = BikeShareSystem()
        
        # 3. Load data
        print("📥 Loading data from CSV files...")
        system.load_data()
        
        # 4. Clean data
        print("🧹 Cleaning and preparing data...")
        system.clean_data()
        
        # 5. Generate reports
        print("📊 Generating analysis reports...")
        system.generate_summary_report()
        
        # 6. Display key insights
        print("\n" + "="*60)
        print("📈 KEY BUSINESS INSIGHTS")
        print("="*60)
        
        summary = system.total_trips_summary()
        print(f"\n📊 Overall Summary:")
        print(f"   • Total Trips: {summary['total_trips']:,}")
        print(f"   • Total Distance: {summary['total_distance_km']:,} km")
        print(f"   • Average Duration: {summary['avg_duration_min']:.1f} min")
        
        # 7. Create visualizations
        print("\n" + "="*60)
        print("🎨 DATA VISUALIZATION")
        print("="*60)
        create_all_visualizations(system.trips, system.stations)
        
        # 8. Completion message
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        print("\n📁 Generated Files:")
        print("   • data/trips_clean.csv")
        print("   • data/stations_clean.csv")
        print("   • output/summary_report.txt")
        print("   • output/figures/trips_per_station.png")
        print("   • output/figures/monthly_trend.png")
        print("   • output/figures/duration_histogram.png")
        print("   • output/figures/duration_by_user_type.png")
        print("\n🏁 Program executed successfully!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()