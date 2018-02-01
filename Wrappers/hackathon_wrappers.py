# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 18:41:33 2018

@author: vibhanshu.singh
"""
import numpy as np
import pandas as pd
#import pyflux as pf
from datetime import datetime
import matplotlib.pyplot as plt
import os, sys
import math

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

path_to_data = os.path.join(PROJECT_ROOT, "Sample - Superstore.xls")

data=pd.ExcelFile(path_to_data)
sheet_names = data.sheet_names

sheets = [(sheet_name, pd.read_excel(data, sheet_name)) for sheet_name in sheet_names]

sheets=dict(sheets)


col_conditions=[["Order ID", "=", "CA-2016-152156"], ["Sales", ">", 20]]

filtered_sheet=sheets["Orders"]

for i in col_conditions:
    if (i[1]=="="):
        filtered_sheet=filtered_sheet.loc[filtered_sheet[i[0]]==i[2]]
    else if (i[1]==">"):
        filtered_sheet=filtered_sheet.loc[filtered_sheet[i[0]]>i[2]]
    else
    

a=sheets["Orders"].loc[sheets["Orders"]['Order ID']=="CA-2016-152156"][["Sales", "Profit"]]

#def process(x, columns):
#    for column in columns:
#        if x[columns] > 5:
#            return x
#        else:
#            return None
#columns = ['Sales']
#B = sheets["Orders"].apply(lambda x : process(x, columns), axis = 0)
#
import spacy

nlp = spacy.load('en')
doc = nlp(u"""find average of sales column""")

tree = doc.print_tree()[0]
root = tree['word']


print("root", root)

"""
for ele in tree['modifiers']:
    print(ele["word"],ele["POS_fine"], ele["arc"])
    for internal in ele['modifiers']:
        print(internal)
"""

from pprint import pprint
pprint(tree)

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
                
def find_operation(word, column):
    for i in operations:
        if word in operations[i]:
            run_operation(i, column)

def run_operation(word, column):
    if word == "mean":
        return mean(column)
    else if word == "std_dev":
        return std_dev(column)
    else if word == "variance":
        return variance(column)
    else if word == "summation":
        return sum(column)
    else if word == "count":
        return len(column)
    else if word == "regression":
        return regression(column)
    else if word == "maximum":
        return max(column)
    else if word == "minimum":
        return min(column):
    else if word == "quick":
        return quick(column)
    else if word == "slow":
        return slow(column)
    else if word == plot:
        return plot(column)
    else if word == "distribution":
        return distribution(column)
    else if word == "histogram":
        return histogram(column)
    else if word == "higher":
        return higher(column)
    else if word == "lower":
        return lower(column)
    else if word == "correlation":
        return correlation(column)

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
    
            
    