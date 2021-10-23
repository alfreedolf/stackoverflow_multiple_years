from unittest import TestCase

import pandas as pd

from preparation.data_transform import prepare_unnamed


class Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # just empty by now, let's see if it would be needed in the near future...Otherwise:
        # TODO delete
        pass

    def setUp(self) -> None:
        # just empty by now, let's see if it would be needed in the near future...Otherwise:
        # TODO delete
        self.results_2011_df = pd.read_csv("../data/2011_results.csv", encoding="ISO-8859-1")
        self.base_column_name = "Which languages are you proficient in?"
        self.following_column_range = 12

    def test_prepare_unnamed_language_proficiencies(self):
        base_column_index = self.results_2011_df.columns.get_loc(self.base_column_name)
        first_valid_row_index = self.results_2011_df[self.base_column_name].first_valid_index()

        heading_prefix = "Proficient in "
        e_new_first_column_name = heading_prefix + self.results_2011_df.iloc[first_valid_row_index, base_column_index]
        new_result_2011_df = prepare_unnamed(self.results_2011_df, self.base_column_name, self.following_column_range)
        new_first_column_name = new_result_2011_df.columns[base_column_index]
        self.assertEqual(new_first_column_name, e_new_first_column_name)
