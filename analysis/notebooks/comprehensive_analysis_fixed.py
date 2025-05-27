#!/usr/bin/env python3
"""
Indonesian Mineral Export Data - Comprehensive Analysis
Complete analytical framework with business insights and strategic recommendations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend for compatibility
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Configure display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x))
plt.style.use('default')
sns.set_palette("husl")

class IndonesianMineralAnalyzer:
    """Comprehensive analyzer for Indonesian mineral export data"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        """Load and prepare the dataset"""
        print("🇮🇩 LOADING INDONESIAN MINERAL EXPORT DATA")
        print("="*60)
        
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            print(f"✅ Data loaded successfully!")
            print(f"📊 Dataset shape: {self.df.shape}")
            print(f"💾 Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            # Basic data cleaning
            self.df.columns = self.df.columns.str.strip()
            
            # Identify business indicators
            self.identify_business_indicators()
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def identify_business_indicators(self):
        """Smart identification of business indicators"""
        print("\n🔍 IDENTIFYING BUSINESS INDICATORS")
        print("-"*50)
        
        # Find key columns
        columns = self.df.columns.tolist()
        
        # Country/Partner columns
        country_cols = [col for col in columns if any(term in col.lower() for term in ['partner', 'country', 'destination'])]
        
        # Product columns  
        product_cols = [col for col in columns if any(term in col.lower() for term in ['product', 'commodity', 'item'])]
        
        # Value columns
        value_cols = [col for col in columns if any(term in col.lower() for term in ['value', 'amount', 'usd', 'dollar'])]
        
        # Quantity columns
        quantity_cols = [col for col in columns if any(term in col.lower() for term in ['quantity', 'volume', 'weight', 'ton'])]
        
        # Time columns
        time_cols = [col for col in columns if any(term in col.lower() for term in ['year', 'date', 'time', 'period'])]
        
        self.business_indicators = {
            'country_col': country_cols[0] if country_cols else None,
            'product_col': product_cols[0] if product_cols else None,
            'value_col': value_cols[0] if value_cols else None,
            'quantity_col': quantity_cols[0] if quantity_cols else None,
            'time_col': time_cols[0] if time_cols else None
        }
        
        print("📊 Business Indicators Identified:")
        for key, value in self.business_indicators.items():
            print(f"   {key}: {value}")
    
    def temporal_analysis(self):
        """Analyze temporal trends"""
        print("\n📈 TEMPORAL ANALYSIS")
        print("-"*50)
        
        time_col = self.business_indicators['time_col']
        value_col = self.business_indicators['value_col']
        
        if time_col and value_col:
            # Annual trends
            annual_trends = self.df.groupby(time_col).agg({
                value_col: ['sum', 'mean', 'count']
            }).round(2)
            
            print("📊 Annual Export Trends:")
            print(annual_trends)
            
            # Growth rates
            annual_values = self.df.groupby(time_col)[value_col].sum()
            growth_rates = annual_values.pct_change() * 100
            
            print(f"\n📈 Year-over-Year Growth Rates:")
            for year, rate in growth_rates.dropna().items():
                print(f"   {year}: {rate:+.1f}%")
            
            self.analysis_results['temporal'] = {
                'annual_trends': annual_trends,
                'growth_rates': growth_rates
            }
    
    def market_analysis(self):
        """Analyze export markets and destinations"""
        print("\n🌍 MARKET ANALYSIS")
        print("-"*50)
        
        country_col = self.business_indicators['country_col']
        value_col = self.business_indicators['value_col']
        
        if country_col and value_col:
            # Top markets
            top_markets = self.df.groupby(country_col)[value_col].sum().sort_values(ascending=False).head(10)
            
            print("🏆 Top 10 Export Markets:")
            for i, (country, value) in enumerate(top_markets.items(), 1):
                print(f"   {i:2d}. {country}: ${value:,.0f}K USD")
            
            # Market concentration (HHI)
            market_shares = self.df.groupby(country_col)[value_col].sum()
            total_value = market_shares.sum()
            market_shares_pct = (market_shares / total_value * 100) ** 2
            hhi = market_shares_pct.sum()
            
            print(f"\n📊 Market Concentration (HHI): {hhi:.0f}")
            if hhi < 1500:
                concentration_level = "Low (Diversified)"
            elif hhi < 2500:
                concentration_level = "Moderate"
            else:
                concentration_level = "High (Concentrated)"
            print(f"   Concentration Level: {concentration_level}")
            
            self.analysis_results['markets'] = {
                'top_markets': top_markets,
                'hhi': hhi,
                'concentration_level': concentration_level
            }
    
    def product_analysis(self):
        """Analyze mineral products and portfolio"""
        print("\n⛏️ PRODUCT PORTFOLIO ANALYSIS")
        print("-"*50)
        
        product_col = self.business_indicators['product_col']
        value_col = self.business_indicators['value_col']
        
        if product_col and value_col:
            # Top products
            top_products = self.df.groupby(product_col)[value_col].sum().sort_values(ascending=False).head(10)
            
            print("💎 Top 10 Mineral Products:")
            for i, (product, value) in enumerate(top_products.items(), 1):
                product_name = str(product)[:50] + "..." if len(str(product)) > 50 else str(product)
                print(f"   {i:2d}. {product_name}: ${value:,.0f}K USD")
            
            # Product diversification
            product_shares = self.df.groupby(product_col)[value_col].sum()
            total_value = product_shares.sum()
            product_shares_pct = (product_shares / total_value * 100) ** 2
            product_hhi = product_shares_pct.sum()
            
            print(f"\n📊 Product Diversification (HHI): {product_hhi:.0f}")
            
            self.analysis_results['products'] = {
                'top_products': top_products,
                'product_hhi': product_hhi
            }
    
    def value_quantity_analysis(self):
        """Analyze export values and quantities"""
        print("\n💰 VALUE & QUANTITY ANALYSIS")
        print("-"*50)
        
        value_col = self.business_indicators['value_col']
        quantity_col = self.business_indicators['quantity_col']
        
        if value_col:
            # Value statistics
            print("📊 Export Value Statistics:")
            print(f"   Total Export Value: ${self.df[value_col].sum():,.0f}K USD")
            print(f"   Average Transaction: ${self.df[value_col].mean():,.0f}K USD")
            print(f"   Median Transaction: ${self.df[value_col].median():,.0f}K USD")
            print(f"   Standard Deviation: ${self.df[value_col].std():,.0f}K USD")
            
        if quantity_col:
            # Quantity statistics  
            print(f"\n📦 Export Quantity Statistics:")
            print(f"   Total Quantity: {self.df[quantity_col].sum():,.0f}")
            print(f"   Average Quantity: {self.df[quantity_col].mean():,.0f}")
    
    def create_visualizations(self):
        """Create comprehensive visualization dashboard"""
        print("\n📊 CREATING VISUALIZATION DASHBOARD")
        print("-"*50)
        
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(2, 3, figsize=(20, 12))
            fig.suptitle('🇮🇩 Indonesian Mineral Export Analysis Dashboard', fontsize=16, fontweight='bold')
            
            time_col = self.business_indicators['time_col']
            value_col = self.business_indicators['value_col']
            country_col = self.business_indicators['country_col']
            product_col = self.business_indicators['product_col']
            
            # 1. Annual Export Trends
            if time_col and value_col:
                annual_values = self.df.groupby(time_col)[value_col].sum() / 1000  # Convert to millions
                axes[0,0].plot(annual_values.index, annual_values.values, marker='o', linewidth=3, markersize=8, color='blue')
                axes[0,0].set_title('Annual Export Values', fontweight='bold')
                axes[0,0].set_xlabel('Year')
                axes[0,0].set_ylabel('Export Value (Million USD)')
                axes[0,0].grid(True, alpha=0.3)
            
            # 2. Top Markets
            if country_col and value_col:
                top_markets = self.df.groupby(country_col)[value_col].sum().sort_values(ascending=False).head(8)
                y_pos = range(len(top_markets))
                axes[0,1].barh(y_pos, top_markets.values, color='lightblue')
                axes[0,1].set_yticks(y_pos)
                axes[0,1].set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_markets.index])
                axes[0,1].set_title('Top Export Markets', fontweight='bold')
                axes[0,1].set_xlabel('Export Value (Thousand USD)')
            
            # 3. Top Products
            if product_col and value_col:
                top_products = self.df.groupby(product_col)[value_col].sum().sort_values(ascending=False).head(8)
                y_pos = range(len(top_products))
                axes[0,2].barh(y_pos, top_products.values, color='lightgreen')
                axes[0,2].set_yticks(y_pos)
                axes[0,2].set_yticklabels([name[:20] + '...' if len(name) > 20 else name for name in top_products.index])
                axes[0,2].set_title('Top Mineral Products', fontweight='bold')
                axes[0,2].set_xlabel('Export Value (Thousand USD)')
            
            # 4. Market Share Distribution
            if country_col and value_col:
                market_shares = self.df.groupby(country_col)[value_col].sum().sort_values(ascending=False)
                top_5 = market_shares.head(5)
                others_value = market_shares.iloc[5:].sum() if len(market_shares) > 5 else 0
                
                if others_value > 0:
                    pie_labels = list(top_5.index) + ['Others']
                    pie_values = list(top_5.values) + [others_value]
                else:
                    pie_labels = list(top_5.index)
                    pie_values = list(top_5.values)
                
                colors = plt.cm.Set3(range(len(pie_values)))
                axes[1,0].pie(pie_values, labels=[name[:10] + '...' if len(name) > 10 else name for name in pie_labels], 
                             autopct='%1.1f%%', startangle=90, colors=colors)
                axes[1,0].set_title('Market Share Distribution', fontweight='bold')
            
            # 5. Export Value Distribution
            if value_col:
                # Use log scale for better visualization
                log_values = np.log10(self.df[value_col].replace(0, 1))  # Replace 0 with 1 for log
                axes[1,1].hist(log_values, bins=50, alpha=0.7, edgecolor='black', color='orange')
                axes[1,1].set_title('Export Value Distribution (Log Scale)', fontweight='bold')
                axes[1,1].set_xlabel('Log10(Export Value)')
                axes[1,1].set_ylabel('Frequency')
            
            # 6. Growth Trend Analysis
            if time_col and value_col:
                annual_values = self.df.groupby(time_col)[value_col].sum()
                if len(annual_values) > 1:
                    growth_rates = annual_values.pct_change() * 100
                    growth_data = growth_rates.dropna()
                    
                    if len(growth_data) > 0:
                        x_pos = range(len(growth_data))
                        colors = ['green' if x > 0 else 'red' for x in growth_data.values]
                        axes[1,2].bar(x_pos, growth_data.values, color=colors, alpha=0.7)
                        axes[1,2].set_xticks(x_pos)
                        axes[1,2].set_xticklabels(growth_data.index, rotation=45)
                        axes[1,2].set_title('Year-over-Year Growth Rates', fontweight='bold')
                        axes[1,2].set_ylabel('Growth Rate (%)')
                        axes[1,2].axhline(y=0, color='black', linestyle='-', alpha=0.3)
                        axes[1,2].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save the figure
            dashboard_path = 'indonesian_mineral_export_dashboard_comprehensive.png'
            plt.savefig(dashboard_path, dpi=300, bbox_inches='tight', facecolor='white')
            
            # Close the figure to free memory
            plt.close(fig)
            
            print(f"✅ Dashboard saved as: {dashboard_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Visualization error: {e}")
            print("📊 Creating simple alternative visualization...")
            
            # Simple fallback visualization
            try:
                plt.figure(figsize=(12, 8))
                
                if time_col and value_col:
                    annual_values = self.df.groupby(time_col)[value_col].sum() / 1000000  # Convert to billions
                    plt.subplot(2, 2, 1)
                    plt.plot(annual_values.index, annual_values.values, marker='o', linewidth=2)
                    plt.title('Annual Export Trends (Billion USD)')
                    plt.xlabel('Year')
                    plt.ylabel('Export Value')
                    plt.grid(True)
                
                if country_col and value_col:
                    top_markets = self.df.groupby(country_col)[value_col].sum().sort_values(ascending=False).head(5)
                    plt.subplot(2, 2, 2)
                    plt.bar(range(len(top_markets)), top_markets.values)
                    plt.title('Top 5 Export Markets')
                    plt.xticks(range(len(top_markets)), [name[:10] for name in top_markets.index], rotation=45)
                    plt.ylabel('Export Value')
                
                plt.tight_layout()
                plt.savefig('indonesian_mineral_simple_dashboard.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("✅ Simple dashboard saved as: indonesian_mineral_simple_dashboard.png")
                return True
                
            except Exception as e2:
                print(f"❌ Alternative visualization also failed: {e2}")
                return False
    
    def generate_insights(self):
        """Generate strategic business insights"""
        print("\n🎯 STRATEGIC BUSINESS INSIGHTS")
        print("="*60)
        
        insights = []
        
        # Market insights
        if 'markets' in self.analysis_results:
            hhi = self.analysis_results['markets']['hhi']
            if hhi < 1500:
                insights.append("✅ MARKET DIVERSIFICATION: Strong market diversification reduces dependency risk")
            elif hhi > 2500:
                insights.append("⚠️ MARKET CONCENTRATION: High dependency on few markets - diversification needed")
        
        # Growth insights
        if 'temporal' in self.analysis_results:
            growth_rates = self.analysis_results['temporal']['growth_rates']
            avg_growth = growth_rates.mean()
            if avg_growth > 5:
                insights.append(f"📈 STRONG GROWTH: Average annual growth of {avg_growth:.1f}% indicates healthy export performance")
            elif avg_growth < -5:
                insights.append(f"📉 DECLINING TREND: Negative average growth of {avg_growth:.1f}% requires strategic intervention")
        
        # Product insights
        if 'products' in self.analysis_results:
            product_hhi = self.analysis_results['products']['product_hhi']
            if product_hhi > 2500:
                insights.append("⚠️ PRODUCT CONCENTRATION: Portfolio concentrated in few products - diversification opportunity")
        
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        return insights
    
    def generate_recommendations(self):
        """Generate actionable business recommendations"""
        print("\n🚀 STRATEGIC RECOMMENDATIONS")
        print("="*60)
        
        recommendations = {
            'immediate': [],
            'medium_term': [],
            'long_term': []
        }
        
        # Market-based recommendations
        if 'markets' in self.analysis_results:
            hhi = self.analysis_results['markets']['hhi']
            if hhi > 2500:
                recommendations['immediate'].append("Develop market entry strategies for emerging economies")
                recommendations['medium_term'].append("Establish trade partnerships with 3-5 new countries")
                recommendations['long_term'].append("Build regional distribution networks in underserved markets")
        
        # Product-based recommendations
        if 'products' in self.analysis_results:
            recommendations['immediate'].append("Conduct value-added processing feasibility studies")
            recommendations['medium_term'].append("Invest in downstream processing capabilities")
            recommendations['long_term'].append("Develop integrated mining-to-manufacturing value chains")
        
        # General strategic recommendations
        recommendations['immediate'].extend([
            "Implement real-time export monitoring dashboard",
            "Conduct competitor analysis in top 3 markets"
        ])
        
        recommendations['medium_term'].extend([
            "Develop ESG compliance framework for international markets",
            "Establish forward contracts for price stability"
        ])
        
        recommendations['long_term'].extend([
            "Build strategic mineral reserves for market leverage",
            "Develop renewable energy powered mining operations"
        ])
        
        print("⚡ IMMEDIATE ACTIONS (0-6 months):")
        for i, rec in enumerate(recommendations['immediate'], 1):
            print(f"   {i}. {rec}")
        
        print("\n📅 MEDIUM-TERM INITIATIVES (6-18 months):")
        for i, rec in enumerate(recommendations['medium_term'], 1):
            print(f"   {i}. {rec}")
        
        print("\n🔮 LONG-TERM STRATEGY (18+ months):")
        for i, rec in enumerate(recommendations['long_term'], 1):
            print(f"   {i}. {rec}")
        
        return recommendations
    
    def save_comprehensive_report(self):
        """Save comprehensive analysis report"""
        print("\n💾 SAVING COMPREHENSIVE REPORT")
        print("-"*50)
        
        report_content = f"""# 🇮🇩 Indonesian Mineral Export Analysis Report
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Dataset Overview
- **Total Records**: {len(self.df):,}
- **Time Period**: {self.df[self.business_indicators['time_col']].min()} - {self.df[self.business_indicators['time_col']].max()}
- **Total Export Value**: ${self.df[self.business_indicators['value_col']].sum():,.0f}K USD
- **Number of Markets**: {self.df[self.business_indicators['country_col']].nunique()}
- **Number of Products**: {self.df[self.business_indicators['product_col']].nunique()}

## 🏆 Top Performance Metrics
"""
        
        # Add market analysis
        if 'markets' in self.analysis_results:
            report_content += f"""
### Top Export Markets
"""
            for i, (country, value) in enumerate(self.analysis_results['markets']['top_markets'].head(5).items(), 1):
                report_content += f"{i}. {country}: ${value:,.0f}K USD\\n"
            
            report_content += f"""
**Market Concentration (HHI)**: {self.analysis_results['markets']['hhi']:.0f} ({self.analysis_results['markets']['concentration_level']})
"""
        
        # Add insights and recommendations
        insights = self.generate_insights()
        recommendations = self.generate_recommendations()
        
        report_content += f"""
## 🎯 Key Insights
"""
        for insight in insights:
            report_content += f"- {insight}\\n"
        
        report_content += f"""
## 🚀 Strategic Recommendations

### Immediate Actions
"""
        for rec in recommendations['immediate']:
            report_content += f"- {rec}\\n"
        
        report_content += f"""
### Medium-term Initiatives
"""
        for rec in recommendations['medium_term']:
            report_content += f"- {rec}\\n"
        
        report_content += f"""
### Long-term Strategy
"""
        for rec in recommendations['long_term']:
            report_content += f"- {rec}\\n"
        
        # Save report
        with open('indonesian_mineral_export_comprehensive_report.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print("✅ Comprehensive report saved as: indonesian_mineral_export_comprehensive_report.md")
    
    def run_complete_analysis(self):
        """Execute complete analysis pipeline"""
        print("🇮🇩 STARTING COMPREHENSIVE INDONESIAN MINERAL EXPORT ANALYSIS")
        print("="*80)
        
        if not self.load_data():
            return False
        
        try:
            # Execute all analysis modules
            print("📊 Running temporal analysis...")
            self.temporal_analysis()
            
            print("🌍 Running market analysis...")
            self.market_analysis()
            
            print("⛏️ Running product analysis...")
            self.product_analysis()
            
            print("💰 Running value analysis...")
            self.value_quantity_analysis()
            
            print("📈 Creating visualizations...")
            viz_success = self.create_visualizations()
            
            print("🎯 Generating insights...")
            self.generate_insights()
            
            print("🚀 Generating recommendations...")
            self.generate_recommendations()
            
            print("💾 Saving comprehensive report...")
            self.save_comprehensive_report()
            
            print("\n🎉 ANALYSIS COMPLETE!")
            print("="*80)
            print("📁 Generated Files:")
            if viz_success:
                print("   - indonesian_mineral_export_dashboard_comprehensive.png")
            else:
                print("   - indonesian_mineral_simple_dashboard.png (fallback)")
            print("   - indonesian_mineral_export_comprehensive_report.md")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Analysis failed with error: {e}")
            print("📋 Partial results may have been generated.")
            return False

if __name__ == "__main__":
    # Initialize analyzer
    data_path = '../../data/ekspor_mineral_indonesia_WITS.csv'
    analyzer = IndonesianMineralAnalyzer(data_path)
    
    # Run complete analysis
    success = analyzer.run_complete_analysis()
    
    if success:
        print("\n✅ Indonesian Mineral Export Analysis completed successfully!")
        print("🚀 Ready for strategic decision making and business optimization!")
    else:
        print("\n❌ Analysis failed. Please check data file and try again.")
