import unittest
from typing import List

import numpy as np
import pandas as pd

from preparation.data_transform import feature_split


class TestFeatureSplit(unittest.TestCase):
    expected_columns_names: List[str]

    def setUp(self) -> None:
        # data load
        self.results_mockup = pd.DataFrame(data={'tech_do': ["java;python", "c++;c;javascript"]})

        # data split
        self.split_results_mockup_df = feature_split(self.results_mockup, 'tech_do', inplace=False)

        # expected values
        self.expected_column_number = 5

        self.expected_columns_names = ["tech_do: c", "tech_do: c++",
                                       "tech_do: java", "tech_do: javascript", "tech_do: python", ]
        self.expected_columns_names.sort()

        self.expected_binarized_features = np.array([[0, 0, 1, 0, 1], [1, 1, 0, 1, 0]])

    def test_feature_split_features_count(self):
        split_features_count = len(self.split_results_mockup_df.columns)
        self.assertEqual(self.expected_column_number, split_features_count)

    def test_feature_split_features_names(self):
        columns = self.split_results_mockup_df.columns.values
        self.assertTrue((self.expected_columns_names == columns).all(),
                        msg="expected_column_names = {}, instead got = {}".format(self.expected_columns_names, columns))

    def test_feature_split_features_binarized(self):
        binarized_features = self.split_results_mockup_df.to_numpy()
        np.testing.assert_array_equal(self.expected_binarized_features, binarized_features)
        # self.assertTrue(self.expected_binarized_features, binarized_features)


if __name__ == '__main__':
    unittest.main()
