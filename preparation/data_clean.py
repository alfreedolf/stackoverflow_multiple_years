"""
Implement function for data cleaning purposes.

Author: Alfonso Ridolfo
Date: October 2021
"""


import pandas as pd


def clean_data(input_dataframe, target_feature: str):
    """Clean a dataframe with respect to a target feature.

    Use the following steps to produce X (features) and y (labels) as output:

    1. Drop all the rows with no preferred language
    2. Create X as all the columns that are not the Salary column
    3. Create y as the Salary column
    4. For each numeric variable, fill the column with the mean value
    6. Create dummy columns for all the categorical variables
    7. Drop original columns.

    Args:
        input_dataframe: (pandas.DataFrame) dataframe to be cleaned
        target_feature: (str) target feature to be cleaned

    Returns:
        input_features: (pandas.DataFrame) matrix of meaninful features
        target_label: (pandas.DataFrame) corresponding answer vector
    """
    # Drop rows with missing target_feature values
    input_dataframe = input_dataframe.dropna(subset=[target_feature], axis=0)
    target_label = input_dataframe[target_feature]

    # Drop respondent and expected salary columns
    # TODO fix
    # input_dataframe = input_dataframe.drop(['Respondent', , target_feature],
    # axis=1)

    # Fill numeric columns with the mean
    num_vars = input_dataframe.select_dtypes(include=['float', 'int']).columns
    for col in num_vars:
        input_dataframe[col].fillna(
            (input_dataframe[col].mean()), inplace=True)

    # Dummy the categorical variables
    cat_vars = input_dataframe.select_dtypes(include=['object']).copy().columns
    for var in cat_vars:
        # for each cat add dummy var, drop original column
        input_dataframe = pd.concat([input_dataframe.drop(var, axis=1), pd.get_dummies(
            input_dataframe[var], prefix=var, prefix_sep='_', drop_first=True)], axis=1)

    input_features = input_dataframe
    return input_features, target_label


def calculate_time_between_dates(date1, date2):
    """Calculate time elapsed between two input dates.

    Args:
        date1: first date
        date2: second date

    Returns:
        time_between_dates: time between two dates
    """
    time_between_dates = abs(date1 - date2)
    return time_between_dates.days
