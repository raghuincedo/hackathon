from ProcessQuery.Process import ProcessNaturalLanguageQuery
from LoadData import sheet_dict

columns = sheet_dict['Orders'].columns

query = """average sales in the last quarter of order id"""
Processor = ProcessNaturalLanguageQuery(query = query, columns = columns)
sent = Processor._transform_sentence()

from pprint import pprint

print(sent)
print(Processor.transformed_columns)
pprint(Processor._get_transformed_structure())