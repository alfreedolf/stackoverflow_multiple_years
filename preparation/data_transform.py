import pandas as pd


def clean_data(df, target_feature):
    """
    This function cleans df using the following steps to produce X and y:
    1. Drop all the rows with no preferred language
    2. Create X as all the columns that are not the Salary column
    3. Create y as the Salary column
    4. For each numeric variable, fill the column with the mean value.
    6. Create dummy columns for all the categorical variables, drop the original columns
    :param df dataframe to be cleaned
    :returns X - A matrix holding all of the variables you want to consider when predicting the response
             y - the corresponding response vector
    """
    # Drop rows with missing target_feature values
    df = df.dropna(subset=[target_feature], axis=0)
    y = df[target_feature]

    # Drop respondent and expected salary columns
    df = df.drop(target_feature, axis=1)

    # Fill numeric columns with the mean
    num_vars = df.select_dtypes(include=['float', 'int']).columns
    for col in num_vars:
        df[col].fillna((df[col].mean()), inplace=True)

    # Dummy the categorical variables
    cat_vars = df.select_dtypes(include=['object']).copy().columns
    for var in cat_vars:
        # for each cat add dummy var, drop original column
        df = pd.concat([df.drop(var, axis=1), pd.get_dummies(df[var], prefix=var, prefix_sep='_', drop_first=True)],
                       axis=1)

    X = df
    return X, y


def binarize_values(column):
    pass


def prepare_unnamed(df: pd.DataFrame, base_column_name: str, following_column_range: int,
                    base_column_new_name: str = None) -> pd.DataFrame:
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



    :param df: input dataframe to be processed
    :param base_column_name: base column name to be used as basis to build option columns
    :param following_column_range: how many columns, starting from column following the base_column_name, has to be
    transformed
    :param base_column_new_name: new name to be added as base_name to rename map
    :return: input dataframe with Unnamed columns dropped and
    """

    # extracting  columns of interest
    df_payload_columns = df.iloc[:, df.columns.get_loc(base_column_name): (df.columns.get_loc(base_column_name) +
                                                                           following_column_range)]

    if base_column_new_name is None:
        column_prefix_name = "Proficient in"

    # iterating through columns of interest, in order to create a column rename map
    columns_rename_map = {}
    for col_name in df_payload_columns.columns:
        # selecting working column
        column_suffix_name_index = df_payload_columns.loc[:, col_name].first_valid_index()

        # retrieving string to be used both as column suffix and as categorical name
        column_suffix = df_payload_columns.loc[column_suffix_name_index, col_name]

        # populating map with correct new column name
        columns_rename_map[col_name] = column_prefix_name + " " + column_suffix

        # transforming column to binary values
        df[col_name] = df[col_name].apply(lambda x: 1 if x == column_suffix else 0)

    # renaming columns using the produced map
    df.rename(columns=columns_rename_map, inplace=True)
    return df
