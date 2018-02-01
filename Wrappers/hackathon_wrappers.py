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
operations = {"find": ["what", "which", "find", "who", "where", "when"],
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

def simpleAction(actionDict):
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
       pass
    else:
        return "please enter data related query"

    if action == "mean":
        return mean(data[column])
    elif action == "std_dev":
        return std_dev(data[column])
    elif action == "variance":
        return variance(data[column])
    elif action == "summation":
        return sum(data[column])
    elif action == "count":
        return len(data[column])
    elif action == "regression":
        return regression(data[column])
    elif action == "maximum":
        return max(data[column])
    elif action == "minimum":
        return min(data[column])


def mean(column):
    return (float(sum(column))/max(len(column), 1))

def std_dev(column):
    num_items=len(column)
    mean_items = mean(column)
    differences = [x - mean_items for x in column]
    sq_differences = [d**2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd/num_items
    sd = math.sqrt(variance)
    return sd
    
def variance(column):
    num_items=len(column)
    mean_items = mean(column)
    differences = [x - mean_items for x in column]
    sq_differences = [d**2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd/num_items
    return variance
    
def regression(column):
    pass


            
    