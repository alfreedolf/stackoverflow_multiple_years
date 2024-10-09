"""This module contains statistics on data."""
from abc import ABC, abstractmethod
from collections import defaultdict

import pandas as pd
from pandas import DataFrame


def map_any_case_to_lower(any_case_input: list) -> dict:
    """Map a list of strings values, given as input in any kind of casing combination, to a lower case corresponding key.
    
    The result is a hash map in which each element has as key a lowercase string and
    as values a list of corresponding strings in any case combination.
    :param any_case_input: a list of any case combination list
    :return: a dictionary containing a list of strings corresponding to the key
    :rtype: dict
    """
    output_map = defaultdict(list)
    for s in any_case_input:
        output_map[s.lower()].append(s)
    return output_map


def drop_columns_from_map(df: object, dropping_map: object, column_to_drop: str) -> pd.DataFrame:
    """
    This function drops a set of columns given a dictionary of columns
    :param df:
    :param dropping_map:
    :param column_to_drop:
    :return: the input dataframe, without any occurrence of string_to_drop, in any case combination
    """ 
    for tbe in dropping_map[column_to_drop]:
        # "SettingWithCopyWarning" in Jupyter Notebook solved, going from:
        # df.drop(tbe, axis=1, inplace=True) to:
        df = df.drop(tbe, axis=1, inplace=False)
    return df


class LanguagesStatsExtractor(ABC):
    """
    This is just an abstract base class that allows to define specific kind of stats extraction from a Dataframe
    """

    @abstractmethod
    def __init__(self, source_data: pd.DataFrame):
        self.__source_data = source_data

    @abstractmethod
    def get_data_source(self) -> DataFrame:
        return self.__source_data

    @abstractmethod
    def get_stats(self) -> dict:
        pass


class LanguagesRankingExtractor(LanguagesStatsExtractor):

    def __init__(self, source_data: pd.DataFrame, columns_selection_criteria=None,
                 exclusion_list=None, entries_merge_list=None, prefix_to_remove=''):
        """

        :type entries_merge_list: list
        :param source_data:
        :param columns_selection_criteria: a range variable or a string,
        used to slice language proficiency from source data.
        :param exclusion_list: languages to be excluded from final results
        :param prefix_to_remove: an optional string to be removed from returned series index
        :param entries_merge_list: this should be a list of couples. If provided, it will add values from tuple second
        element label to tuple first element label.
        """
        if entries_merge_list is None:
            entries_merge_list = []
        if exclusion_list is None:
            exclusion_list = []
        self.__source_data = source_data
        self.__columns_selection_criteria = columns_selection_criteria
        self.__prefix_to_remove = prefix_to_remove
        self.__exclusion_list = exclusion_list
        self.__entries_merge_list = entries_merge_list
        self.__language_proficiency_ranking = None
        self.__top_ten_languages = None

    def compute_top_ten_languages(self, ignore_case=True) -> pd.Series:
        """
        Computes top ten languages by proficiency.
        :param ignore_case: if True, the method will look for elements in exclusion_list to be in source dataframe,
        ignoring occurrences casing (upper or lower case)
        :return: a Pandas' series of at most 10 elements, containing top languages by proficiency, ordered from the most
        to the least popular.
        """

        # TODO check for removal
        # if self.__columns_selection_criteria is None:
        #     columns_selection_criteria = range(0, self.__source_data.shape[1])
        if self.__language_proficiency_ranking is None:
            # retrieving languages proficiencies ranking in descending order
            self.__language_proficiency_ranking = self.compute_language_proficiency_ranking(ignore_case=ignore_case)

        # storing top ten elements by popularity in a dedicated pandas series
        self.__top_ten_languages = self.__language_proficiency_ranking.iloc[:10]
        # s_proficiencies_top_10 = self.__language_proficiency_ranking.head(10)

        # rectifying index name as requested
        self.__top_ten_languages.index = self.__top_ten_languages.index.str.replace(self.__prefix_to_remove, '')
        # s_proficiencies_top_10.index = s_proficiencies_top_10.index.str.replace(self.__prefix_to_remove, '')

        return self.__top_ten_languages

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
                df_proficiencies.drop(to_be_excluded, axis=1, inplace=True)
            else:
                print(f"Error finding feature '{to_be_excluded}' in axis")

        # merging entries from entries_merge_list, if not empty
        if self.__entries_merge_list:
            self.merge_entries(df_proficiencies, self.__entries_merge_list)

        # computing total proficiencies
        s_proficiencies_clean_sum: pd.Series = df_proficiencies.sum(axis=0, numeric_only=True)

        # sorting values by popularity
        self.__language_proficiency_ranking = s_proficiencies_clean_sum.sort_values(ascending=ascending)
        # s_proficiencies_clean_sum.sort_values(ascending=ascending, inplace=True)

        return self.__language_proficiency_ranking

    def merge_entries(self, df_proficiencies: pd.DataFrame, entries_merge_list: list) -> None:
        """
        Method that merges proficiencies entries
        :param df_proficiencies: input dataframe
        :param entries_merge_list: entries tuples merge list
        """
        for t in entries_merge_list:
            # summing columns to be merged
            merger = self.__prefix_to_remove + t[0]
            mergee = self.__prefix_to_remove + t[1]
            # rows where reference data (merger) used in final statistics has a "miss", i.e. is set to '0'
            condition_row = df_proficiencies.loc[:, merger] == 0

            df_proficiencies.loc[condition_row, merger] = df_proficiencies.loc[condition_row, mergee]
            # dropping merged column
            df_proficiencies.drop(mergee, axis=1, inplace=True)

    def get_stats(self) -> dict:
        """
        This method returns a dictionary holding two values: full ranking and top ten languages from input dataframe
        :return: a dictionary holding two values: full ranking and top ten languages from input dataframe.
        """
        if self.__language_proficiency_ranking is None:
            self.compute_language_proficiency_ranking()
        if self.__top_ten_languages is None:
            self.compute_top_ten_languages()
        return {'full ranking': self.__language_proficiency_ranking, 'top ten languages': self.__top_ten_languages}

    
    def get_data_source(self):
        return self.__source_data

    
    


class LanguagesProficienciesPercentages(LanguagesStatsExtractor):
    """
    This class computes languages proficiencies percentages
    """

    def get_data_source(self) -> DataFrame:
        return self.__lre.get_data_source()

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
        """Retrieve proficiency percentages.
        
        Description
        :return: number of respondents, proficiency percentages and top ten languages percentages
        """
        return {'number respondents': self.get_data_source().shape[1],
                'proficiency percentages': self.get_percentages(),
                'top ten proficiency percentages': self.get_top_ten_percentages()}

    
    def platform_shares(self, platform: str, language_feature_name_pattern: str="^LanguageWorkedWith.*") -> pd.Series:
        """Compute percentages share of languages on a specified platform.

        Args:
            platform (str): name of the platform (operating system or similar) used as reference for computing percentages
            language_feature_name_pattern (str, optional): _description_. Defaults to "LanguageWorkedWith".

        Returns:
            list: list of share of languages with reference to the platform
        """
        # TODO: check if meaningful, otherwise delete it
        
        # languages used on the platform
        platform_condition = self.__lre.get_data_source()["PlatformWorkedWith"] == platform
        # languages from datasource
        df_languages_filtered = self.__lre.get_data_source().filter(regex=language_feature_name_pattern, axis=1)
        df_languages_shares = df_languages_filtered[df_languages_filtered.eq(1).any(axis=1) & platform_condition]
        # sum on columns
        # computing total proficiencies
        s_proficiencies_clean_sum: pd.Series = df_languages_shares.sum(axis=0, numeric_only=True)
        languages_proficiency_on_platform_ranking = s_proficiencies_clean_sum.sort_values(ascending=False)

        return languages_proficiency_on_platform_ranking

    def joint_share(self, languages: list, unison: bool=False,
                    platform_key: str="PlatformWorkedWith", platform: str=None) -> float:
        """Compute languages experience joint share with reference to a platform.

        A percentage value that expresses the size of the languages list share on a selected platform is
        In case platform is set to None, the share is computed over the whole population.

        Args:
            languages (list): list of languages considered in the share computation
            unison (bool, optional): If true, will indi. Defaults to False.
            platform (str, optional): _description_. Defaults to None.

        Returns:
            float: share percentage of the languges
        """
        if platform is None:
            platform_condition = True
            population_size = self.__lre.get_data_source().shape[0]
        else:
            platform_condition = self.__lre.get_data_source()[platform_key] == platform
            population_size = self.__lre.get_data_source()[platform_condition].shape[0]
        
        if unison:
            share_sum = self.__lre.get_data_source()[((self.__lre.get_data_source()[languages] !=0).all(axis=1)) & platform_condition].shape[0]
        else:
            share_sum = self.__lre.get_data_source()[((self.__lre.get_data_source()[languages] !=0).any(axis=1)) & platform_condition].shape[0]

        return (share_sum/population_size) * 100
    
    def exclusive_share(self, ref_language: str, excluded_languages: list, platform: str=None) -> float:
        """Compute languages experience share of a language, subtracting shares of a list of languages.
        
        In case platform is set to None, the share is computed over the whole population.

        :return: share percentage of the languges
        """
        if platform is None:
            platform_condition = True
            population_size = self.__lre.get_data_source().shape[0]
        else:
            platform_condition = self.__lre.get_data_source()["PlatformWorkedWith"] == platform
            population_size = self.__lre.get_data_source()[platform_condition].shape[0]
        
        reference_language_mask = self.__lre.get_data_source()[ref_language] != 0

        ref_share = self.__lre.get_data_source()[reference_language_mask & (self.__lre.get_data_source()[excluded_languages] == 0).all(axis=1) & platform_condition].shape[0]

        return (ref_share/population_size) * 100

    def intersection_percentage(self, language_1: str, language_2: str, overall: bool=False) -> float:
        """Compute and return cardinality of the intersection set of respondents that have declared to have worked with language_1 also have declared to have been working in language_2.

        :param: overall if true, the intersection percentage will be co returned with respect to the full population of respondents, otherwise, respect to language_1 population
        
        :return: overlap cardinality, in percentage
        """
        if overall:
            base_count = self.__lre.get_data_source().shape[0]
        else:
            base_count = self.__lre.get_data_source()[self.__lre.get_data_source()[language_1] != 0].shape[0] 
            
        
        overlap_count = self.__lre.get_data_source()[(self.__lre.get_data_source()[language_1] != 0)  &  (self.__lre.get_data_source()[language_2] != 0)].shape[0]

        overlap = (overlap_count / base_count) * 100
        return overlap

    def difference_percentage(self, language_1: str, language_2: str, union_relative: bool=False) -> float:
        """Compute and returns the cardinality of the intersection set of respondents that have declared to have worked with language_1 also have declared to have been working in language_2.

        :param: union_relative if true, the base to compute the percentage, will be the cardinality of union of language_1 and language_2 respondents, otherwise it will be language_1 population cardinality
        """
        if union_relative:
            base_count = self.__lre.get_data_source()[(self.__lre.get_data_source()[language_1] != 0)  &  (self.__lre.get_data_source()[language_2] != 0)].shape[0]
        else:
            base_count = self.__lre.get_data_source()[self.__lre.get_data_source()[language_1] != 0].shape[0] 
            
        difference_count = (self.__lre.get_data_source()[(self.__lre.get_data_source()[language_1] != 0)  &  (self.__lre.get_data_source()[language_2] == 0)].shape[0])

        difference = (difference_count / base_count) * 100
        return difference

