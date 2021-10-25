import pandas
import pandas as pd


def transform_unnamed_cols_base(df: pd.DataFrame, base_column_name: str, following_columns_range_size: int,
                                new_column_name_prefix: str = None, inplace=False) -> object:
    """
    This function transforms a range of columns based on the fact that
    the following schema will be found in dataframe:

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
    :param following_columns_range_size: how many columns, starting from column following the base_column_name,
    has to be transformed
    :param new_column_name_prefix:  new name to be added as base_name to rename map
    :param inplace: If False, return a copy. Otherwise, do operation inplace and return None.
    :return: input dataframe with Unnamed columns dropped and string values transformed to binary values (0,1)
    """

    # extracting  columns of interest
    df_target_columns = df.iloc[:, df.columns.get_loc(base_column_name): (df.columns.get_loc(base_column_name) +
                                                                          following_columns_range_size)]

    return _even_out_categorical_as_binaries(df, df_target_columns,
                                             new_column_name_prefix=new_column_name_prefix, inplace=inplace)


def transform_unnamed_cols_range(df: pd.DataFrame, columns_range: range,
                                 new_column_name_prefix: str, inplace=False) -> object:
    """
    This function transforms a range of columns based on the fact that
    the following schema will be found in dataframe:

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
    columns_rename_map = {}
    for col_name in target_columns:
        # selecting working column
        column_suffix_name_index = df[target_columns].loc[:, col_name].first_valid_index()

        # retrieving string to be used both as column suffix and as categorical name
        column_suffix_name = df[target_columns].loc[column_suffix_name_index, col_name]

        # populating map with correct new column name
        columns_rename_map[col_name] = " ".join((column_prefix_name, column_suffix_name))

        if binary_output:
            # transforming column to binary values
            df[col_name] = df[col_name].apply(lambda x: 1 if x == column_suffix_name else 0)
    # renaming columns using the produced map
    df.rename(columns=columns_rename_map, inplace=True)

# TODO: check it and think about deleting it
# def clean_data(df, target_feature):
#     """
#     This function cleans df using the following steps to produce X and y:
#     1. Drop all the rows with no preferred language
#     2. Create X as all the columns that are not the Salary column
#     3. Create y as the Salary column
#     4. For each numeric variable, fill the column with the mean value.
#     6. Create dummy columns for all the categorical variables, drop the original columns
#     :param df dataframe to be cleaned
#     :returns X - A matrix holding all of the variables you want to consider when predicting the response
#              y - the corresponding response vector
#     """
#     # Drop rows with missing target_feature values
#     df = df.dropna(subset=[target_feature], axis=0)
#     y = df[target_feature]
#
#     # Drop respondent and expected salary columns
#     df = df.drop(target_feature, axis=1)
#
#     # Fill numeric columns with the mean
#     num_vars = df.select_dtypes(include=['float', 'int']).columns
#     for col in num_vars:
#         df[col].fillna((df[col].mean()), inplace=True)
#
#     # Dummy the categorical variables
#     cat_vars = df.select_dtypes(include=['object']).copy().columns
#     for var in cat_vars:
#         # for each cat add dummy var, drop original column
#         df = pd.concat([df.drop(var, axis=1), pd.get_dummies(df[var], prefix=var, prefix_sep='_', drop_first=True)],
#                        axis=1)
#
#     X = df
#     return X, y
