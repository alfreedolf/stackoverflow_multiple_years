"""
This file contains functions needed to load data from sources
"""
import os
import re
import pandas as pd


def load_from_csv(file_path: str, encoding: str):
    """
    Loads single year survey data from CSV file
    :param file_path: file path to get data from
    :param encoding: cvs source file encoding
    :return: a dataframe containing raw data from survey from a single year
    """

    # in case no path is provided, assuming default path
    return pd.read_csv(file_path, encoding=encoding)


def load_surveys_data_from_csv(years=None, data_path="data", encoding="ISO-8859-1"):
    """
    Loads multiple years survey data from CSV files
    :param years: a list of multiple years in integer format
    :param data_path: data folder where CSV files is expected to be located
    :param encoding: csv files encoding
    :return: a dictionary of dataframes containing raw data from surveys from multiple years
    """
    if years is None:
        years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # dictionary containing years data
    surveys_years_df = {}
    # retrieving base directory where data folder is expected to be located 
    base_dir = os.getcwd()
    # base_dir = os.path.split(os.getcwd())[0]
    for y in years:
        surveys_years_df[y] = load_from_csv(os.path.join(base_dir, data_path,
                                                         f"{y}_results.csv"),
                                                         encoding)
    return surveys_years_df


def get_dataset_max_shapes(df_dict):
    """
    This function will extract max shapes values from dataset
    :param df_dict: input dictionary
    :return: max number of columns and rows
    """
    max_rows = 0
    max_cols = 0
    for _, df in df_dict.items():
        # counting rows
        if max_rows < df.shape[0]:
            max_rows = df.shape[0]
        # counting columns
        if max_cols < df.shape[1]:
            max_cols = df.shape[1]
    return max_rows, max_cols


def get_intersection(features_list1: list, features_list2: list) -> list:
    """
    Get intersection between two list of features as strings list
    :param features_list1: first list of features
    :param features_list2: second list of features
    :return: a list of string, composed of all elements both in features_list1 and features_list2
    """
    features_intersection = [value for value in features_list1 if value in features_list2]
    return features_intersection


def get_common_feature_list(data_frames_dict: dict) -> list:
    """
    Computes least common features set from dataframes dictionary
    :param data_frames_dict: dataframe dictionary in the form of {year : dataframe}
    :return: least common features set in a dict of dataframes
    """

    # computing common features
    features = []
    for i, df in enumerate(data_frames_dict.values()):
        if i == 0:
            features = df.columns
        else:
            features = get_intersection(features, df.columns)
    return features


def merge_dataframes(data_frames_dict):
    """
    Merges dataframes based on least common feature set
    :param data_frames_dict: a dataframes dictionary data to be merged, based on least common features
    :return: a single, merged dataframe based on least common feature set
    """
    merged_df = None
    common_features_list = get_common_feature_list(data_frames_dict)
    for i, (year, df) in enumerate(data_frames_dict.items()):
        df['year'] = year
        if i == 0:
            merged_df = df
        else:
            merged_df = pd.concat([merged_df[common_features_list], df[common_features_list]])
    return merged_df


def get_10most_popular_languages_by_year(languages_popularity_df: pd.DataFrame,
                                         proficiencies_by_year_data: dict[str, list], top10languages: list):
    """Retrieve 10 most populare languages by year

    Args:
        languages_popularity_df (pd.DataFrame): input dataframe containing popularity data for languages
        proficiencies_by_year_data (dict[str, list]): key-value year-proficiency data list 
        top10languages (list): _description_
    """
    for year, dataset in proficiencies_by_year_data.items():
        # retrieving data of the first 10 popular languages
        for lang in top10languages:
            lang_re = r'\b' + re.escape(lang) + r'\Z'
            tmp_stats = dataset[0]["full ranking"].filter(regex=lang_re)
            if len(tmp_stats) > 0:
                languages_popularity_df.loc[year, lang] = int(tmp_stats.values[0])
            else:
                languages_popularity_df.loc[year, lang] = 0
            tmp_percentages = dataset[1]["proficiency percentages"].filter(regex=lang_re)
            if len(tmp_percentages) > 0:
                languages_popularity_df.loc[year, lang+" percentage"] = tmp_percentages.values[0]
            else:
                languages_popularity_df.loc[year, lang+" percentage"] = 0
            del tmp_stats, tmp_percentages
