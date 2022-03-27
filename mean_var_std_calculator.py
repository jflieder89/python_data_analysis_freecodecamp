# This entrypoint file to be used in development. Start by reading README.md
# import mean_var_std
# from unittest import main

# print(mean_var_std.calculate([0,1,2,3,4,5,6,7,8]))

# # Run unit tests automatically
# main(module='test_module', exit=False)
##Tester input: [0,1,2,3,4,5,6,7,8]
import numpy as np
#print(np.__version__)
#lst = input('Input a list of 9 digits to analyze: ')
lst = '[0,1,2,3,4,5,6,7,8]'
# print(lst)
# print(type(lst))


##Clean up the list which is actually still a string:
lst = lst.replace("[", "")
lst = lst.replace("]", "")
lst = lst.replace("(", "")
lst = lst.replace(")", "")
lst = lst.replace("{", "")
lst = lst.replace("}", "")
lst = lst.replace("'", "")
lst = lst.replace('"', "")
#separate values by commas:
lst = lst.split(',')
# print(lst)
# print(type(lst))
# print(type(lst[0]))
##Now turn the separated digit strings into integers
for num in range(len(lst)):
  # print(num)
  # print(type(num))
  #print(type(num))
  num_int = int(lst[num])
  lst[num] = num_int
  #print(type(num))
# print(lst)
# print(type(lst[0]))
a = np.array([
  [lst[0], lst[1], lst[2]],
  [lst[3], lst[4], lst[5]],
  [lst[6], lst[7], lst[8]]
  ])
#print(a)

def calculate(lst):
  ##program in an error if number of digits entered is not 9:
  if len(lst)!= 9:
    raise ValueError('List must contain nine numbers.')
  #create final dictionary with empty values for now:
  calculation_dict = {'mean': 0, 'variance': 0, 'standard deviation': 0, 'max': 0, 'min': 0, 'sum': 0}
  # print(type(lst))
  # print(calculation_dict)
  a = np.array([
  [lst[0], lst[1], lst[2]],
  [lst[3], lst[4], lst[5]],
  [lst[6], lst[7], lst[8]]
  ])
  #print(a)

  #Now to get the values into the dictionary properly, with the values being lists instead of arrays
  #Use .tolist() method to have zeroes added to left side decimal points
  mean_axis1 = np.mean(a, axis=0).tolist()
  mean_axis2 = np.mean(a, axis=1).tolist()
  mean_axis_flattened = np.mean(a).tolist()
  calculation_dict['mean'] = [mean_axis1, mean_axis2, mean_axis_flattened]

  var_axis1 = np.var(a, axis=0).tolist()
  var_axis2 = np.var(a, axis=1).tolist()
  var_axis_flattened = np.var(a).tolist()
  calculation_dict['variance'] = [var_axis1, var_axis2, var_axis_flattened]

  std_axis1 = np.std(a, axis=0).tolist()
  std_axis2 = np.std(a, axis=1).tolist()
  std_axis_flattened = np.std(a).tolist()
  calculation_dict['standard deviation'] = [std_axis1, std_axis2, std_axis_flattened]

  max_axis1 = np.max(a, axis=0).tolist()
  max_axis2 = np.max(a, axis=1).tolist()
  max_axis_flattened = np.max(a).tolist()
  calculation_dict['max'] = [max_axis1, max_axis2, max_axis_flattened]

  min_axis1 = np.min(a, axis=0).tolist()
  min_axis2 = np.min(a, axis=1).tolist()
  min_axis_flattened = np.min(a).tolist()
  calculation_dict['min'] = [min_axis1, min_axis2, min_axis_flattened]

  sum_axis1 = np.sum(a, axis=0).tolist()
  sum_axis2 = np.sum(a, axis=1).tolist()
  sum_axis_flattened = np.sum(a).tolist()
  calculation_dict['sum'] = [sum_axis1, sum_axis2, sum_axis_flattened]





  print(calculation_dict)
calculate(lst)