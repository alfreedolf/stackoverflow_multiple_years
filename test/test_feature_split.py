"""Test module for feature split
"""
import unittest
from typing import List

import numpy as np
import pandas as pd

from preparation.data_transform import feature_split


class TestFeatureSplit(unittest.TestCase):
    """Feature split test case
    """
    expected_columns_names: List[str]

    def setUp(self) -> None:
        # data load
        self.results_mockup = pd.DataFrame(
            data={'tech_do': ["java;python", "c++;c;javascript", "c++;c;java;javascript"]})

        # data split
        self.split_results_mockup_df = feature_split(self.results_mockup, 'tech_do', inplace=False)

        # expected values
        self.expected_column_number = 5

        self.expected_columns_names = ["tech_do: java", "tech_do: python",
                                       "tech_do: c++", "tech_do: c", "tech_do: javascript", ]
        self.expected_columns_names.sort()

        self.expected_binarized_features = np.array([[1, 1, 0, 0, 0], [0, 0, 1, 1, 1], [1, 0, 1, 1, 1]])

    def test_feature_split_features_count(self):
        """test that split count is correct
        """
        split_features_count = len(self.split_results_mockup_df.columns)
        self.assertEqual(self.expected_column_number, split_features_count)

    def test_feature_split_features_names(self):
        """test that split names are correct
        """
        columns = self.split_results_mockup_df.columns.values
        columns.sort()
        self.assertTrue((self.expected_columns_names == columns).all(),
                        msg="expected_column_names = {}, instead got = {}".format(self.expected_columns_names, columns))

    def test_feature_split_features_binarized(self):
        """test that split binarized features are split
        """
        binarized_features = self.split_results_mockup_df.to_numpy()
        np.testing.assert_array_equal(self.expected_binarized_features, binarized_features)
        # self.assertTrue(self.expected_binarized_features, binarized_features)


if __name__ == '__main__':
    unittest.main()
