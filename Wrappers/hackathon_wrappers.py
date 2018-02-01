# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 18:41:33 2018

@author: vibhanshu.singh
"""
import numpy as np
import os, sys
import math
import pandas as pd
from LoadData import sheet_dict as data
from fuzzywuzzy import fuzz



data = data['Orders']
data.columns = map(str.lower, data.columns)
#data2 = data
operations = {"find": ["what", "which", "find", "who", "where", "when"],
              "equal": ["equal", "same", "same as", "equals", "equivalent"],
              "mean":["mean", "average"], 
              "std_dev":["standard deviation"], 
                "variance":["variance"], 
                "summation":["sum", "total", "all"], 
                "count":["number", "count"], 
                "regression":["regression", "project", "projection", "predict", "regress"],
                "maximum":["maximum", "max", "top", "highest", "best", "most", "high", "topmost", "big", "biggest"],
                "minimum":["minimum", "min", "bottom", "lowest", "poorest", "least", "low", "worst", "small", "smallest"],
                "quick": ["quick", "fast", "quickest", "fastest"],
                "slow": ["slow", "slowest"],
                "plot": ["plot", "graph", "draw", "trend"],
                "distribution": ["distribution", "pie chart", "pie-chart", "pie"],
                "histogram": ["histogram", "frequency distribution", "frequency"],
                "higher": ["higher", "greater", "above", "over", "more", "more than", "bigger"],
                "lower": ["lower", "smaller", "below", "under", "less", "less than"],
                "correlation": ["correlation", "correlation coefficient"]
                }
def find_operation(action):
    for item in operations:
        if action in operations[item]:
            return item

def simpleAction(actionDict, filtered_data):
    action = ''
    column = ''
    for key in actionDict:
        action = key
        column = actionDict[key]
    max_value = 0
    max_column_value = ''
    action = find_operation(action)
    for col in data.columns:
        score = fuzz.partial_ratio(col, column.lower())
        if score >max_value:
            max_value = score
            max_column_value = col
    if max_value > 80:
       column = max_column_value
    else:
        return "please enter data related query"

    if action == "mean":
        return mean(filtered_data[column], filtered_data)
    elif action == "std_dev":
        return std_dev(filtered_data[column], filtered_data)
    elif action == "variance":
        return variance(filtered_data[column], filtered_data)
    elif action == "summation":
        return sum(filtered_data[column], filtered_data)
    elif action == "count":
        return len(filtered_data[column], filtered_data)
    elif action == "forecast":
        return forecast(filtered_data[column], filtered_data)
    elif action == "maximum":
        return max(filtered_data[column], filtered_data)
    elif action == "minimum":
        return min(filtered_data[column], filtered_data)
    elif action == "plot":
        return plot("scatter plot", filtered_data[column], filtered_data, column)
    elif action == "distribution":
        return plot("pie chart", filtered_data[column], filtered_data, column)
    elif action == "histogram":
        return plot("histogram", filtered_data[column], filtered_data, column)
    elif action == "correlation":
        df = filtered_data[column]
        corr = np.corrcoef(df[column[0]], df[column[1]])
        corr = corr[0][1]
        return corr




def mean(column, filtered_data):
    return (float(sum(column))/max(len(column), 1))

def std_dev(column, filtered_data):
    num_items=len(column)
    mean_items = mean(column)
    differences = [x - mean_items for x in column]
    sq_differences = [d**2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd/num_items
    sd = math.sqrt(variance)
    return sd
    
def variance(column, filtered_data):
    num_items=len(column)
    mean_items = mean(column)
    differences = [x - mean_items for x in column]
    sq_differences = [d**2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd/num_items
    return variance
    
def forecast(column, filtered_data):
    column2=column
    for i in range(3):
        column2.loc[len(column2)]=mean(column2.loc[(len(column2)-3):(len(column2)-1),], filtered_data)
    return column2

def plot(column, type, filtered_data, col_name):
    dates = list(filtered_data.loc[:, "order date"])
    values = list(filtered_data.loc[:, col_name])
    return (type, dates, values, ["dates", col_name])



def action2_type1(actionDict, filtered_data):
    action = [x for x in actionDict][0]
    act_dict = actionDict[action]
    parameter = act_dict["parameter"]
    column = act_dict["column"]
    max_value = 0
    max_column_value = ''
    action = find_operation(action)
    for col in data.columns:
        score = fuzz.partial_ratio(col, column.lower())
        if score > max_value:
            max_value = score
            max_column_value = col
    if max_value > 80:
        column = max_column_value
    else:
        return "please enter data related query"
    if action == "higher":
        return higher(column, parameter, filtered_data)
    elif action == "lower":
        return  lower(column, parameter, filtered_data)
    elif action == "equal":
        return equal(column, parameter, filtered_data)



def higher(column, value, filtered_data):
    temp = pd.DataFrame(columns=list(filtered_data.columns.values))
    for i in range(1, len(filtered_data)):
        if (filtered_data[column][i]>value):
            temp = temp.append(filtered_data.loc[i,])
    return temp

def lower(column, value, filtered_data):
    temp = pd.DataFrame(columns=list(filtered_data.columns.values))
    for i in range(1, len(filtered_data)):
        if (filtered_data[column][i]<value):
            temp = temp.append(filtered_data.loc[i,])
    return temp

def equal(column, value, filtered_data):
    temp = pd.DataFrame(columns=list(filtered_data.columns.values))
    for i in range(1, len(filtered_data)):
        if (filtered_data[column][i]==value):
            temp = temp.append(filtered_data.loc[i,])
    return temp




            
    