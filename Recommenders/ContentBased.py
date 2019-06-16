#!/usr/bin/python3

# pip3 install numpy matplotlib pandas scikit-learn gym opencv-python
import pandas as pd
import numpy  as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender():
    def __init__(self, df, features):
        self.df = df
        self.features = features
        self.cosine_sim_matrix = []


    def set_features(self, features):
        self.features = features


    def calc_cosine_sim_matrix(self):
        cv = CountVectorizer()
        cosine_sim_matrices = []
        total_weight = self.__calc_features_weight_sum()

        for feature in self.features:
            feature_label   = feature['label']
            feature_weight = feature['weight']
            count_matrix   = cv.fit_transform(self.df[feature_label].fillna(''))
            cosine_sim 	   = cosine_similarity(count_matrix) * feature_weight/total_weight

            cosine_sim_matrices.append(cosine_sim)

        self.cosine_sim_matrix = self.__calc_total_weighted_sim(cosine_sim_matrices)
        return self.cosine_sim_matrix


    def get_cosine_sim_matrix(self):
        return self.cosine_sim_matrix


    def get_similar_items(self, item_index):
        item_index    = self.get_row_from_db_id(item_index)
        similar_items = list(enumerate(self.cosine_sim_matrix[item_index]))
        similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[0:10]
        similar_items = [self.get_db_id_from_row(item[0]) for item in similar_items]

        return similar_items


    def get_row_from_db_id(self, item_id):
        return int(self.df[self.df.item_id == item_id].index.values[0])

    def get_db_id_from_row(self, index):
        return int(self.df[self.df.index == index]['item_id'].values[0])


    def __calc_features_weight_sum(self):
        return sum(feature['weight'] for feature in self.features)


    def __calc_total_weighted_sim(self, cosine_sim_matrices):
        return sum(cosine_sim for cosine_sim in cosine_sim_matrices)
