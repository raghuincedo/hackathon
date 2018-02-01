from ProcessQuery.Process import ProcessNaturalLanguageQuery
from LoadData import sheet_dict

columns = sheet_dict['Orders'].columns

#for column in columns:
#    sheet_dict['Orders'][column].unique()

#query = """average sales in the last quarter of order id"""
#query = """plot graph between sales and profit"""
#query = """find the product id with top sales"""
#query = """what is the product id with maximum sales"""
#query = """find the quantity sold of product id in anderson"""
query = """plot the sales of next quarter"""

Processor = ProcessNaturalLanguageQuery(query = query, columns = columns)
sent = Processor._transform_sentence()

from pprint import pprint

print(sent)
print(Processor.transformed_columns)
pprint(Processor._get_transformed_structure())