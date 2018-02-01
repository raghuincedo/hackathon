from __paths__ import path_to_resources
import os
import pandas as pd

data = pd.ExcelFile(os.path.join(path_to_resources, "Sample - Superstore.xls"))
sheet_names = data.sheet_names

sheets = [(sheet_name, pd.read_excel(data, sheet_name)) for sheet_name in sheet_names]

sheet_dict = dict(sheets)

del sheet_names, sheets

actions = {"mean":["mean", "average"],

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