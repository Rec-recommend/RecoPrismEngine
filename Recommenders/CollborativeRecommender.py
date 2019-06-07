from Recommenders.CF.CFAlgoFactory import CFAlgoFactory
from surprise import KNNWithMeans, KNNBasic, SVD, NMF
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split
import pandas as pd


class CollborativeRecommender():
    def __init__(self, sim_options, df, line_format):
        reader = Reader(line_format=line_format, skip_lines=1, sep=' ')
        dataset = Dataset.load_from_df(df, reader)
        self.trainset 		   = dataset.build_full_trainset()
        self.similarity_matrix = []
        self.set_cf_type(sim_options)
        self.__calc_sim_matrix()

    def set_cf_type(self, sim_options):
        self.sim_options = sim_options
        self.cf_algo     = CFAlgoFactory.get_cf_algo(sim_options)

    def get_recommendations(self, raw_id):
        return self.cf_algo.get_recommendations(raw_id, self.trainset, self.similarity_matrix)

    def __calc_sim_matrix(self):
        algo = KNNBasic(sim_options=self.sim_options)
        algo.fit(self.trainset)
        self.similarity_matrix = algo.compute_similarities()
