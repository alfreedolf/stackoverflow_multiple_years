from unittest import TestCase

import numpy as np
import pandas as pd

from preparation.data_stats import map_any_case_to_lower, drop_columns_from_map, LanguagesRankingExtractor


# class TestLanguagesStatsExtractor(TestCase):
#     def test_compute_top_ten_languages(self):
#         self.fail()
#
#
# class TestLanguagesStatsExtractor(TestCase):
#     def test_compute_language_proficiency_ranking(self):
#         self.fail()


class TestDropColumnsFromLowerCaseMap(TestCase):
    def setUp(self) -> None:
        # input output vectors
        self.any_case_input = ['Proficient in Java', 'Proficient in JavaScript', 'Proficient in Javascript']
        self.df_input = pd.DataFrame(index=[1, 2, 3, 4, 5], columns=self.any_case_input)
        self.column_to_drop = 'Proficient in JavaScript'

        # expected output vectors
        self.expected_output_map = {'proficient in java': ['Proficient in Java'],
                                    'proficient in javascript': ['Proficient in JavaScript',
                                                                 'Proficient in Javascript']}
        self.expected_output_columns = ['Proficient in Java']
        self.df_expected_output = pd.DataFrame(index=[1, 2, 3, 4, 5], columns=self.expected_output_columns)

    def test_map_any_case_to_lower(self):
        out_map = map_any_case_to_lower(self.any_case_input)
        self.assertEqual(out_map, self.expected_output_map)

    def test_drop_columns_from_map(self):
        df_output = drop_columns_from_map(self.df_input, dropping_map=self.expected_output_map,
                                          column_to_drop=self.column_to_drop.lower())
        self.assertEqual(df_output.columns, self.df_expected_output.columns)


class TestLanguagesRankingExtractor(TestCase):

    def setUp(self) -> None:
        # input dataframe initialization
        # input index
        self.input_index = [1, 2, 3, 4]

        # input columns
        self.input_columns = ['Proficient in Java', 'Proficient in C++', 'Proficient in C#', 'Proficient in Python',
                              'Proficient in Ruby', 'Proficient in C', 'Proficient in JavaScript',
                              'Proficient in Objective-C', 'Proficient in Visual Basic', 'Proficient in PHP',
                              'Proficient in Node.js', 'Proficient in jQuery']

        # input data
        data = [[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
                [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
                [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
                [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]]
        self.df_input = pd.DataFrame(data=data, index=self.input_index, columns=self.input_columns)

        # expected output
        self.s_expected_output_index = ['JavaScript', 'Java', 'Python',
                                        'PHP', 'C++', 'C#',
                                        'C', 'Visual Basic', 'Ruby',
                                        'Objective-C']
        self.s_expected_output = pd.Series(index=self.s_expected_output_index, data=[4, 3, 3, 3, 2, 2, 2, 2, 1, 1])

        # entries merge list
        self.entries_merge_list = [""]

        # input LanguagesStatsExtractor
        self.lre = LanguagesRankingExtractor(source_data=self.df_input, prefix_to_remove='Proficient in ',
                                             entries_merge_list=[('JavaScript', 'Node.js'), ('JavaScript', 'jQuery')])

    def test_compute_top_ten_languages(self):
        top_ten_languages_df: pd.DataFrame = self.lre.compute_top_ten_languages()
        # check for index equality
        with self.subTest():
            np.testing.assert_array_equal(top_ten_languages_df.index.values,
                                          self.s_expected_output.index.values)
        # check for values equality
        with self.subTest():
            np.testing.assert_array_equal(top_ten_languages_df.values,
                                          self.s_expected_output.values)

    def test_compute_language_proficiency_ranking(self):
        # TODO add test
        # language_proficiencies_ranking_df = self.lre.compute_language_proficiency_ranking()
        pass

    def test_get_stats(self):
        # TODO add test
        pass

