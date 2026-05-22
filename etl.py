import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
sns.set_theme(style="whitegrid", palette="pastel")
from sqlalchemy import create_engine
def plot_bar(df, x_col, y_col, title, xlabel, ylabel, filename, color='teal'):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col], color=color, edgecolor='black')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
df_r=pd.read_csv('FAO.csv',encoding='latin-1')
#تنظيف البيانات
years = [f'Y{year}' for year in range(2000, 2014)]
df_r[years] = df_r[years].apply(pd.to_numeric, errors='coerce')
connection_string = "mssql+pyodbc://localhost\SQLEXPRESS/AgricultureDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)
df_r.to_sql('agro_table', con=engine, if_exists='replace', index=False)
query = """
SELECT TOP 5 
    Area, 
    (
        (SUM(Y2005 + Y2006 + Y2007 + Y2008 + Y2009) / 5.0) - (SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004) / 5.0)
    ) / (SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004) / 5.0) * 100.0 AS Growth_Percentage_Rate
FROM agro_table 
GROUP BY Area
HAVING SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004) > 0
ORDER BY Growth_Percentage_Rate DESC;
"""
df = pd.read_sql(query, con=engine)  
# الرسمة الأولى
plot_bar(df, 'Area', 'Growth_Percentage_Rate',
         'Top 5 Fastest-Growing Agricultural Economies (2000-2009)',
         'Country', 'Growth Rate (%)', color='teal')
#----------------------------------------
print('__________________________________________' )
# ==============================================================================
# الخطوة 2: رسم أعلى 5 دول في الإنتاج لعام 2013 (استعلام)
# ==============================================================================
query_top_2013 = """
SELECT TOP 5 Area, SUM(Y2013) AS total_producut2_2013 
FROM agro_table 
GROUP BY Area 
ORDER BY total_producut2_2013 DESC;
"""
df_top_2013 = pd.read_sql(query_top_2013, con=engine)

plot_bar(df_top_2013, 'Area', 'total_producut2_2013',
         'Top 5 Global Agricultural Producers in 2013',
         'Country', 'Production Volume (Tons)', color='#1f77b4')

# ==============================================================================
# ا: حساب إجمالي إنتاج دولة غانا لعام 2013 
# ==============================================================================
query_ghana = """
SELECT Area, SUM(Y2013) as total_production_2013 
FROM agro_table 
WHERE area ='Ghana' 
GROUP BY Area;
"""
df_ghana = pd.read_sql(query_ghana, con=engine)

print("\n" + "="*60)
print(" AGRICULTURAL REPORT: KEY PERFORMANCE INDICATORS (KPIs)")
print("="*60)

if not df_ghana.empty:
    ghana_total = df_ghana['total_production_2013'].values[0]
    print(f" Ghana Total Agricultural Production (2013): {ghana_total:,.2f} Tons")
else:
    print(" No data found for Ghana in 2013.")
print("="*60 + "\n")
# ==============================================================================
# مقارنة فترات أمريكا باستخدام ـ Lollipop Chart
# ==============================================================================
query_usa = """
SELECT Area, 
       SUM(Y2000+Y2001+Y2002+Y2003+Y2004) AS production2000TO2004,
       SUM(Y2005+Y2006+Y2007+Y2008+Y2009) AS production2005TO2009
FROM agro_table 
WHERE Area ='United States of America' 
GROUP BY Area;
"""
df_usa = pd.read_sql(query_usa, con=engine)
val_2000_2004 = df_usa['production2000TO2004'].values[0]
val_2005_2009 = df_usa['production2005TO2009'].values[0]
periods = ['Period: 2000-2004', 'Period: 2005-2009']
values = [val_2000_2004, val_2005_2009]
plt.figure(figsize=(7, 6))
min_val = min(values)
baseline = min_val * 0.98  
plt.ylim(bottom=baseline, top=max(values) * 1.01)
plt.vlines(x=periods, ymin=baseline, ymax=values, color='gray', alpha=0.7, linewidth=2.5)
plt.scatter(periods, values, color=['#1f77b4', 'crimson'], s=200, zorder=3, edgecolor='black')
for i, txt in enumerate(values):
    plt.text(periods[i], values[i] + (max(values) * 0.001), f'{txt:,.0f} Tons', 
             ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title('USA Agricultural Production Drop (Lollipop View)', fontsize=14, fontweight='bold')
plt.ylabel('Production Volume (Tons)', fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.4) 
plt.tight_layout()
plt.savefig('usa_lollipop_decline.png', dpi=300, bbox_inches='tight')
plt.show()
# ==============================================================================
#  أعلى 5 دول في التوسع السنوي المطلق (Top 5 Annual Expansion)
# ==============================================================================
query_top_expansion = """
SELECT TOP 5 Area, 
    SUM(Y2005 + Y2006 + Y2007 + Y2008 + Y2009)/5.0 - SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004)/5.0 AS averNet_Growth 
FROM agro_table 
GROUP BY Area
ORDER BY averNet_Growth DESC;
"""
df_top_expansion = pd.read_sql(query_top_expansion, con=engine)

plot_bar(df_top_expansion, 'Area', 'averNet_Growth',
         'Top 5 Global Leaders in Annual Agricultural Expansion',
         'Country', 'Average Net Growth (Tons)', color='forestgreen')
# ==============================================================================
#  أكثر 5 دول تراجعاً بنظام ال Diverging Chart والألوان المتدرجة
# ==============================================================================
query_bottom_decline = """
SELECT TOP 5 Area, 
    (SUM(Y2005 + Y2006 + Y2007 + Y2008 + Y2009)/5.0 - SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004)/5.0) AS averageof_Net_Growth 
FROM agro_table 
GROUP BY Area
HAVING ((SUM(Y2005 + Y2006 + Y2007 + Y2008 + Y2009) / 5.0) - (SUM(Y2000 + Y2001 + Y2002 + Y2003 + Y2004) / 5.0)) IS NOT NULL
ORDER BY averageof_Net_Growth ASC;
"""
df_bottom_decline = pd.read_sql(query_bottom_decline, con=engine)
plt.figure(figsize=(10, 5))
custom_reds = sns.color_palette("Reds_r", n_colors=len(df_bottom_decline))[0:5]
bars = plt.barh(df_bottom_decline['Area'], df_bottom_decline['averageof_Net_Growth'], 
                color=custom_reds, edgecolor='black', height=0.6)
plt.axvline(x=0, color='black', linestyle='-', linewidth=1.5)
for bar in bars:
    width = bar.get_width()
    plt.text(width - 130, bar.get_y() + bar.get_height()/2, f'{width:,.0f} Tons', 
             va='center', ha='right', fontsize=5, fontweight='bold', color='darkred')
plt.title('Top 5 Countries with Average Annual Production Decline', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Average Net Contraction (Tons)', fontsize=11)
plt.ylabel('Country', fontsize=11)
plt.gca().invert_yaxis() 
plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('top_5_production_decline.png', dpi=300, bbox_inches='tight')
plt.show()
# ==============
#  أكثر 10 محاصيل إنتاجاً (Global Top 10 Items)
years_sum = " + ".join([f"Y{year}" for year in range(2000, 2014)])
query_top_items = f"""
SELECT TOP 10 Item, 
       SUM({years_sum}) AS total_item_production
FROM agro_table 
GROUP BY Item
ORDER BY total_item_production DESC;
"""
df_items = pd.read_sql(query_top_items, con=engine)
plt.figure(figsize=(11, 6))
sns.barplot(data=df_items, 
            x='total_item_production', 
            y='Item', 
            palette='viridis', 
            edgecolor='black')
plt.title('Top 10 Globally Produced Agricultural Items (2000-2013)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Total Production Volume (Tons)', fontsize=11)
plt.ylabel('Agricultural Item', fontsize=11)
plt.grid(axis='x', linestyle='--', alpha=0.4)
for index, value in enumerate(df_items['total_item_production']):
    plt.text(value, index, f' {value:,.0f} Tons', 
             va='center', ha='left', fontsize=9, fontweight='bold', color='black')
plt.tight_layout()
plt.savefig('top_10_produced_items.png', dpi=300, bbox_inches='tight')
plt.show()
# ==============================================================================
# الارتباط لأعلى 5 محاصيل 
# ==============================================================================
top_crops = df_items['Item'].head(5).tolist()
df_filtered = df_r[df_r['Item'].isin(top_crops)]
years = [f'Y{year}' for year in range(2000, 2014)]
df_pivot = df_filtered.groupby('Item')[years].sum().transpose()
corr_matrix = df_pivot.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Dynamic Correlation Between Top 5 Agricultural Crops', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('crops_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
#____________________________ 
#علاقة التنوع بالانتاج 
#_______________________________
query_diversity = """
SELECT 
    Area,
    COUNT(DISTINCT Item) AS crop_diversity,
    SUM(Y2013) AS total_production_2013
FROM agro_table
GROUP BY Area
HAVING SUM(Y2013) > 0
"""
df_div = pd.read_sql(query_diversity, con=engine)
#نحسب الارتباط
correlation = df_div['crop_diversity'].corr(df_div['total_production_2013'])
print(f"Correlation: {correlation:.2f}")
Q99 = df_div['total_production_2013'].quantile(0.99)
df_clean = df_div[df_div['total_production_2013'] < Q99]
#نرسم توضيح

plt.figure(figsize=(9, 6))
plt.scatter(df_div['crop_diversity'], 
            df_div['total_production_2013'],
            alpha=0.6, color='teal', edgecolor='black', s=80)
z = np.polyfit(df_div['crop_diversity'], df_div['total_production_2013'], 1)
p = np.poly1d(z)
plt.plot(sorted(df_div['crop_diversity']), 
         p(sorted(df_div['crop_diversity'])), 
         "r--", linewidth=2, label=f'Correlation: {correlation:.2f}')

plt.title('Crop Diversity vs Total Production by Country', fontsize=13, fontweight='bold')
plt.xlabel('Number of Distinct Crops', fontsize=11)
plt.ylabel('Total Production (Tons)', fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig('crop_diversity_vs_production.png', dpi=300, bbox_inches='tight')
plt.show()
# ==============================================================
# أي سنة كانت الأسوأ والأفضل عالمياً؟
# ==============================================================
#هعمل قايمة فيها السنوات وانتاجيتهم
years = [f'Y{year}' for year in range(2000, 2014)]
yearly_totals = {
    year: df_r[year].sum() for year in years
}

# تحويل لـ DataFrame
df_years = pd.DataFrame(list(yearly_totals.items()), 
                         columns=['Year', 'Total_Production'])
df_years['Year'] = df_years['Year'].str.replace('Y', '')

# الأسوأ والأفضل
worst_year = df_years.loc[df_years['Total_Production'].idxmin()]
best_year  = df_years.loc[df_years['Total_Production'].idxmax()]

print(f" أسوأ سنة: {worst_year['Year']} - الإنتاج: {worst_year['Total_Production']:,.0f} طن")
print(f" أفضل سنة: {best_year['Year']}  - الإنتاج: {best_year['Total_Production']:,.0f} طن")

# ==============================================================
# الرسمة

colors = []
for val in df_years['Total_Production']:
    if val == worst_year['Total_Production']:
        colors.append('#e74c3c')   # أحمر للأسوأ
    elif val == best_year['Total_Production']:
        colors.append('#2ecc71')   # أخضر للأفضل
    else:
        colors.append('#3498db')   # أزرق للباقي

plt.figure(figsize=(12, 6))
bars = plt.bar(df_years['Year'], df_years['Total_Production'], 
               color=colors, edgecolor='black')
plt.bar(worst_year['Year'], worst_year['Total_Production'], 
        color='#e74c3c', edgecolor='black', label=f"Worst: {worst_year['Year']}")
plt.bar(best_year['Year'], best_year['Total_Production'], 
        color='#2ecc71', edgecolor='black', label=f"Best: {best_year['Year']}")
plt.title('Global Agricultural Production by Year (2000-2013)', 
          fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Production (Tons)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('global_production_by_year.png', dpi=300, bbox_inches='tight')
plt.show()