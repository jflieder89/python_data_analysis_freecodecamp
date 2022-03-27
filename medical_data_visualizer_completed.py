# # This entrypoint file to be used in development. Start by reading README.md
# import medical_data_visualizer
# from unittest import main

# # Test your function by calling it here
# medical_data_visualizer.draw_cat_plot()
# medical_data_visualizer.draw_heat_map()

# # Run unit tests automatically
# main(module='test_module', exit=False)

## to be entered into command prompt on initial screen:
# py -m pip install numpy
# py -m pip install pandas
# py -m pip install matplotlib
# py -m pip install seaborn

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

df = pd.read_csv('medical_examination.csv')
#print(pd.isnull(df).sum())
#print(df.head())
# print(df.info())
#print(df.size)
# print(df.shape)
# print(df.describe())
#Add overweight column. This is going to involve iterating over the rows at some point:
df[['overweight']] = 0 #First put in the column to be full of zeros
#print(df.head())
# print(df.shape)

#Now iterate through the rows to calculate BMI and update overweight column if BMI > 25
#Generally: #df.loc[df[‘column’] condition, ‘new column name’] = ‘value if condition is met’
##DO NOT USE QUOTATION MARKS AROUND THE VALUES THAT YOU WANT TO CHANGE TO! THIS WILL MESS UP PLOTTING DOWN THE LINE DUE TO INTEGERS NOT BEING THE SAME AS STRINGS!!
df.loc[df['weight'] / ( (df['height'] / 100) ** 2) > 25, 'overweight'] = 1
#print(df.head(21))

#For cholesterol and gluc, normalize all good as 0 and all bad as 1. So set 1's to 0, then set 2's and 3's to 1. That order is important! Need to use pipes instead of 'or' written out. Use loc to iterate across rows
##DO NOT USE QUOTATION MARKS AROUND THE VALUES THAT YOU WANT TO CHANGE TO! THIS WILL MESS UP PLOTTING DOWN THE LINE DUE TO INTEGERS NOT BEING THE SAME AS STRINGS!!
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
#print(df.cholesterol.head(21))
df.loc[df['gluc'] == 1, 'gluc'] = 0
#print(df.gluc.head(21))
df.loc[ (df['cholesterol'] == 2) | (df['cholesterol'] == 3 ), 'cholesterol'] = 1
df.loc[ (df['gluc'] == 2) | (df['gluc'] == 3 ), 'gluc'] = 1
#print('Cholesterol: ', '\n', df.cholesterol.head(21))
#print('Gluc: ', '\n', df.gluc.head(21))

#Filter out when diastolic pressure is higher than systolic pressure (when (df['ap_lo'] >= df['ap_hi'])). Going to use the drop method.
df_bad_pressure_rows = df[ df['ap_lo'] >= df['ap_hi'] ].index #single out all rows for which the drop condition is present
#print(df.head())
#print(df_bad_pressure_rows.head()) #only print after removing .index from this df's assignment
# print(df.shape)
# print(df_bad_pressure_rows.shape)
df.drop(df_bad_pressure_rows, inplace = True) #inplace = True is needed to make the changes permanent to df
# print(df.shape)

#Filter out rows for which height is less than the 2.5th percentile
##set the 'too low' and 'too high' thresholds all off of the original df! Don't do it sequentially or else you'll change it! The 'too high' of the original df is different that the 'too high' of a df with the 'too low' already removed!
# print(df.height.quantile(q=0.025))
# print(df['height'].quantile(q=0.025))
height_low_th = df.height.quantile(q=0.025)
height_high_th = df.height.quantile(q=0.975)
weight_low_th = df.weight.quantile(q=0.025)
weight_high_th = df.weight.quantile(q=0.975)

#print(df_height_too_low) #only print after removing .index from this df's assignment
# print(df.shape)
# print(df[ df.height < height_low_th ].shape) #can't have .index in there when printing any of it
df_height_too_low = df[ df.height < height_low_th ].index
df.drop(df_height_too_low, inplace = True)

# print(df.shape)

#Filter out rows for which height is greater than the 97.5th percentile
#print(df.height.quantile(q=0.975))

# print(df[ df.height > height_high_th ].shape) #can't have .index in there when printing any of it
# print(df.shape)
df_height_too_high = df[ df.height > height_high_th ].index
df.drop(df_height_too_high, inplace = True)

# print(df.shape)

#Filter out rows for which weight is less than the 2.5th percentile
# print(df.weight.quantile(q=0.025))

# print(df.shape)
# print(df[ df.weight < weight_low_th ].shape) #can't have .index in there when printing any of it
##Getting an error when just running the following: df.drop(df_weight_too_low, inplace = True). I think I'm now trying to remove a row again that was already removed with one of the height threshold drops. Therefore, I'll set the thresholds before any dropping of rows, but I'll set the sections of the df to be dropped right before individually dropping them! That should settle it.
df_weight_too_low = df[ df.weight < weight_low_th ].index
df.drop(df_weight_too_low, inplace = True)
# print(df.shape)

#Filter out rows for which weight is greater than the 97.5th percentile
#print(df.weight.quantile(q=0.975))

# print(df[ df.weight > weight_high_th ].shape) #can't have .index in there when printing any of it
# print(df.shape)
df_weight_too_high = df[ df.weight > weight_high_th ].index
df.drop(df_weight_too_high, inplace = True)
# print(df.shape)

# Convert the data into long format and create a chart that shows the value counts of the categorical features using seaborn's catplot(). The dataset should be split by 'Cardio' so there is one chart for each cardio value. The chart should look like examples/Figure_1.png.

#sns.set_theme(style="ticks") #sets the shape to be rectangular instead of something else like scatterplots
df_categorical = df.loc[:, 'cholesterol':] #create new dataframe with only categorical parameters. This syntax is row slicing first then column slicing.
#Going to order columns alphabetically, besides cardio column which will be removed later anyway
# print(df_categorical.iloc[:,0]) #to print first column
first_column = df_categorical.pop('active')
df_categorical.insert(0, 'active', first_column)
second_column = df_categorical.pop('alco')
df_categorical.insert(1, 'alco', second_column)
fifth_column = df_categorical.pop('overweight')
df_categorical.insert(4, 'overweight', fifth_column)
#print(df_categorical.head())
df_categorical.drop(['cardio'], axis=1, inplace = True) #remove cardio column
df_categorical['index_'] = df.index #put in a column to categorical df that is same number as index number from original df
#print(df_categorical.head(20))
df_categorical_long_form = pd.melt(df_categorical, id_vars = ['index_'], var_name='variable', value_name='values')
# print(df_categorical_long_form.head(20))
df_categorical_long_form['cardio'] = 0 #put in a cardio column full of zeros for now
# print(df_categorical_long_form.tail())
# print(df_categorical_long_form.head())
 #get the total number of remaining rows from original df
## Now get cholesterol values from original df to correct corresponding rows in long form df
card = df.cardio

#print(chol)
#chol = chol.append(chol)
## append method in pandas is deprecated; need to use concat instead!!
card = pd.concat([card, card, card, card, card, card])
# print(card)
# print(df_categorical_long_form)
##need index to match for each series/df in order to merge.
##set index to default for both:
df_categorical_long_form.reset_index(inplace = True, drop= True)
# print(df_categorical_long_form)
# print(card.tail())
#rest series index: inplace= True to make it permanant, drop = True to keep it a series by dropping the old index (would become data frame otherwise)
card.reset_index(inplace = True, drop= True)
df_categorical_long_form.cardio = card
# print(card)
# card.columns = ['cardio']
# print(card)
# quit()
# print(df_categorical_long_form)
# print(df_categorical_long_form.loc[(df_categorical_long_form.values == '0') ])
# print(df_categorical_long_form.loc[(df_categorical_long_form.values == '1') ])
# #print(1 == 1)
# print(df_categorical_long_form.iloc[2]['values'] == df_categorical_long_form.iloc[378748]['values'])
# print(len(str(df_categorical_long_form.iloc[378749]['values'])))



##Get the data frame to an excel document to inspect it since the graph is coming out funny. This will help me know if it is either the data that is wrong or if I'm just graphing it wrong
#df_categorical_long_form.to_excel(r'C:\Users\jflieder\Desktop\long_form.xlsx', index = False, header=True)


# sns.set_theme(style="ticks")
# fig1 = sns.catplot(x="variable", hue = "values", hue_order = [0, 1], data=df_categorical_long_form, col = "cardio", kind="count", palette=sns.color_palette(['blue', 'orange']) )
# fig1.set(ylabel ="total")
# fig1.savefig('fig1_catplot.png')

# ##Now use the original data frame, with the filters/additions required, to make a heat map for figure2:
# fig2 = sns.heatmap(data = df)
# # #Add in a .figure. for this saving of the picture to avoid a AttributeError: 'AxesSubplot' object has no attribute 'savefig'. This is to avoid jamming multiple figures into the fig spot in python:
# fig2.savefig('fig2_heatmap.png')

##Kept getting either the figure1 stuff inserted into figure2 in a messy way or kept getting a 'fig, ax = plt.subplots()' error. Now going to try the fig, ax = plt.subplots() business to get the two separate figures without errors or the figures getting mixed:

fig, ax1 = plt.subplots()
sns.set_theme(style="ticks")
ax1 = sns.catplot(x="variable", hue = "values", hue_order = [0, 1], data=df_categorical_long_form, col = "cardio", kind="count", palette=sns.color_palette(['blue', 'orange']) )
ax1.set(ylabel ="total")
ax1.figure.savefig('fig1_catplot.png')

fig, ax2 = plt.subplots()
#Need to get a version of the data frame df that has the columns along both the x axis and teh y axis so a correlation matrix can be made:
df_corr = df.corr()
#Now make a mask using numpy syntax I found online. This mask will keep only the lower half triangle of the correlation matrix when entered into the argument of the heatmap function:
mask_lower=np.triu(np.ones(df_corr.shape)).astype(bool) #note that np.bool is deprecated, so I changed it to simply bool
ax2 = sns.heatmap(data = df.corr(), mask = mask_lower, cmap = "rocket") #cmap is the color palette argument, rocket is default
#Need to add in a .figure. to avoid the following error: AttributeError: 'AxesSubplot' object has no attribute 'savefig'
ax2.figure.savefig('fig2_heatmap.png')