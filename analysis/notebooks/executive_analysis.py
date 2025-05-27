#!/usr/bin/env python3
"""
Indonesian Mineral Export Analysis - Executive Summary
Focused analysis with key insights and strategic recommendations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("🇮🇩 INDONESIAN MINERAL EXPORT ANALYSIS")
print("="*60)

# Load data
data_path = '../../data/ekspor_mineral_indonesia_WITS.csv'
print("📂 Loading dataset...")

try:
    df = pd.read_csv(data_path, encoding='utf-8')
    print(f"✅ Data loaded: {df.shape[0]:,} records, {df.shape[1]} columns")
except:
    df = pd.read_csv(data_path, encoding='latin-1')
    print(f"✅ Data loaded with latin-1: {df.shape[0]:,} records, {df.shape[1]} columns")

# Identify key columns
value_col = 'Trade Value 1000USD'
country_col = 'Partner'
product_col = 'Product Description'
year_col = 'Year'
quantity_col = 'Quantity'

print(f"\n📊 DATASET OVERVIEW")
print(f"Time period: {df[year_col].min()} - {df[year_col].max()}")
print(f"Total export value: ${df[value_col].sum():,.0f}K USD")
print(f"Number of markets: {df[country_col].nunique()}")
print(f"Number of products: {df[product_col].nunique()}")

# 1. TEMPORAL ANALYSIS
print(f"\n📈 TEMPORAL TRENDS")
print("-" * 40)
annual_exports = df.groupby(year_col)[value_col].sum()
for year, value in annual_exports.items():
    print(f"{year}: ${value:,.0f}K USD")

# Growth rates
growth_rates = annual_exports.pct_change() * 100
print(f"\n📊 Year-over-Year Growth:")
for year, rate in growth_rates.dropna().items():
    status = "📈" if rate > 0 else "📉"
    print(f"{year}: {status} {rate:+.1f}%")

# 2. MARKET ANALYSIS
print(f"\n🌍 TOP EXPORT MARKETS")
print("-" * 40)
top_markets = df.groupby(country_col)[value_col].sum().sort_values(ascending=False).head(10)
for i, (country, value) in enumerate(top_markets.items(), 1):
    share = (value / df[value_col].sum()) * 100
    print(f"{i:2d}. {country}: ${value:,.0f}K USD ({share:.1f}%)")

# Market concentration (HHI)
market_shares = df.groupby(country_col)[value_col].sum()
total_value = market_shares.sum()
market_shares_pct = (market_shares / total_value * 100) ** 2
hhi = market_shares_pct.sum()

print(f"\n📊 Market Concentration Analysis:")
print(f"Herfindahl-Hirschman Index (HHI): {hhi:.0f}")
if hhi < 1500:
    concentration = "Low (Well diversified)"
elif hhi < 2500:
    concentration = "Moderate"
else:
    concentration = "High (Concentrated)"
print(f"Concentration level: {concentration}")

# 3. PRODUCT ANALYSIS
print(f"\n⛏️ TOP MINERAL PRODUCTS")
print("-" * 40)
top_products = df.groupby(product_col)[value_col].sum().sort_values(ascending=False).head(8)
for i, (product, value) in enumerate(top_products.items(), 1):
    share = (value / df[value_col].sum()) * 100
    product_name = product[:50] + "..." if len(product) > 50 else product
    print(f"{i}. {product_name}")
    print(f"   Value: ${value:,.0f}K USD ({share:.1f}%)")

# Product concentration
product_shares = df.groupby(product_col)[value_col].sum()
product_shares_pct = (product_shares / total_value * 100) ** 2
product_hhi = product_shares_pct.sum()
print(f"\n📊 Product Diversification (HHI): {product_hhi:.0f}")

# 4. VALUE ANALYSIS
print(f"\n💰 EXPORT VALUE STATISTICS")
print("-" * 40)
print(f"Total export value: ${df[value_col].sum():,.0f}K USD")
print(f"Average transaction: ${df[value_col].mean():,.0f}K USD")
print(f"Median transaction: ${df[value_col].median():,.0f}K USD")
print(f"Largest transaction: ${df[value_col].max():,.0f}K USD")

# High-value transactions
high_value = df[df[value_col] > df[value_col].quantile(0.95)]
print(f"\nTop 5% transactions:")
print(f"Count: {len(high_value):,} ({len(high_value)/len(df)*100:.1f}%)")
print(f"Value: ${high_value[value_col].sum():,.0f}K USD ({high_value[value_col].sum()/df[value_col].sum()*100:.1f}%)")

# 5. STRATEGIC INSIGHTS
print(f"\n🎯 STRATEGIC INSIGHTS")
print("=" * 60)

insights = []

# Market insights
if hhi < 1500:
    insights.append("✅ MARKET DIVERSIFICATION: Strong market diversification reduces risk")
elif hhi > 2500:
    insights.append("⚠️ MARKET RISK: High market concentration - diversification needed")

# Growth insights
avg_growth = growth_rates.mean()
if avg_growth > 5:
    insights.append(f"📈 STRONG GROWTH: Average {avg_growth:.1f}% annual growth")
elif avg_growth < 0:
    insights.append(f"📉 DECLINING TREND: Negative {avg_growth:.1f}% average growth")

# Product insights
if product_hhi > 2500:
    insights.append("⚠️ PRODUCT CONCENTRATION: Portfolio needs diversification")

# Value insights
concentration_ratio = high_value[value_col].sum() / df[value_col].sum()
if concentration_ratio > 0.5:
    insights.append("💎 HIGH-VALUE FOCUS: Large portion from premium transactions")

for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

# 6. STRATEGIC RECOMMENDATIONS
print(f"\n🚀 STRATEGIC RECOMMENDATIONS")
print("=" * 60)

print("⚡ IMMEDIATE ACTIONS (0-6 months):")
immediate = [
    "Implement real-time export monitoring dashboard",
    "Conduct detailed competitor analysis in top 3 markets",
    "Assess value-added processing opportunities for top products",
    "Develop customer relationship management for high-value clients"
]

for i, rec in enumerate(immediate, 1):
    print(f"   {i}. {rec}")

print(f"\n📅 MEDIUM-TERM INITIATIVES (6-18 months):")
medium_term = [
    "Develop market entry strategies for emerging economies",
    "Invest in downstream processing capabilities",
    "Establish strategic partnerships with key buyers",
    "Implement ESG compliance framework for international markets"
]

for i, rec in enumerate(medium_term, 1):
    print(f"   {i}. {rec}")

print(f"\n🔮 LONG-TERM STRATEGY (18+ months):")
long_term = [
    "Build integrated mining-to-manufacturing value chains",
    "Develop renewable energy powered mining operations",
    "Create regional distribution networks",
    "Establish strategic mineral reserves for market leverage"
]

for i, rec in enumerate(long_term, 1):
    print(f"   {i}. {rec}")

# 7. SAVE SUMMARY REPORT
print(f"\n💾 GENERATING SUMMARY REPORT")
print("-" * 40)

report = f"""# Indonesian Mineral Export Analysis Summary
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Metrics
- **Dataset**: {df.shape[0]:,} export records
- **Time Period**: {df[year_col].min()}-{df[year_col].max()}
- **Total Export Value**: ${df[value_col].sum():,.0f}K USD
- **Markets Served**: {df[country_col].nunique()}
- **Product Portfolio**: {df[product_col].nunique()} mineral products

## Top 5 Export Markets
"""

for i, (country, value) in enumerate(top_markets.head(5).items(), 1):
    share = (value / df[value_col].sum()) * 100
    report += f"{i}. {country}: ${value:,.0f}K USD ({share:.1f}%)\n"

report += f"""
## Market Analysis
- **Market Concentration (HHI)**: {hhi:.0f} ({concentration})
- **Product Diversification (HHI)**: {product_hhi:.0f}
- **Average Annual Growth**: {avg_growth:.1f}%

## Strategic Priorities
1. {"Market diversification" if hhi > 2500 else "Maintain market diversification"}
2. {"Product portfolio expansion" if product_hhi > 2500 else "Optimize product mix"}
3. {"Growth acceleration" if avg_growth < 5 else "Sustain growth momentum"}
4. Value-added processing development
5. Sustainable mining practices implementation

## Risk Assessment
- **Market Risk**: {"High" if hhi > 2500 else "Low" if hhi < 1500 else "Moderate"}
- **Product Risk**: {"High" if product_hhi > 2500 else "Low" if product_hhi < 1500 else "Moderate"}
- **Growth Risk**: {"High" if avg_growth < 0 else "Low" if avg_growth > 5 else "Moderate"}
"""

with open('indonesian_mineral_export_summary.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ Summary report saved: indonesian_mineral_export_summary.md")

# 8. CREATE SIMPLE VISUALIZATION
print(f"\n📊 CREATING VISUALIZATION")
print("-" * 40)

try:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Indonesian Mineral Export Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # Annual trends
    annual_exports.plot(kind='line', marker='o', ax=ax1, linewidth=3, markersize=8)
    ax1.set_title('Annual Export Values', fontweight='bold')
    ax1.set_ylabel('Export Value (Thousand USD)')
    ax1.grid(True, alpha=0.3)
    
    # Top markets
    top_markets.head(8).plot(kind='barh', ax=ax2)
    ax2.set_title('Top Export Markets', fontweight='bold')
    ax2.set_xlabel('Export Value (Thousand USD)')
    
    # Growth rates
    growth_rates.dropna().plot(kind='bar', ax=ax3, color=['green' if x > 0 else 'red' for x in growth_rates.dropna()])
    ax3.set_title('Year-over-Year Growth Rates', fontweight='bold')
    ax3.set_ylabel('Growth Rate (%)')
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Market share pie chart
    top_5_markets = top_markets.head(5)
    others_value = top_markets.iloc[5:].sum()
    pie_data = list(top_5_markets.values) + [others_value]
    pie_labels = list(top_5_markets.index) + ['Others']
    
    ax4.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90)
    ax4.set_title('Market Share Distribution', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('indonesian_mineral_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard saved: indonesian_mineral_dashboard.png")
    
except Exception as e:
    print(f"⚠️ Visualization error: {e}")

print(f"\n🎉 ANALYSIS COMPLETE!")
print("=" * 60)
print("📁 Generated Files:")
print("   - indonesian_mineral_export_summary.md")
print("   - indonesian_mineral_dashboard.png")
print("   - data_exploration_results.txt")

print(f"\n✅ Indonesian Mineral Export Analysis completed successfully!")
print("🚀 Ready for strategic decision making and business optimization!")
