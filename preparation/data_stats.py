from collections import defaultdict

import pandas as pd


def map_any_case_to_lower(any_case_input: list) -> dict:
    """
    This function maps a list of strings values, given as input in any case combination,
    to a lower case corresponding key. The result is a hash map in which each element has as key a lowercase string and
    as values a list of corresponding strings in any case combination.
    :param any_case_input: a list of any case combination list
    :return: a dictionary containing a list of strings corresponding to the key
    :rtype: dict
    """
    output_map = defaultdict(list)
    for s in any_case_input:
        output_map[s.lower()].append(s)
    return output_map


def drop_columns_from_map(df, dropping_map, column_to_drop: str) -> pd.DataFrame:
    """
    This function drops a set of columns given a dictionary of columns
    :param df:
    :param dropping_map:
    :param column_to_drop:
    :return: the input dataframe, without any occurrence of string_to_drop, in any case combination
    """
    for tbe in dropping_map[column_to_drop]:
        df = df.drop(tbe, axis=1)
    return df


class LanguagesStatsExtractor:

    def __init__(self, source_data: pd.DataFrame):
        self.__source_data = source_data

    def compute_top_ten_languages(self, languages_proficiency_column_range, exclusion_list=[],
                                  ignore_case=True) -> pd.Series:
        """
        Computes top ten languages by proficiency.
        :param languages_proficiency_column_range: a range variable, used to slice language proficiency from source data
        :param exclusion_list: languages to be excluded from final results
        :param ignore_case: if True, the method will look for elements in exclusion_list to be in source dataframe,
        ignoring occurrences casing (upper or lower case)
        :return: a Pandas series of at most 10 elements, containing top languages by proficiency, ordered from the most
        to the least popular.
        """

        # retrieving languages proficiencies ranking in descending order
        s_2011_proficiencies_clean_sum = self.compute_language_proficiency_ranking(languages_proficiency_column_range,
                                                                                   exclusion_list, ignore_case)

        # storing top ten elements by popularity in a dedicated pandas series
        s_2011_proficiencies_top_10 = s_2011_proficiencies_clean_sum.head(10)

        return s_2011_proficiencies_top_10

    def compute_language_proficiency_ranking(self, languages_proficiency_column_range, exclusion_list=[],
                                             ignore_case=True, ascending=False) -> pd.Series:
        """
        Computes language proficiency ranking on source data, given a selected column range containing
        language proficiencies data.
        :param languages_proficiency_column_range: a range variable, used to slice language proficiency from source data
        :param exclusion_list: languages to be excluded from final results
        :param ignore_case: if True, the method will look for elements in exclusion_list to be in source dataframe,
        ignoring occurrences casing (upper or lower case)
        :param ascending: if True, the returning value will be ordered in ascending order
        :return: a Pandas Series containing language proficiency ranking, obtained through summation of values
        from selected range, excepting values from exclusion list.
        """
        # slicing features columns containing language proficiencies data
        df_proficiencies: pd.DataFrame = self.__source_data.iloc[:, languages_proficiency_column_range]

        # populating lower case version of column list, if requested
        # proficiencies_column_names_lower_case = [column.lower() for column in df.columns]
        proficiencies_lower_to_original_map = map_any_case_to_lower(list(df_proficiencies.columns))

        # excluding selected columns, representing proficiency
        # (when not relevant, e.g. not a programming language) from final computation
        for to_be_excluded in exclusion_list:
            if ignore_case and (to_be_excluded.lower() in proficiencies_lower_to_original_map.keys()):
                df_proficiencies = drop_columns_from_map(df_proficiencies, proficiencies_lower_to_original_map,
                                                         to_be_excluded.lower())
            elif not ignore_case and (to_be_excluded in df_proficiencies.columns):
                df_proficiencies = df_proficiencies.drop(to_be_excluded, axis=1)
            else:
                print("error finding feature in axis")

        # computing total proficiencies
        s_2011_proficiencies_clean_sum: pd.Series = df_proficiencies.sum(axis=0)

        # sorting values by popularity
        s_2011_proficiencies_clean_sum.sort_values(ascending=ascending, inplace=True)

        return s_2011_proficiencies_clean_sum
