#%%

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Importing Data (266 rows, 104 cols)
corona_dataset_csv = pd.read_csv("./covid19_Confirmed_dataset.csv")

#Drop Lat and Long columns & combine states/provinces to just look at countries (187 rows/countries, 100 cols/dates)
corona_dataset_csv.drop(["Lat","Long"], axis=1, inplace=True)
corona_dataset_aggregated = corona_dataset_csv.groupby("Country/Region").sum()

#Import and Format our happiness data (drop unneeded cols)
happiness_report_csv = pd.read_csv("worldwide_happiness_report.csv")
unused_cols = ["Overall rank", "Score", "Generosity", "Perceptions of corruption"]
happiness_report_csv.drop(unused_cols, axis = 1, inplace=True)

happiness_report_csv.set_index("Country or region", inplace=True)

#Check infection sums over time
# corona_dataset_aggregated.loc["China"].plot()
# corona_dataset_aggregated.loc["Italy"].plot()
# corona_dataset_aggregated.loc["Spain"].plot()
# plt.legend()

#Checking maximums infection rates on graph
# print(corona_dataset_aggregated.loc["China"].diff().plot())
# print(corona_dataset_aggregated.loc["US"].diff().plot())
# print(corona_dataset_aggregated.loc["Italy"].diff().plot())

#Create new Array to hold our maximum rates
countries = list(corona_dataset_aggregated.index)
max_infection_rates = []

for c in countries :
  max_infection_rates.append(corona_dataset_aggregated.loc[c].diff().max())
corona_dataset_aggregated["Max Infection Rate"] = max_infection_rates

corona_data = pd.DataFrame(corona_dataset_aggregated["Max Infection Rate"])





#Using Inner join to join on name of country, join the happiness data to infection data
combined_data = corona_data.join(happiness_report_csv, how="inner")

combined_data.corr()
#GDP Chart
gdp_x = combined_data["GDP per capita"]
inf_rate_y = combined_data["Max Infection Rate"]
sns.scatterplot(gdp_x,np.log(inf_rate_y))
sns.regplot(gdp_x,np.log(inf_rate_y))
plt.savefig('GDPvInfectionRate.png')
plt.clf()

#Social Supp Chart
social_supp_x = combined_data["Social support"]
sns.scatterplot(social_supp_x, np.log(inf_rate_y))
sns.regplot(social_supp_x, np.log(inf_rate_y))
plt.savefig('SocialSupportvInfectionRate.png')
plt.clf()

#Life Expectancy Chart
life_exp_x = combined_data["Healthy life expectancy"]
sns.scatterplot(life_exp_x, np.log(inf_rate_y))
sns.regplot(life_exp_x, np.log(inf_rate_y))
plt.savefig('LifeExpvInfectionRate.png')

#Combined
plt.figure()
sns.scatterplot(gdp_x, np.log(inf_rate_y))
sns.regplot(gdp_x, np.log(inf_rate_y))

sns.scatterplot(social_supp_x, np.log(inf_rate_y))
sns.regplot(social_supp_x, np.log(inf_rate_y))

sns.scatterplot(life_exp_x, np.log(inf_rate_y))
sns.regplot(life_exp_x, np.log(inf_rate_y))
plt.savefig('ComparativeInfectionRate.png')

# %%
