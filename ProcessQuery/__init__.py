from ProcessQuery.Process import ProcessNaturalLanguageQuery
from Wrappers import hackathon_wrappers as wrapper
from LoadData import sheet_dict
from string import punctuation
from pprint import pprint
punctuation += " "
import re
regex = re.compile('[%s]' % re.escape(
    punctuation))

columns = sheet_dict['Orders'].columns
row_wise_column = {}

for column in sheet_dict['Orders'].select_dtypes(include=['object']).columns:
    for row in sheet_dict['Orders'][column].unique():
        row_wise_column[row] = regex.sub("_", column.lower())



#    sheet_dict['Orders'][column].unique()

#query = """average sales in the last quarter of CA-2016-138688"""
#query = """graph plot between sales and profit"""
#query = """find the product id with top sales"""
#query = """what is the product id with maximum sales"""
#query = """find the quantity sold of product id in anderson"""
#query = """show me the monthly sales of nevell322 for past one year"""
#query = """show me total sales for CA-2016-138688"""
#query = """predict sales"""

def get_action_col(query):
    Processor = ProcessNaturalLanguageQuery(query=query, columns=columns, row_wise_column=row_wise_column)
    sent = Processor._transform_sentence()
    print(sent)
    pprint(Processor._get_transformed_structure())
    Processor.extract_action1_columns()
    Processor.extract_action2_columns()
    Processor.extract_action3_columns()
    print(Processor.dic_action1_column)
    print(Processor.dic_action2_column)
    print(Processor.dic_action3_column)
    print(Processor.row)
    print(Processor.column)
    #print(Processor.dic_action2_column)
    #print(Processor.find_target_column())
    return Processor.dic_action1_column, Processor.dic_action2_column, Processor.dic_action3_column, Processor.find_target_column(), Processor.row, Processor.column

action1_col, action2_col, action3_col, target, row, column = get_action_col("""find maximum profit for south""")

print(wrapper.wrapper(action1_col, action2_col, action3_col, target, row, column))
