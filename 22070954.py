# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 22:25:59 2023

@author: sai
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import colors
# Load data
military_df = pd.read_csv("militarybudjet.csv", skiprows=4)
gdp_df = pd.read_csv("economist.csv", skiprows=4)
mortality_df = pd.read_csv("child_mortality.csv", skiprows=4)
poverty_df = pd.read_csv("poverty_headcount.csv", skiprows=4)
plt.rcParams.update({'axes.facecolor':'white'})


# Select the top four countries by military expenditure
top_countries = ['United States', 'India', 'China', 'Russian Federation', '']
df_top = military_df[military_df['Country Name'].isin(top_countries)][['Country Name', '2019']]
world_total = military_df['2019'].sum()
top_total = df_top['2019'].sum()
percentages = df_top['2019'] / top_total * 100

# Extract the GDP per capita data from 2000 to 2020 with 5 years interval
countries = ["India", "China", "United States", "Russian Federation", "Brazil", "United Kingdom"]
years = [str(year) for year in range(2000, 2021, 5)]
gdp_data = gdp_df[gdp_df["Country Name"].isin(countries)][["Country Name"] + years]
gdp_data = gdp_data.set_index("Country Name")

# Select the desired countries and years for mortality rate under 5
years = range(2000, 2021, 5)
subset = mortality_df.loc[mortality_df["Country Name"].isin(countries), ["Country Name"] + [str(year) for year in years]]
subset.set_index("Country Name", inplace=True)
subset = subset.transpose()

# Prepare poverty headcount ratio data for histogram
poverty_df = poverty_df.set_index("Country Name")
dropped_df = poverty_df.loc[:, "2000":"2021"]
filtered_df = dropped_df.dropna(axis=0, how="all")
mean_pov_ratio = filtered_df.mean(skipna=True, numeric_only=True)

# Set up grid layout
fig = plt.figure(figsize=(16, 8), dpi=300)
fig.suptitle('Defending Childhood: Balancing Military Spending Impact', fontsize=25, fontweight='bold',color='green')

gs = gridspec.GridSpec(nrows=2, ncols=3, figure=fig, wspace=0.3, hspace=0.4)

# Pie chart for military expenditure
ax1 = fig.add_subplot(gs[0, 0])
explode = (0.1, 0.1, 0.1, 0.1)
ax1.pie(percentages, labels=df_top['Country Name'], autopct='%1.1f%%',explode=explode)
ax1.set_title('Military Expenditure of Top Four Countries in 2019',color='r')

# Bar chart for GDP per capita
ax2 = fig.add_subplot(gs[0, 1])
gdp_data.plot(kind="bar", rot=0, ax=ax2)
ax2.set_title("GDP per capita (current US$) from 2000 to 2020",color='r')
ax2.set_xlabel("Country")
ax2.set_ylabel("GDP per capita (current US$)",color='r')
ax2.legend(title="Year",facecolor="snow")
plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')

# Line chart for mortality rate under 5
ax3 = fig.add_subplot(gs[1, 1])
subset.plot(kind="line", ax=ax3)
ax3.set_title("Mortality rate under 5 from 2000 to 2020",color='r')
ax3.set_xlabel("Year")
ax3.set_ylabel("Mortality rate under 5 (per 1,000 live births)",color='r')
ax3.legend(title="Country",prop={"size":8},facecolor="snow")

# Histogram for mean poverty headcount ratio worldwide
ax4 = fig.add_subplot(gs[1, 0])
N, bins,patches=ax4.hist(mean_pov_ratio, bins=20)
fracs = N / N.max()

# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Now, we'll loop through our objects and set the color of each accordingly

for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)
ax4.set_xlabel('Mean Poverty Headcount Ratio Worldwide')
ax4.set_ylabel('Frequency',color='r')
ax4.set_title('Histogram of Mean Poverty Headcount Ratio',color='r')
box_style=dict(boxstyle='round', facecolor='thistle', alpha=0.5)
left = 1.5
width = 0.9
bottom  = 1.1
height = 0.9
right = left + width
top = bottom + height
ax = plt.gca()
# Transform axes

ax.set_transform(ax.transAxes)

fig.text(right, top, 'The comprehension of the relationships\nbetween the effects on various countries\n worldwide between military spending,\nGDP per capita, the death rate under 5, \nand the mean poverty ratio.The statistics\n makes it abundantly evident that the\n nations with the highest GDP per capita, \nlowest death rate under 5, and lowest \nmean poverty ratio are also those with \nthe largest military spending. This \nsuggests that nations with greater \nmilitary spending are also those with\ngreater capacity to invest in their \ncitizens, offering them greater access \nto economic, healthcare, and educational \npossibilities. Fostering a wealthy and \nhealthy society requires striking a \nbalance between human growth and national \n security. Sustainable development also \ndepends on balanced resource allocation. \nThis strategy boosts the countries overall \nresilience and promotes long-term stability.\nIt is evident that India experienced a 94%\nspike in mortality rate and the United States\nexperienced a 60% fall in military expenditure.',
        horizontalalignment='left',
        verticalalignment='top',
        bbox=box_style,
        size=13,
        color='blue',
        transform=ax.transAxes)

# Add student name and student ID
plt.figtext(2.5, 2.4, 'Student Name: Sai Kalyan Boyapati\nstudent ID: 22070954',
        horizontalalignment='left',
        verticalalignment='top',
        bbox=box_style,
        size=13.3,
        color='indigo',
        transform=ax.transAxes)

fig.patch.set_facecolor('lightyellow')

plt.savefig("22070954.png",dpi=300)
