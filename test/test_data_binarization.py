import unittest

import pandas as pd
from numpy import NaN

from preparation.data_transform import binarize_column, binarize_columns_range


def _is_binary(df):
    nd_df = df.to_numpy()  # s.values (pandas<0.24)
    return (nd_df[0] == 1).all()


class TetCase2(unittest.TestCase):

    def setUp(self) -> None:
        dummy_lp_data = {'python_proficient': ['python', NaN, 'python'], 'java_proficient': [NaN, 'java', NaN]}
        self.df_binarizable = pd.DataFrame(data=dummy_lp_data)

        # data load
        self.results_2015_df = pd.read_csv("../data/2015_results.csv", encoding="ISO-8859-1")

        # fixing 2015 results header
        new_2015_header = self.results_2015_df.iloc[0]
        self.results_2015_df = self.results_2015_df[1:]
        self.results_2015_df.columns = new_2015_header

        # Columns Range Of Interest definition
        self.results_2015_CROI = range(8, 50)

        # computing valid values
        self.results_2015_FVI = []
        self.results_2015_true_values = []
        for i_col, col in enumerate(self.results_2015_df.columns):
            valid_row = self.results_2015_df[col].first_valid_index()
            # rows of interest
            self.results_2015_FVI.append(valid_row)
            self.results_2015_true_values.append(self.results_2015_df.iloc[valid_row, i_col])

    def test_binarize_columns_range(self):
        # computing expected output
        binarize_columns_range(self.results_2015_df, self.results_2015_CROI, self.results_2015_true_values)
        df_binarized = self.results_2015_df.iloc[self.results_2015_FVI, self.results_2015_CROI]

        self.assertTrue(_is_binary(df_binarized))

    def test__binarize_column(self):
        binarize_column(self.df_binarizable, col_name='python_proficient', true_val='python')
        self.assertTrue(_is_binary(self.df_binarizable))


if __name__ == '__main__':
    unittest.main()
