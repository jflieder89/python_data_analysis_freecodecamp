# This entrypoint file to be used in development. Start by reading README.md
# import demographic_data_analyzer
# from unittest import main

# # Test your function by calling it here
# demographic_data_analyzer.calculate_demographic_data()

# # Run unit tests automatically
# main(module='test_module', exit=False)
import pandas as pd

def calculate_demographic_data(print_data=True):
  # Read data from file and clean it up
  df = pd.read_csv('adult.data.csv', 
  na_values = ['', '?', '-', '--', 'NaN'] )
  #print(df.head())
  #print(df.info) #this gives rows and column amounts plus the whole file
  #print(df.shape) #this gives dimensions: (rows, columns) in this case
  #print(pd.isnull(df).sum()) #see how many null values exist in each column
  ##Clean null data with a forward fill and axis=0 means filling down the columns instead axis=1 which fills across the rows:
  df = df.fillna(method='ffill', axis=0)
  #print(pd.isnull(df).sum()) #see how many null values exist in each column
  ##I don't see any decimals, but here is how I'd round them to the nearest tenth. This is just for one column:
  ##df.loc[df['age'] == float, 'age'] = round(df.loc[df['age'] == float, 'age'], 1)
  #Replace all hyphens with underscores instead. This will help with counting up amounts later on:
  df = df.replace('-','_', regex=True)

  # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
  #print(df['race'].count()) #count up all items in the column
  #print(df['race'].value_counts()) #this gives a table of what I'm looking for (the counts of each entry value).
  #print(df.race.value_counts().White) # To get count of an individual value of a column
  race_count = pd.Series([(df.race.value_counts().White), (df.race.value_counts().Amer_Indian_Eskimo), (df.race.value_counts().Black), (df.race.value_counts().Asian_Pac_Islander), (df.race.value_counts().Other)
  ])
  race_count.index = ['White', 'Amer-Indian-Eskimo', 'Black', 'Asian-Pac-Islander', 'Other']
  race_count = race_count.to_string() # to remove the dtype at the bottom!
  #print(race_count) 

  # What is the average age of men?
  df_only_men = df.loc[df['sex'] == 'Male'] #create new dataframe with only men included
  #print(df_only_men.head(10))
  #print(df_only_men.describe()) #this give some info, including what I'm looking for
  #print(df_only_men['age'].mean())
  average_age_men = df_only_men['age'].mean()

  # What is the percentage of people who have a Bachelor's degree?
  #print(df['education'].count()) #count up all items in the column
  df_only_bachelors = df.loc[df['education'] == 'Bachelors']
  #print(df_only_bachelors['education'].head())
  #print(df_only_bachelors['education'].count()) #count up all items in the column
  percentage_bachelors = round((df_only_bachelors['education'].count() / df['education'].count()) * 100, 1) # round to the nearest tenth!
  #print(percentage_bachelors)

  #What percentage of people with advanced education (`Bachelors`, Masters`,or `Doctorate`) make more than 50K?
  #Here is the syntax for filtering for multiple values of a column. Need to use pipes instead of 'or' written out:
  df_higher_ed = df[ (df.education == 'Bachelors') | (df.education == 'Masters') | (df.education == 'Doctorate')]
  #print(df_higher_ed.head(20))
  #print(df_higher_ed['education'].count()) #to all count higher educated
  #print((df_higher_ed[df_higher_ed.salary == '>50K']).head())
  df_higher_ed_rich = (df_higher_ed[df_higher_ed.salary == '>50K'])
  #print(df_higher_ed_rich['salary'].count()) #to count rich higher educated
  higher_ed_rich = round((df_higher_ed_rich['salary'].count() / df_higher_ed['education'].count()) * 100, 1)
  #print(higher_ed_rich)
  ##other method to filter for higher educated could be something like this:
  # filter_list = ['Bachelors', 'Masters', 'Doctorate']
  # df[df.education.isin(filter_list)]

  # What percentage of people without advanced education make more than 50K?
  df_lower_ed = df[ (df.education != 'Bachelors') & (df.education != 'Masters') & (df.education != 'Doctorate')]
  #print(df_lower_ed['education'].count()) #to all count higher educated
  #print(df_lower_ed.head(20))
  df_lower_ed_rich = (df_lower_ed[df_lower_ed.salary == '>50K'])
  #print(df_lower_ed_rich['salary'].count()) #to count rich lower educated
  lower_ed_rich = round((df_lower_ed_rich['salary'].count() / df_lower_ed['education'].count()) * 100, 1)
  #print(lower_ed_rich)
  ##other method to filter for lower educated could be something like this:
  # filter_list = ['Bachelors', 'Masters', 'Doctorate']
  # df[~df.education.isin(filter_list)]

  # What is the minimum number of hours a person works per week (hours-per-week feature)?
  #print(df['hours-per-week'].min())
  min_work_hours = df['hours-per-week'].min()

  # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
  df_min_workers = df[ df['hours-per-week'] == min_work_hours ]
  #print(df_min_workers.head())
  num_min_workers = df_min_workers['hours-per-week'].count() #to get total number of people working the min hours
  #print(num_min_workers) 
  df_num_min_workers_rich = df_min_workers[df_min_workers.salary == '>50K' ]
  #print(df_num_min_workers_rich.head())
  num_min_workers_rich = df_num_min_workers_rich['salary'].count() #to get number of rich people working the minimin hours
  #print(num_min_workers_rich)
  rich_percentage = round( (num_min_workers_rich / num_min_workers) * 100, 1)
  #print(rich_percentage)

  # What country has the highest percentage of people that earn >50K?
  df_higher_earn =  df[df.salary == '>50K']
  #print(df_higher_earn.head(25))
  higher_earn_amount = df_higher_earn['native-country'].count() #to get total amount of rich people
  #print(higher_earn_amount)
  #print(df_higher_earn['native-country'].value_counts()) #this gives the full breakdown of how many high earners are from each country
  df_high_earn_country_amount = df_higher_earn[ df_higher_earn['native-country'] == 'United_States']
  #print(df_high_earn_country_amount.head(25))
  high_earn_country_amount = df_high_earn_country_amount['native-country'].count()
  #print(high_earn_country_amount) #this gives the amount of high earners spcifically from the country with the highest amount of earners
  # print(higher_earn_amount) 
  # print(df_higher_earn['native-country'].count())
  # print(df_higher_earn['native-country'].mode()) #this gives me the country with the most amount of high earners, but in object form which is hard to work with
  # print(df_higher_earn['native-country'].value_counts().idxmax()) #this syntax returns the country with the highest amount of high earners in a more manageable form
  # print(type(df_higher_earn['native-country'].value_counts().idxmax()))
  highest_earning_country = df_higher_earn['native-country'].value_counts().idxmax()
  #print(highest_earning_country)
  highest_earning_country_percentage = round( (high_earn_country_amount / higher_earn_amount) * 100, 1)
  #print(highest_earning_country_percentage)

  # Identify the most popular occupation for those who earn >50K in India.
  df_india_rich = df[ (df['native-country'] == 'India') & (df['salary'] == '>50K')]
  #print(df_india_rich['occupation'].head(10))  
  top_IN_occupation = (df_india_rich['occupation'].value_counts().idxmax())
  #print(top_IN_occupation)
  
  return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_ed_rich,
        'lower_education_rich': lower_ed_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

calculate_demographic_data()