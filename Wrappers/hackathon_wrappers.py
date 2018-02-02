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
from Wrappers.graphMaker import Graphs
plotGraph = Graphs()

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
                "forecast":["forecast", "project", "projection", "predict"],
                "maximum":["maximum", "max", "top", "highest", "best", "most", "high", "topmost", "big", "biggest"],
                "minimum":["minimum", "min", "bottom", "lowest", "poorest", "least", "low", "worst", "small", "smallest"],
                "quick": ["quick", "fast", "quickest", "fastest"],
                "slow": ["slow", "slowest"],
                "plot": ["plot", "graph", "draw", "trend"],
                "distribution": ["distribution", "pie chart", "pie-chart", "pie"],
                "histogram": ["histogram", "frequency distribution", "frequency"],
                "higher": ["higher", "greater", "above", "over", "more", "more than", "bigger"],
                "lower": ["lower", "smaller", "below", "under", "less", "less than", "lesser"],
                "correlation": ["correlation", "correlation coefficient"]
                }
def find_operation(action):
    for item in operations:
        if action in operations[item]:
            return item

def simpleAction(actionDict, filtered_data, target):
    action = ''
    column = ''
    for key in actionDict:
        if key == None:
            continue
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
        return pd.DataFrame({"Error":["please enter data related query"]})

    if action == "mean":
        return pd.DataFrame({"mean of "+column : [mean(filtered_data[column], filtered_data)]})
    elif action == "std_dev":
        return pd.DataFrame({"std_dev of "+column : [std_dev(filtered_data[column], filtered_data)]})
    elif action == "variance":
        return pd.DataFrame({"variance of "+column : [variance(filtered_data[column], filtered_data)]})
    elif action == "summation":
        return pd.DataFrame({"total of "+column : [sum(filtered_data[column])]})
    elif action == "count":
        return pd.DataFrame({"number of "+column : [len(filtered_data[column])]})
    elif action == "forecast":
        return forecast(column, filtered_data)
    elif action == "maximum":
        return pd.DataFrame({"maximum of "+column:filtered_data[filtered_data[column] == max(filtered_data[column])][(" ").join(target.split("_")).strip()]})#, filtered_data)
    elif action == "minimum":
        return pd.DataFrame({"maximum of "+column:filtered_data[filtered_data[column] == min(filtered_data[column])][(" ").join(target.split("_")).strip()]})#, filtered_data)
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
    filtered_data2 = filtered_data
    filtered_data2['month-year'] = filtered_data2['order date'].apply(lambda x: x.date().strftime('%y-%m'))
    filtered_data2.groupby(filtered_data2.sort_values(by='order date')['month-year'])[column].sum()
    column2=filtered_data2[column]
    for i in range(3):
        column2.loc[len(column2)]=mean(column2.loc[(len(column2)-3):(len(column2)-1)], filtered_data)
    return column2

def plot(column, type, filtered_data, col_name):
    dates = list(filtered_data.loc[:, "order date"])[-20:]
    values = list(filtered_data.loc[:, col_name])[-20:]
    if type == 'scatter plot':
        plotGraph.scatterPlot(dates,values)
    elif type == "histogram":
        plotGraph.histogram("Histogram","dates",col_name, dates, values)
    return (type, dates, values, ["dates", col_name])



def action2(actionDict, filtered_data):
    action = [x for x in actionDict][0]
    """
    act_dict = actionDict[]
    act_name = ''
    for key in act_dict:
        act_name = key
    """

    parameter = actionDict[action]['parameter']
    column = actionDict[action]["column"]
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

def action3(actionDict, filteredData):
    #action = [x for x in actionDict][0]
    """
    act_dict = actionDict[]
    act_name = ''
    for key in act_dict:
        act_name = key
    """
    column = ''
    action = ''

    for key in actionDict:
        column = actionDict[key]
        action = key

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
    if action == "forecast":
        return forecast(column, filteredData)



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

def wrapper(action_type1, action_type2, action_type3, target, row, column):
    filtered_data = data
    if row is not None:
        if column is not None:
            filtered_data = data[data[column] == row]

    #filtered_data = data
    #print(filtered_data.head())
    if (len(action_type3)==0):
        for i in action_type2:
            filtered_data = action2(i, filtered_data)
        df = simpleAction(action_type1, filtered_data, target)
        plotGraph.showData(df)
    else:
        x = list(action3(action_type3, filtered_data))[-20:]

        obj = Graphs()
        obj.scatterPlot(list(range(len(x))),list(x))



