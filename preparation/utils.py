import pandas as pd


def map_languages_to_color_list(languages_color_palette: dict, s_2011_proficiencies_top_10: pd.Series) -> list[str]:
    # mapping values from dictionary to palette color list to be fed to plot bar code
    return [languages_color_palette[s_2011_proficiencies_top_10.index[i]] for i in
            range(len(s_2011_proficiencies_top_10))]


class LanguagesStatsExtractor:

    def __init__(self, source_data: pd.DataFrame):
        self.__source_data = source_data

    def compute_top_ten_languages(self, languages_proficiency_column_range, exclusion_list=[]) -> pd.Series:
        """
        Computes top ten languages by proficiency.
        :param languages_proficiency_column_range: a range variable, used to slice language proficiency from source data
        :param exclusion_list: languages to be excluded from final results
        :return: a Pandas series of at most 10 elements, containing top languages by proficiency, ordered from the most
        to the least popular.
        """

        # retrieving languages proficiencies ranking in descending order
        s_2011_proficiencies_clean_sum = self.compute_language_proficiency_ranking(languages_proficiency_column_range,
                                                                                   exclusion_list, False)

        # storing top ten elements by popularity in a dedicated pandas series
        s_2011_proficiencies_top_10 = s_2011_proficiencies_clean_sum.head(10)

        return s_2011_proficiencies_top_10

    def compute_language_proficiency_ranking(self, languages_proficiency_column_range, exclusion_list=[],
                                             ascending=False) -> pd.Series:
        """
        Computes language proficiency ranking on source data, given a selected column range containing
        language proficiencies data.
        :param languages_proficiency_column_range: a range variable, used to slice language proficiency from source data
        :param exclusion_list: languages to be excluded from final results
        :param ascending: if True, the returning value will be ordered in ascending order
        :return: a Pandas Series containing language proficiency ranking, obtained through summation of values
        from selected range, excepting values from exclusion list.
        """
        # slicing features columns containing language proficiencies data
        df_proficiencies: pd.DataFrame = self.__source_data.iloc[:, languages_proficiency_column_range]

        # excluding selected language from computation
        for to_be_excluded in exclusion_list:
            df_proficiencies = df_proficiencies.drop(to_be_excluded, axis=1)

        # computing total proficiencies
        s_2011_proficiencies_clean_sum: pd.Series = df_proficiencies.sum(axis=0)

        # sorting values by popularity
        s_2011_proficiencies_clean_sum.sort_values(ascending=ascending, inplace=True)

        return s_2011_proficiencies_clean_sum
