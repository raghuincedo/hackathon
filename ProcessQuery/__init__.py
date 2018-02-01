from ProcessQuery.Process import ProcessNaturalLanguageQuery
from LoadData import sheet_dict
from string import punctuation
punctuation += " "
import re
regex = re.compile('[%s]' % re.escape(
    punctuation))

columns = sheet_dict['Orders'].columns
row_wise_column = {}

for column in sheet_dict['Orders'].select_dtypes(include=['object']).columns:
    for row in sheet_dict['Orders'][column].unique():
        row_wise_column[row.lower()] = regex.sub("_", column.lower())



print(row_wise_column)
#for column in columns:
#    sheet_dict['Orders'][column].unique()

#query = """average sales in the last quarter of CA-2016-138688"""
#query = """graph plot between sales and profit"""
#query = """find the product id with top sales"""
#query = """what is the product id with maximum sales"""
#query = """find the quantity sold of product id in anderson"""
#query = """show me the monthly sales of nevell322 for past one year"""
#query = """show me total sales for CA-2016-138688"""
#query = """predict sales"""
query = """find total sales of top quantity"""

Processor = ProcessNaturalLanguageQuery(query = query, columns = columns, row_wise_column = row_wise_column)
sent = Processor._transform_sentence()

from pprint import pprint

print(sent)
print(Processor.transformed_columns)
pprint(Processor._get_transformed_structure())
Processor.extract_action_columns()
print(Processor.dic)