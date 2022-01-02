import pandas as pd

"""
This script is useful to just look at the data from PyCharm SciView
"""
results_2011_df = pd.read_csv("2011_results.csv", encoding="ISO-8859-1")
results_2012_df = pd.read_csv("2012_results.csv", encoding="ISO-8859-1")
results_2013_df = pd.read_csv("2013_results.csv", encoding="ISO-8859-1")
results_2014_df = pd.read_csv("2014_results.csv", encoding="ISO-8859-1")
results_2015_df = pd.read_csv("2015_results.csv", encoding="ISO-8859-1")
new_2015_header = results_2015_df.iloc[0]
results_2015_df = results_2015_df[1:]
results_2015_df.columns = new_2015_header
results_2016_df = pd.read_csv("2016_results.csv", encoding="ISO-8859-1")
results_2017_df = pd.read_csv("2017_results.csv", encoding="ISO-8859-1")
results_2018_df = pd.read_csv("2018_results.csv", encoding="ISO-8859-1")
results_2019_df = pd.read_csv("2018_results.csv", encoding="ISO-8859-1")
results_2020_df = pd.read_csv("2020_results.csv", encoding="ISO-8859-1")
results_2021_df = pd.read_csv("2021_results.csv", encoding="ISO-8859-1")
