import pandas as pd
import numpy as np


class StrokeDTClassifier:
    def __init__(self, csv_filename, index):
        self.dataframe = csv_data = pd.read_csv(csv_filename, index_col=index)
        csv_data.head()
        self.index_ids = self.dataframe.index

    def test_accuracy(self):
        pass
