import pandas as pd
from __paths__ import path_to_resources
import os

class FilterDataLowLevel(object):
    """
    -> a class to filter pandas data at low level
    -> given column names, and respective values on which column values need to be filtered
       and corresponding operations
    -> will return filtered data
    """

    def __init__(self,
                 columns = [],
                 values = [],
                 operators = [],
                 targets = [],
                 path_to_excel = os.path.join(path_to_resources, "Sample - Superstore.xls")):
        """
        -> expects column names, values, and operation
        """
        self.columns = columns
        self.values = values
        self.operators = operators
        self.targets = targets
        data = pd.ExcelFile(path_to_excel)
        sheet_names = data.sheet_names

        sheets = [(sheet_name, pd.read_excel(data, sheet_name)) for sheet_name in sheet_names]

        self.sheet_dict = dict(sheets)

        del sheet_names, sheets

    def filter(self):
        """
        -> filter data
        :return: filtered data
        """
        df_1=self.sheet_dict["Orders"]
        #for i in range(len(self.columns)):

