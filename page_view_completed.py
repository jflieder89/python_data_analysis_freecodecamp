import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

df = pd.read_csv('fcc-forum-pageviews.csv')
# print(df.head())
# print(df.info())
df.date = pd.to_datetime(df['date']) #set date column to be in datetime format for later slicing
# print(df.info())
df.set_index('date', inplace = True) #inplace = True makes it permanent
# print(df.head())
# print(df.index) #can't do print(df.date) now that date is now the index

#set the low 2.5% and high 2.5% both off of the original df! Don't do it sequentially or else you'll change it! The highest 2.5% of the original df is different that the highest 2.5% of a df with the bottom 2.5% already removed!
# print(df.value.quantile(q=0.025))
value_too_low = df.value.quantile(q=0.025)
# print(df.value.quantile(q=0.975))
value_too_high = df.value.quantile(q=0.975)
# print()

##Now remove the rows with value in the lowest 2.5% of the data frame
df_value_too_low = df[ df.value < value_too_low ].index
#print(df_value_too_low) #only print after removing .index from this df's assignment
# print(df.shape)
# print(df[ df.value < value_too_low ].shape) #can't have .index in there when printing any of it
df.drop(df_value_too_low, inplace = True)
# print(df.shape)
# print()

##Now remove the rows with value in the highest 2.5% of the data frame
df_value_too_high = df[ df.value > value_too_high ].index
#print(df_value_too_high) #only print after removing .index from this df's assignment
# print(df.shape)
# print(df[ df.value > value_too_high ].shape) #can't have .index in there when printing any of it
df.drop(df_value_too_high, inplace = True)
# print(df.shape)

##Next is line chart function using MatPlotLib to create figure1
def draw_line_plot(data_frame):
  data_frame.plot(figsize=(16, 6), color="red", legend=None) #figsize parameters are (width, height). Trial and error got it to match the example figure1's size.
  plt.xlabel("Date", fontsize = 12)
  plt.ylabel("Page Views", fontsize = 12)
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize = 20)
  plt.xticks(rotation = 0, horizontalalignment='center') #set xtick labels to get them horizontal. Trial and error on the number. Also center the labels on the tick marks
  #plt.show()
  plt.savefig('line_plot.png')

##Next is bar plot function to create figure2
def draw_bar_plot(data_frame):
  ## First need to get monthly data from the dataframe
  ##The way I found to do this requires to create month lists containing the desired averages for each year
  #print(df.head(15))
  ##Create a new data frame grouped by month. !!Need to go off  of a version of original dataframe that does not have date column set as index!!:
  df_month = data_frame.reset_index().groupby(pd.Grouper(key='date', axis=0, freq='M')).mean()
  #print(df_month.head(15))
  #Now try to find a clever way to get month lists without doing it manually for giggles:
  df_jan = df_month.filter(like = '-01-', axis=0) #dataframe with only the january averages
  jan = df_jan.value.tolist() #list of the january averages
  df_feb = df_month.filter(like = '-02-', axis=0)
  feb = df_feb.value.tolist()
  df_mar = df_month.filter(like = '-03-', axis=0)
  mar = df_mar.value.tolist()
  df_apr = df_month.filter(like = '-04-', axis=0)
  apr = df_apr.value.tolist()
  df_may = df_month.filter(like = '-05-', axis=0)
  may = df_may.value.tolist()
  df_jun = df_month.filter(like = '-06-', axis=0)
  jun = df_jun.value.tolist()
  df_jul = df_month.filter(like = '-07-', axis=0)
  jul = df_jul.value.tolist()
  df_aug = df_month.filter(like = '-08-', axis=0)
  aug = df_aug.value.tolist()
  df_sep = df_month.filter(like = '-09-', axis=0)
  sep = df_sep.value.tolist()
  df_oct = df_month.filter(like = '-10-', axis=0)
  oct = df_oct.value.tolist()
  df_nov = df_month.filter(like = '-11-', axis=0)
  nov = df_nov.value.tolist()
  df_dec = df_month.filter(like = '-12-', axis=0)
  dec = df_dec.value.tolist()
  # print(df_sep)
  # print(df_oct)
  # print(df_nov)
  # print(df_dec)
  # print(sep)
  # print(oct)
  # print(nov)
  # print(dec)
  ##Going to add zero values at the beginning of Jan   through Apr lists since they have no 2016 data but the rest of the months do. I tired None values instead but that messed up the plotting
  #print(jan)
  jan.insert(0, 0)
  #print(jan)
  feb.insert(0, 0)
  mar.insert(0, 0)
  apr.insert(0, 0)
  bar_width = 0.05 #set a width to be used to dictate each bar width. Trial and error.
  fig = plt.subplots(figsize =(12, 8)) #Trial and error plus internet search help to get the right sized figure. Pick it and stick with it then adjust the x axis stuff later! BTW changing it to 16, 9 did not mess up centering of ticks.
  #Now set up the bar offsets between the months. I will offset them the same amount as the bar widths so they will be touching:
  bar_jan = list(range(4))
  bar_feb = [x + bar_width for x in bar_jan]
  bar_mar = [x + bar_width for x in bar_feb]
  bar_apr = [x + bar_width for x in bar_mar]
  bar_may = [x + bar_width for x in bar_apr]
  bar_jun = [x + bar_width for x in bar_may]
  bar_jul = [x + bar_width for x in bar_jun]
  bar_aug = [x + bar_width for x in bar_jul]
  bar_sep = [x + bar_width for x in bar_aug]
  bar_oct = [x + bar_width for x in bar_sep]
  bar_nov = [x + bar_width for x in bar_oct]
  bar_dec = [x + bar_width for x in bar_nov]
  
  ##Now plot the bars for each month:
  plt.bar(bar_jan, jan, color ='blue', width = bar_width, edgecolor ='grey', label ='January')
  plt.bar(bar_feb, feb, color ='orange', width = bar_width, edgecolor ='grey', label ='February')
  plt.bar(bar_mar, mar, color ='green', width = bar_width, edgecolor ='grey', label ='March')
  plt.bar(bar_apr, apr, color ='red', width = bar_width, edgecolor ='grey', label ='April')
  plt.bar(bar_may, may, color ='purple', width = bar_width, edgecolor ='grey', label ='May')
  plt.bar(bar_jun, jun, color ='brown', width = bar_width, edgecolor ='grey', label ='June')
  plt.bar(bar_jul, jul, color ='pink', width = bar_width, edgecolor ='grey', label ='July')
  plt.bar(bar_aug, aug, color ='grey', width = bar_width, edgecolor ='grey', label ='August')
  plt.bar(bar_sep, sep, color ='yellow', width = bar_width, edgecolor ='grey', label ='September')
  plt.bar(bar_oct, oct, color ='deepskyblue', width = bar_width, edgecolor ='grey', label ='October')
  plt.bar(bar_nov, nov, color ='navy', width = bar_width, edgecolor ='grey', label ='November')
  plt.bar(bar_dec, dec, color ='darkorange', width = bar_width, edgecolor ='grey', label ='December')
  
  plt.xlabel('Years', fontsize = 12)
  plt.ylabel('Average Page Views', fontsize = 12)
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize = 20)
  tick_space = 0.275 #trial and error. Use the bar_width as a measurement tool to adjust! Want to get the tick mark in between the 6th and 7th months: June and July.
  plt.xticks([n + tick_space for n in bar_jan],
        ['2016', '2017', '2018', '2019'])
  plt.legend()
  plt.savefig('bar_plot.png')

##Next is box plot function from Seaborn to create figure3
def draw_box_plot(data_frame):
  #since I'm using seaborn and data frames as per the instructions of the assignment, I'll create new columns in the data frame that identify the year and month of the row. Otherwise, if I could use regular boxplot or plt.box, I'd create a list of year lists containing the page views of each day of each year. something like this: 
  #df_2016 = df.filter(like = '2016', axis=0) #dataframe with only the 2016 page views. Then use tolist() method to make to list of that year's page views. then add to list of year lists: lst_year = [lst_2016, lst_2017, etc.]
  # print(data_frame.head())
  data_frame.reset_index(inplace=True) #This gave me an easier time working with the date column. Remember inplace= True!!
  # print(data_frame.head())
  data_frame['month'] = 0 #create empty column for months at first
  data_frame['year'] = 0 #create empty column for years at first
  # print(data_frame.head())
  # print(data_frame.tail())
  data_frame['year'] = pd.DatetimeIndex(df['date']).year #Glad I found this online, this is way easier than some other ways I tried to fill in these new columns
  # print(data_frame.head())
  # print(data_frame.tail())
  data_frame['month'] = pd.DatetimeIndex(df['date']).month
  # print(data_frame.head())
  # print(data_frame.tail())
  
  ##Here is the plt.subplot way of graphing it all:
  fig = plt.subplots(figsize =(24, 9))#Trial and error with sizes especially with both graphs being plotted
  plt.subplot(1, 2, 1) #(rows, columns, panel selected)
  sns.boxplot(x="year", y="value", data=data_frame)
  plt.xlabel( "Year", size = 14 ) # Trial and error with the sizes
  plt.ylabel( "Page Views", size = 14 )
  plt.title( "Year-wise Box Plot (Trend)", size = 18 )
  plt.subplot(1, 2, 2)
  sns.boxplot(x="month", y="value", data=data_frame)
  plt.xlabel( "Month", size = 14 ) # Trial and error with the sizes
  plt.ylabel( "Page Views", size = 14 )
  plt.title( "Month-wise Box Plot (Seasonality)" , size = 18 )
  plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['Jan','Feb','Mar','Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) #Change the default x ticks from numbers -starting with zero- to the desired shortened month names
  plt.savefig('box_plot.png')
  
  ##I gave a quick try to do the plot_objects method with the following syntax but kept getting the plots on top of each other on the right subplot. I think maybe the seaborn aspect of the boxplot preventing ax1.boxplot... and instead requiring ax1 = sns.boxplot... is messing it up somehow:
  # plot_objects = plt.subplots(nrows=1, ncols=2, figsize=(24, 9))
  # ax1 = sns.boxplot(x="year", y="value", data=data_frame)
  # ax2 = sns.boxplot(x="month", y="value", data=data_frame)
  # fig, (ax1, ax2) = plot_objects
  # plt.savefig('box_plot.png')

  
draw_line_plot(df) ## to get figure1 line plot
draw_bar_plot(df) ## to get figure 2 bar plot
draw_box_plot(df) ## to get figure 3 box plot