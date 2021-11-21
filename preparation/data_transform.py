import re
from typing import Dict, Optional

import pandas
import pandas as pd
from pandas import DataFrame


def transform_unnamed_cols_base(df: pd.DataFrame, base_column_name: str, columns_look_ahead: int,
                                new_column_name_prefix: str = None, inplace=False) -> object:
    """
    This function transforms a range of columns based assuming the presence of following schema in dataframe:

    |base_column_name|Unnamed_n|Unnamed_n+1|Unnamed_n+2|---
    |option_1        |NaN      |NaN        |NaN        |---
    |----------------|NaN      |option_3   |NaN        |---
    |----------------|option_2 |NaN        |NaN        |---
    |----------------|NaN      |NaN        |option_4   |---
    Without a precise order, only one cell will be checked as "option_x"

    and that the following schema will be given as output:
    |base_column_name_option_1|base_column_name_option_2 |base_column_name_option_3|base_column_name_option_3|---

    Also, it will replace cell values from this columns with binary data (1, 0) according to the presence or not
    of the corresponding categorical value.


    :param df: input dataframe to be processed
    :param base_column_name: base column name to be used as basis to build option columns
    :param columns_look_ahead: how many columns, starting from column following the base_column_name,
    has to be transformed
    :param new_column_name_prefix:  new name to be added as base_name to rename map
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: input dataframe with Unnamed columns dropped and string values transformed to binary values (0,1)
    """

    # extracting  columns of interest
    df_target_columns = df.iloc[:, df.columns.get_loc(base_column_name): (df.columns.get_loc(base_column_name) +
                                                                          columns_look_ahead)]

    return _even_out_categorical_as_binaries(df, df_target_columns,
                                             new_column_name_prefix=new_column_name_prefix, inplace=inplace)


def transform_unnamed_cols_range(df: pd.DataFrame, columns_range: range,
                                 new_column_name_prefix: str, inplace=False) -> object:
    """
    This function transforms a range of columns based assuming the presence of following schema in dataframe:

    |base_column_name|Unnamed_n|Unnamed_n+1|Unnamed_n+2|---
    |option_1        |NaN      |NaN        |NaN        |---
    |----------------|NaN      |option_3   |NaN        |---
    |----------------|option_2 |NaN        |NaN        |---
    |----------------|NaN      |NaN        |option_4   |---
    Without a precise order, only one cell will be checked as "option_x"

    and that the following schema will be given as output:
    |base_column_name_option_1|base_column_name_option_2 |base_column_name_option_3|base_column_name_option_4|---

    Also, it will replace cell values from this columns with binary data (1, 0) according to the presence or not
    of the corresponding categorical value.



    :param df: input dataframe to be processed
    :param columns_range: range of columns from input dataframe to be transformed
    :param new_column_name_prefix: new name to be added as base_name to rename map
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: input dataframe with Unnamed columns dropped and string values transformed to binary values (0,1)
    """

    # extracting  columns of interest
    df_target_columns = df.iloc[:, columns_range]

    return _even_out_categorical_as_binaries(df, df_target_columns.columns,
                                             new_column_name_prefix=new_column_name_prefix, inplace=inplace)


def _even_out_categorical_as_binaries(df: pandas.DataFrame, df_target_columns: pandas.DataFrame,
                                      new_column_name_prefix: str, inplace: bool) -> object:
    """
    This function will even out a range of columns containing string values into a range of binary values in [0,1]
    :param df: input dataframe
    :param df_target_columns: target columns as dataframe
    :param new_column_name_prefix: string to be used as prefix
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: input dataframe with Unnamed columns dropped and string values transformed to binary values (0,1)
    """
    if not inplace:
        df_out = df.copy(deep=True)
        _categorical_columns_range_rename(df_out, df_target_columns.columns, new_column_name_prefix)
        return df_out
    else:
        _categorical_columns_range_rename(df, df_target_columns.columns, new_column_name_prefix)
        return None


def _categorical_columns_range_rename(df: pandas.DataFrame, target_columns: pandas.Index,
                                      column_prefix_name: str, binary_output: bool = True) -> None:
    """
    This function renames dataframe columns, from categorical data which are in the form
    :param df: input dataframe
    :param target_columns: columns to be processed
    :param column_prefix_name: prefix to be used for new headings name
    :param binary_output: if true, output values of the target columns cells will be transformed to values in (0, 1)
    """
    # iterating through columns of interest, in order to create a column rename map
    columns_rename_map: Dict[str, str] = {}
    for col_name in target_columns:
        # selecting working column
        column_suffix_name_index = df[target_columns].loc[:, col_name].first_valid_index()

        # retrieving string to be used both as column suffix and as categorical name
        column_suffix_name = df[target_columns].loc[column_suffix_name_index, col_name]

        # populating map with correct new column name
        columns_rename_map[col_name] = " ".join((column_prefix_name, column_suffix_name))
        if binary_output:
            binarize_column(df, col_name, column_suffix_name)
    # renaming columns using the produced map
    df.rename(columns=columns_rename_map, inplace=True)


def binarize_column(df: pandas.DataFrame, col_name: str, true_val: str, inplace: bool = True) -> Optional[DataFrame]:
    """
    Transforms a single column to binary values, converting specific values to '1' and all the other values to '0'
    :param df: input dataframe
    :param col_name: target column
    :param true_val: values to be converted to '1'
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return optionally returns input df modified, if inplace is False
    """
    if not inplace:
        df_out = df.copy(deep=True)
        df_out[col_name] = df_out[col_name].apply(lambda x: 1 if x == true_val else 0)
        return df_out
    else:
        df[col_name] = df[col_name].apply(lambda x: 1 if x == true_val else 0)
        return None


def binarize_columns_range(df: pandas.DataFrame, col_range: range, true_values: list,
                           inplace: bool = True) -> Optional[DataFrame]:
    """
    Transforms a set of columns (a dataframe) to binary values
    :param df: input dataframe
    :param col_range: range of columns from the dataframe to be binarized
    :param true_values: the function will look in the range of columns
    for each of the each of the values in this list respectively,
    writing a '1' in each cell that contains the value and a '0' in each cell that doesn't.
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: input dataframe updated according to binarization
    """
    if not inplace:
        df_out = df.copy(deep=True)
        for col, tv in zip(df_out.iloc[:, col_range].columns, true_values):
            binarize_column(df_out, col, tv, inplace=True)
        return df_out
    else:
        for col, tv in zip(df.iloc[:, col_range].columns, true_values):
            binarize_column(df, col, tv, inplace=inplace)
        return None


def first_valid_value_index(column_name: str, column_data: pd.Series):
    curr_valid_index = -1
    for i, val in column_data.iteritems():
        if isinstance(val, str):
            if val in column_name and curr_valid_index < 0:
                curr_valid_index = i + 1
    return curr_valid_index


def feature_split(df: pd.DataFrame,
                  column_to_split: str, sep: str = ";", inplace: bool = True) -> Optional[pd.DataFrame]:
    """
    This function splits data from a single column into a set of columns
    :rtype: object
    :param df: input dataframe
    :param column_to_split: name of the column to be split
    :param sep: separator to be used in feature splitting
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: optionally returns a new dataframe
    """

    # retrieving feature values from desired column
    joint_features_series: pd.Series = df.loc[:, column_to_split]
    # initializing empty set
    features = set()

    if not inplace:
        # copying input dataframe
        df_out = df.copy(deep=True)
    else:
        df_out = df

    # iterating over features rows to populate features set
    for index, joint_features in joint_features_series.iteritems():
        if isinstance(joint_features, str):
            # joint_features_list =
            for feat in [feat.strip() for feat in joint_features.split(sep=sep)]:
                column_name = column_to_split + ": " + feat
                df_out.loc[index, column_name] = 1

    df_out.drop(labels=column_to_split, axis=1, inplace=True)
    df_out.fillna(value=0, inplace=True)
    if not inplace:
        return df_out
    else:
        return None


def string_found(string1, string2):
    """
    This function looks for a string
    :param string1:
    :param string2:
    :return:
    """
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False
