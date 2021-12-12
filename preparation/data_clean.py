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
    :param target_feature: target feature to be cleaned
    :returns X - A matrix holding all the variables you want to consider when predicting the response
             y - the corresponding response vector
    """
    # Drop rows with missing target_feature values
    df = df.dropna(subset=[target_feature], axis=0)
    y = df[target_feature]

    # Drop respondent and expected salary columns
    # TODO fix
    # df = df.drop(['Respondent', , target_feature], axis=1)

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
