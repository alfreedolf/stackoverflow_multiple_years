"""Test Data Binarization

"""
import os
import unittest

import numpy as np
import pandas as pd

from preparation.data_transform import binarize_column, binarize_columns_range


def _contains_all_true_values(df: pd.DataFrame):
    """Checks if input dataframe is all made of 1 values

    Args:
        df (pd.DataFrame): input dataframe made of binary values in [1, 0]

    Returns:
        bool: True if every value is 0
    """
    nd_df = df.to_numpy()  # s.values (pandas<0.24)
    return (nd_df[0] == 1).all()


def _contains_all_false_values(df: pd.DataFrame):
    """Checks if input dataframe is all made of 1 values

    Args:
        df (pd.DataFrame): input dataframe made of binary values in [1, 0]

    Returns:
        bool: True if every value is 0
    """
    nd_df = df.to_numpy()  # s.values (pandas<0.24)
    return (nd_df[0] == 0).all()


def _contains_binary_values_only(df: pd.DataFrame):
    """Checks if input DataFrame is made of binary values only

    Args:
        df (pd.DataFrame): input pandas DataFrame

    Returns:
        bool: True if every value in the dataframe is in  [0, 1]
    """
    nd_df = df.to_numpy()  # s.values (pandas<0.24)
    return not (np.any(nd_df[0] > 1) and np.any(nd_df[0] < 0))


class TestBinarization(unittest.TestCase):
    """Test case for binarization
    """

    def setUp(self) -> None:
        """Setup function"""
        dummy_lp_data = {"python_proficient": ["python", np.NaN, "python"], "java_proficient": [np.NaN, "java", np.NaN]}
        self.df_binarizable = pd.DataFrame(data=dummy_lp_data)

        # data load
        base_dir = os.getcwd()
        results_2015_file_path = os.path.join(base_dir, "data", "2015_results.csv")
        self.results_2015_df = pd.read_csv(results_2015_file_path, encoding="ISO-8859-1")

        # fixing 2015 results header
        new_2015_header = self.results_2015_df.iloc[0]
        self.results_2015_df = self.results_2015_df[1:]
        self.results_2015_df.columns = new_2015_header

        # Columns Range Of Interest definition
        self.results_2015_croi = range(8, 50)

        # computing valid values
        self.results_2015_fvi = []
        self.results_2015_true_values = []
        for col in self.results_2015_df.iloc[:, self.results_2015_croi].columns:
            valid_row = self.results_2015_df[col].first_valid_index()
            # rows of interest
            self.results_2015_fvi.append(valid_row)
            self.results_2015_true_values.append(
                self.results_2015_df.iloc[valid_row, self.results_2015_df.columns.get_loc(col)]
            )

    def test_binarize_columns_range(self):
        """Tests that the column range is binarized by binarize_column_range function"""
        # computing expected output
        binarize_columns_range(self.results_2015_df, self.results_2015_croi, self.results_2015_true_values)
        df_binarized = self.results_2015_df.iloc[self.results_2015_fvi, self.results_2015_croi]
        self.assertTrue(
            _contains_binary_values_only(df_binarized),
            msg=f"""
            Binarizable values = {self.results_2015_df.iloc[:, self.results_2015_croi]}, \n
            True values = {self.results_2015_true_values}, \n
            binarized column = {df_binarized}"
            """,
        )

    def test_binarize_column(self):
        """Tests that a single column is being binarized by binarize_column function"""
        binarize_column(self.df_binarizable, col_name="python_proficient", true_val="python")
        self.assertTrue(_contains_binary_values_only(self.df_binarizable))


if __name__ == "__main__":
    unittest.main()
