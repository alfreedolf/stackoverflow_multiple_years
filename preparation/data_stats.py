from abc import ABC, abstractmethod
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


class LanguagesStatsExtractor(ABC):
    """
    This is just an abstract base class that allows to define specific kind of stats extraction from a Dataframe
    """

    @abstractmethod
    def __init__(self, source_data: pd.DataFrame):
        self.__source_data = source_data

    @abstractmethod
    def get_data_source(self) -> dict:
        return self.__source_data

    @abstractmethod
    def get_stats(self) -> dict:
        pass


class LanguagesRankingExtractor(LanguagesStatsExtractor):

    def __init__(self, source_data: pd.DataFrame, columns_selection_criteria=None,
                 exclusion_list=[], entries_merge_list=[], prefix_to_remove=''):
        """

        :param source_data:
        :param columns_selection_criteria: a range variable or a string,
        used to slice language proficiency from source data.
        :param exclusion_list: languages to be excluded from final results
        :param prefix_to_remove: an optional string to be removed from returned series index
        :param entries_merge_list: this should be a list of couples. If provided, it will add values from tuple second
        element label to tuple first element label.
        """
        self.__source_data = source_data
        self.__columns_selection_criteria = columns_selection_criteria
        self.__prefix_to_remove = prefix_to_remove
        self.__exclusion_list = exclusion_list
        self.__entries_merge_list = entries_merge_list

    def compute_top_ten_languages(self, ignore_case=True) -> pd.Series:
        """
        Computes top ten languages by proficiency.
        :param ignore_case: if True, the method will look for elements in exclusion_list to be in source dataframe,
        ignoring occurrences casing (upper or lower case)
        :return: a Pandas' series of at most 10 elements, containing top languages by proficiency, ordered from the most
        to the least popular.
        """

        if self.__columns_selection_criteria is None:
            columns_selection_criteria = range(0, self.__source_data.shape[1])

        # retrieving languages proficiencies ranking in descending order
        s_proficiencies_clean_sum = self.compute_language_proficiency_ranking(ignore_case=ignore_case)

        # storing top ten elements by popularity in a dedicated pandas series
        s_proficiencies_top_10 = s_proficiencies_clean_sum.head(10)

        # rectifying index name as requested
        s_proficiencies_top_10.index = s_proficiencies_top_10.index.str.replace(self.__prefix_to_remove, '')

        return s_proficiencies_top_10

    def compute_language_proficiency_ranking(self, ignore_case=True, ascending=False) -> pd.Series:
        """
        Computes language proficiency ranking on source data, given a selected column range containing
        language proficiencies data.
        :param ignore_case: if True, the method will look for elements in exclusion_list to be in source dataframe,
        ignoring occurrences casing (upper or lower case).
        :param ascending: if True, the returning value will be ordered in ascending order.

        :return: a Pandas Series containing language proficiency ranking, obtained through summation of values.
        from selected range, excepting values from exclusion list.
        """
        # filtering dataframe in case of string value as input languages_proficiency_columns parameter
        if isinstance(self.__columns_selection_criteria, str):
            df_proficiencies: pd.DataFrame = self.__source_data.filter(like=self.__columns_selection_criteria)
        # slicing features columns containing language proficiencies data
        # in case of range value as input as languages_proficiency_columns parameter
        elif isinstance(self.__columns_selection_criteria, range):
            df_proficiencies: pd.DataFrame = self.__source_data.iloc[:, self.__columns_selection_criteria]
        else:
            df_proficiencies: pd.DataFrame = self.__source_data

        # populating lower case version of column list, if requested
        # proficiencies_column_names_lower_case = [column.lower() for column in df.columns]
        proficiencies_lower_to_original_map = map_any_case_to_lower(list(df_proficiencies.columns))

        # excluding selected columns, representing proficiency
        # (when not relevant, e.g. not a programming language) from final computation
        for to_be_excluded in self.__exclusion_list:
            if ignore_case and (to_be_excluded.lower() in proficiencies_lower_to_original_map.keys()):
                df_proficiencies = drop_columns_from_map(df_proficiencies, proficiencies_lower_to_original_map,
                                                         to_be_excluded.lower())
            elif not ignore_case and (to_be_excluded in df_proficiencies.columns):
                df_proficiencies = df_proficiencies.drop(to_be_excluded, axis=1)
            else:
                print("error finding feature in axis")

        # merging entries from entries_merge_list
        if entries_merge_list is not None:
            for t in entries_merge_list:
                df_proficiencies[t[0]] += df_proficiencies[t[1]]

        # computing total proficiencies
        s_proficiencies_clean_sum: pd.Series = df_proficiencies.sum(axis=0)

        # sorting values by popularity
        s_proficiencies_clean_sum.sort_values(ascending=ascending, inplace=True)

        return s_proficiencies_clean_sum

    def get_stats(self) -> dict:
        """
        This method returns a dictionary holding two values: full ranking and top ten languages from input dataframe
        :return: a dictionary holding two values: full ranking and top ten languages from input dataframe.
        """
        return {'full ranking': self.compute_language_proficiency_ranking(),
                'top ten': self.compute_top_ten_languages()}

    def get_data_source(self):
        return self.__source_data


class LanguagesProficienciesPercentages(LanguagesStatsExtractor):
    """
    This class computes languages proficiencies percentages
    """

    def get_data_source(self) -> dict:
        return self.__source_data

    def __init__(self, languages_ranking_extractor: LanguagesRankingExtractor):
        self.__lre = languages_ranking_extractor

    def get_percentages(self) -> pd.Series:
        """
        Retrieves programmers proficiency percentages, using  all languages as reference
        :return: full input data proficiency percentages
        """
        percentages = (self.__lre.compute_language_proficiency_ranking() / self.__lre.get_data_source().shape[0]) * 100
        return percentages

    def get_top_ten_percentages(self) -> pd.Series:
        """
        Retrieves programmers proficiency percentages, using top ten languages only as reference
        :return: top ten languages data proficiency percentages
        """
        percentages = (self.__lre.compute_top_ten_languages() / self.__lre.get_data_source().shape[0]) * 100
        return percentages

    def get_stats(self) -> dict:
        """
        This function returns both proficiency percentages
        :return: both full percentages and top ten languages percentages
        """
        return {'full percentages': self.get_percentages(), 'top ten percentages': self.get_top_ten_percentages()}
