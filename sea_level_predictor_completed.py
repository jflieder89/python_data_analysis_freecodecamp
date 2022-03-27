import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
  df = pd.read_csv('epa-sea-level.csv')
  # print(df.head())

  # Create scatter plot of CSIRO Adjusted Sea Level data
  plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

  # Create first line of best fit
  slope1, intercept1, r_value1, p_value1, stderr1 = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
  # print(linregress(df['Year'], df['CSIRO Adjusted Sea Level']))
  # print(slope)
  # print(intercept)
  
  start_year = int(df.iloc[0]['Year'])
  # print(start_year)
  fit1_x = list(range(start_year, 2051, 1)) #range(start, end + 1, interval)
  # print(fit1_x)
  ##Can't multiply list of integers by a float! Need to multiply each element of the list by the float individually
  fit1_y = [] #create list to append values into
  for item in fit1_x:
    fit1_y.append( (item * slope1) + intercept1)
  # print(fit1_y)
  print(len(fit1_x))
  print(len(fit1_y))
  plt.plot(fit1_x, fit1_y, color='y', linestyle='dashed')

  # Create second line of best fit
  df_new = df[df['Year'] >= 2000]
  # print(df_new)
  slope2, intercept2, r_value2, p_value2, stderr2 = linregress(df_new['Year'], df_new['CSIRO Adjusted Sea Level'])
  fit2_x = list( range(2000, 2051, 1) ) #range (start, stop + 1, interval)
  # print(fit2_x)
  #print(type(fit2_x[0]))
  # fake = [0, 1, 2, 3, 4, 5]
  # print(fake * 2)
  # print(fake * 2.5)
  
  #print(type(slope2))
  #slope2 = float(slope2) # to make it not a numpy.float64, which gets messed up when plotting
  #print(type(slope2))
  #intercept2 = float(intercept2)
  fit2_y = [] #Create empty list to append values into for y variable
  ##Can't multiply list of integers by a float! Need to multiply each element of the list by the float individually
  for item in fit2_x:
    fit2_y.append( (item * slope2) + intercept2)
  # print(fit2_x)
  # print(fit2_y)
  # print(len(fit2_x))
  # print(len(fit2_y))
  plt.plot(fit2_x, fit2_y, color='r', linestyle='dotted')

  # Add labels and title
  plt.xlabel('Year')
  plt.ylabel('Sea Level (inches)')
  plt.title('Rise in Sea Level')

    
  # Save plot and return data for testing (DO NOT MODIFY)
  plt.savefig('sea_level_plot.png')
  #return plt.gca()
draw_plot()