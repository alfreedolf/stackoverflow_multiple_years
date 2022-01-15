from unittest import TestCase

import pandas as pd

from preparation.data_stats import map_any_case_to_lower, drop_columns_from_map


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
