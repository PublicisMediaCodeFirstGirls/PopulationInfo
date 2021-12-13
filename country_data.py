import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# convert raw data to float and convert the percentages
def convert_column_to_float(pop_data, column_list):
    for i in column_list:
        pop_data[i] = pop_data[i].astype("float")
    return pop_data


def convert_percentage(pop_data, column_list):
    for i in column_list:
        pop_data.loc[:, i] /= 100
    return pop_data


# input csv file whilst removing the N.A. and %
df = (
    pd.read_csv("population_by_country_2020.csv")
    .replace("N.A.", None)
    .replace("%", "", regex=True)
)

# assigning the columns into the float and percentage functions
df = convert_column_to_float(df, ["Yearly Change", "Fert. Rate", "Med. Age", "Urban Pop %", "World Share"])
df = convert_percentage(df, ["Yearly Change", "Urban Pop %", "World Share"])

# List of each column results
country = df["Country (or dependency)"]
population = df["Population (2020)"]
pop_growth = df["Yearly Change"]
net_pop_growth = df["Net Change"]
density = df["Density (P/Km²)"]
land_area = df["Land Area (Km²)"]
migration = df["Migrants (net)"]
fertility = df["Fert. Rate"]
age = df["Med. Age"]
urban_pop = df["Urban Pop %"]
world_share = df["World Share"]

# Countries sorted in alphabetical order
sorted_country = sorted(country)


migration_per_capita = migration / population * 100
df["Migration_Per_Capita"] = migration_per_capita

for index, row in df.iterrows():
    if row['Med. Age'] == "N.A.":
        df['Med. Age'].replace(to_replace="N.A.",value=0, inplace=True)

df['Med. Age'] = pd.to_numeric(df['Med. Age'])


# Get each detail for a selected country
class CountryDetails:
    def __init__(self, chosencountry):
        self.__chosen_country = chosencountry

    def population(self):
        country_population = (population[country == self.__chosen_country]).iloc[0]
        return country_population

    def yearly_change(self):
        country_yearly_change = (pop_growth[country == self.__chosen_country]).iloc[0]
        return f'{country_yearly_change:.1%}'

    def net_change(self):
        country_net_change = (net_pop_growth[country == self.__chosen_country]).iloc[0]
        return country_net_change

    def density(self):
        country_density = (density[country == self.__chosen_country]).iloc[0]
        return country_density

    def land_area(self):
        country_land_area = (land_area[country == self.__chosen_country]).iloc[0]
        return country_land_area

    def migrants(self):
        country_migrants = (migration[country == self.__chosen_country]).iloc[0]
        return country_migrants

    def fert_rate(self):
        country_fert_rate = (fertility[country == self.__chosen_country]).iloc[0]
        return country_fert_rate

    def med_age(self):
        country_med_age = (age[country == self.__chosen_country]).iloc[0]
        return country_med_age

    def urban_pop(self):
        country_urban_pop = (urban_pop[country == self.__chosen_country]).iloc[0]
        return f'{country_urban_pop:.1%}'

    def world_share(self):
        country_world_share = (world_share[country == self.__chosen_country]).iloc[0]
        return f'{country_world_share:.1%}'


class CountriesData:
    @staticmethod
    def heat_map():
        img = df.corr()
        print(img)
        # Creating a Heat Map
        fig, ax = plt.subplots()
        im = ax.imshow(df.corr().abs(), cmap="hot")
        ax.set_xticks(np.arange(df.shape[1] - 1))
        ax.set_yticks(np.arange(df.shape[1] - 1))
        ax.set_xticklabels(df.columns[1:])
        ax.set_yticklabels(df.columns[1:])
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=25, ha="right", rotation_mode="anchor")
        ax.set_title("Country Statistic Correlation Heatmap")
        heat_map_chart = 'static/heat_map.png'
        plt.savefig(heat_map_chart)
        return heat_map_chart

    @staticmethod
    def chart1():
        df.head(25)[['Country (or dependency)', 'Migration_Per_Capita']].plot.bar(x='Country (or dependency)')
        plt.ylabel("Migrants (in/out) / Population")
        plt.title("Migration rate, top 25 most populous countries")
        plt.suptitle("Data demonstrates the highest levels of immigration occur in Germany, the UK, Turkey and the USA")
        chart1_chart = 'static/chart1.png'
        plt.savefig(chart1_chart)
        return chart1_chart

    @staticmethod
    def chart2():
        df.head(25)[['Country (or dependency)', 'Migration_Per_Capita', 'Yearly Change']].plot.bar(
            x='Country (or dependency)', secondary_y='Yearly Change')
        plt.ylabel("Migrants (in/out) / Population")
        plt.title("Migration rate and population growth, top 25 most populous countries")
        plt.suptitle(
            "However, those countries with the highest migration rate are not experiencing heavy population growth")
        chart2_chart = 'static/chart2.png'
        plt.savefig(chart2_chart)
        return chart2_chart

    @staticmethod
    def chart3():
        df.head(25)[['Migration_Per_Capita', 'Med. Age']].plot.scatter(x='Migration_Per_Capita', y='Med. Age')
        plt.ylabel("Average Age")
        plt.xlabel("Migrants (in/out) / Population")
        plt.title("Migration rate vs. average age of population, top 25 most populous countries")
        plt.suptitle("In fact, those countries with the highest migration rate have ageing populations, and are therefore in need of migrants of working age")
        chart3_chart = 'static/chart3.png'
        plt.savefig(chart3_chart)
        return chart3_chart
