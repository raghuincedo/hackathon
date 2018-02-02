from __paths__ import path_to_resources
import os
import pandas as pd

data = pd.ExcelFile(os.path.join(path_to_resources, "data.xls"))
sheet_names = data.sheet_names

sheets = [(sheet_name, pd.read_excel(data, sheet_name)) for sheet_name in sheet_names]

sheet_dict = dict(sheets)

#print(sheet_dict['Orders'].head())

del sheet_names, sheets

c = {"find": [
    "what",
    "which",
    "find",
    "who",
    "where",
    "when",
    "show"
  ]}

actions = {

  "date_wise": [
    "next month",
    "previous month",
    "the next month",
    "the last month",
    "last month",
    "month",
    "year",
    "week",
    "the previous month",
    "monthly",
    "yearly",
    "next year",
    "the next year",
    "previous year",
    "the previous year",
    "daily",
    "next day",
    "previous day",
    "weekly",
    "next week",
    "previous week",
    "quarterly",
    "next quarter",
    "previous quarter",
    "the next quarter",
    "the previous quarter"
  ],
  "mean": [
    "mean",
    "average"
  ],
  "std_dev": [
    "standard deviation"
  ],
  "variance": [
    "variance"
  ],
  "summation": [
    "sum",
    "total",
    "all"
  ],
  "count": [
    "number",
    "count"
  ],
  "maximum": [
    "maximum",
    "max",
    "top",
    "highest",
    "best",
    "most",
    "high",
    "topmost",
    "big",
    "biggest"
  ],
  "minimum": [
    "minimum",
    "min",
    "bottom",
    "lowest",
    "poorest",
    "least",
    "low",
    "worst",
    "small",
    "smallest"
  ],
  "quick": [
    "quick",
    "fast",
    "quickest",
    "fastest"
  ],
  "slow": [
    "slow",
    "slowest"
  ],
  "plot": [
    "plot",
    "graph",
    "draw",
    "trend"
  ],
  "distribution": [
    "distribution",
    "pie chart",
    "pie-chart",
    "pie"
  ],
  "histogram": [
    "histogram",
    "frequency distribution",
    "frequency"
  ],
  "correlation": [
    "correlation",
    "correlation coefficient"
  ]
}

actions2 = {
  "higher": [
    "higher",
    "greater",
    "above",
    "over",
    "more",
    "more than",
    "bigger"
  ],
  "lower": [
    "lower",
    "smaller",
    "below",
    "under",
    "lesser",
    "less than",
    "equal"
  ],
  "equal": [
    "equal",
    "same",
    "same as",
    "equals",
    "equivalent"
  ]
}

actions3 = {
    "forecast": [
        "forecast",
        "project",
        "projection",
        "predict"
    ]
}