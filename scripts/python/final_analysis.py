#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Indonesian Mineral Export Analysis - Python 2.7 Compatible
Simple analysis without PySpark for initial data exploration
"""

import csv
import sys
from collections import defaultdict

def analyze_mineral_exports():
    """Analyze Indonesian mineral export data"""
    print("=== Indonesian Mineral Export Analysis ===")
    print("Loading data from CSV file...")
    
    # Data structures for analysis
    yearly_totals = defaultdict(float)
    country_totals = defaultdict(float)
    product_totals = defaultdict(float)
    yearly_country = defaultdict(lambda: defaultdict(float))
    yearly_product = defaultdict(lambda: defaultdict(float))
    
    total_records = 0
    valid_records = 0
    
    try:
        with open('/opt/spark/data/ekspor_mineral_indonesia_WITS.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                total_records += 1
                
                try:
                    year = int(row.get('Year', 0))
                    trade_value = float(row.get('Trade Value 1000USD', 0))
                    partner = row.get('Partner', '').strip()
                    product = row.get('Product Description', '').strip()
                    
                    if year > 0 and trade_value > 0 and partner and product:
                        valid_records += 1
                        
                        # Convert to millions for easier reading
                        trade_value_million = trade_value / 1000.0
                        
                        # Aggregate data
                        yearly_totals[year] += trade_value_million
                        country_totals[partner] += trade_value_million
                        product_totals[product] += trade_value_million
                        yearly_country[year][partner] += trade_value_million
                        yearly_product[year][product] += trade_value_million
                        
                except (ValueError, TypeError):
                    continue
                    
                if total_records % 10000 == 0:
                    print("Processed {} records...".format(total_records))
    
    except IOError as e:
        print("Error reading CSV file: {}".format(str(e)))
        return
    
    print("\n=== DATA SUMMARY ===")
    print("Total records processed: {}".format(total_records))
    print("Valid records for analysis: {}".format(valid_records))
    print("Data quality: {:.1f}%".format(100.0 * valid_records / total_records if total_records > 0 else 0))
    
    # Yearly trends analysis
    print("\n=== YEARLY EXPORT TRENDS ===")
    sorted_years = sorted(yearly_totals.keys())
    for year in sorted_years:
        print("Year {}: ${:.2f} million USD".format(year, yearly_totals[year]))
    
    # Top export destinations
    print("\n=== TOP 10 EXPORT DESTINATIONS ===")
    top_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (country, value) in enumerate(top_countries, 1):
        print("{}. {}: ${:.2f} million USD".format(i, country, value))
    
    # Top export products
    print("\n=== TOP 10 EXPORT PRODUCTS ===")
    top_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (product, value) in enumerate(top_products, 1):
        print("{}. {}: ${:.2f} million USD".format(i, product[:60], value))
    
    # Recent year analysis (last available year)
    if sorted_years:
        latest_year = max(sorted_years)
        print("\n=== ANALYSIS FOR YEAR {} ===".format(latest_year))
        
        latest_countries = sorted(yearly_country[latest_year].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
        print("Top 5 destinations in {}:".format(latest_year))
        for i, (country, value) in enumerate(latest_countries, 1):
            print("{}. {}: ${:.2f} million USD".format(i, country, value))
        
        latest_products = sorted(yearly_product[latest_year].items(), 
                               key=lambda x: x[1], reverse=True)[:5]
        print("\nTop 5 products in {}:".format(latest_year))
        for i, (product, value) in enumerate(latest_products, 1):
            print("{}. {}: ${:.2f} million USD".format(i, product[:40], value))
    
    # Growth analysis
    if len(sorted_years) >= 2:
        print("\n=== GROWTH ANALYSIS ===")
        first_year = sorted_years[0]
        last_year = sorted_years[-1]
        
        first_value = yearly_totals[first_year]
        last_value = yearly_totals[last_year]
        
        if first_value > 0:
            growth_rate = ((last_value - first_value) / first_value) * 100
            print("Total growth from {} to {}: {:.1f}%".format(
                first_year, last_year, growth_rate))
            
            years_span = last_year - first_year
            if years_span > 0:
                avg_annual_growth = (pow(last_value / first_value, 1.0 / years_span) - 1) * 100
                print("Average annual growth rate: {:.1f}%".format(avg_annual_growth))
    
    print("\n=== ANALYSIS COMPLETE ===")
    print("Indonesian mineral export analysis finished successfully!")

if __name__ == "__main__":
    analyze_mineral_exports()
