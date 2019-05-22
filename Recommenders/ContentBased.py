#!/usr/bin/python3

# pip3 install numpy matplotlib pandas scikit-learn gym opencv-python
import pandas as pd
import numpy  as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender():
    def __init__(self, file_path, features):
        self.df       = pd.read_csv(file_path)
        self.features = features
        self.cosine_sim_matrix = []


    def set_features(self, features):
        self.features = features


    def calc_cosine_sim_matrix(self):
        cv = CountVectorizer()
        cosine_sim_matrices = []
        total_weight = self.__calc_features_weight_sum()

        for feature in features:
            feature_name   = feature['name']
            feature_weight = feature['weight']
            count_matrix   = cv.fit_transform(self.df[feature_name].fillna(''))
            cosine_sim 	   = cosine_similarity(count_matrix) * feature_weight/total_weight

            cosine_sim_matrices.append(cosine_sim)

        self.cosine_sim_matrix = self.__calc_total_weighted_sim(cosine_sim_matrices)

        return self.cosine_sim_matrix


    def get_cosine_sim_matrix(self):
        return self.cosine_sim_matrix


    def get_similar_items(self, item_name):
        item_index = self.get_index_from_name(item_name)
        similar_items = list(enumerate(self.cosine_sim_matrix[item_index]))
        return sorted(similar_items, key=lambda x: x[1], reverse=True)


    def get_title_from_index(self, index):
        return self.df[self.df.index == index]["title"].values[0]


    def get_index_from_name(self, name):
        return self.df[self.df.title == name]["index"].values[0]


    def __calc_features_weight_sum(self):
        return sum(feature['weight'] for feature in self.features)


    def __calc_total_weighted_sim(self, cosine_sim_matrices):
        return sum(cosine_sim for cosine_sim in cosine_sim_matrices)



# ##################################################
# file_path = "movie_dataset.csv"
# item_name = "Skyfall"

# features = [
#     {"name": "genres", "weight": 1},
#     {"name": "director", "weight": 1},
#     {"name": "cast", "weight": 1},
#     {"name": "keywords", "weight": 1},
# ]

# rec = ContentBasedRecommender(file_path, features)
# rec.calc_cosine_sim_matrix()
# rec.get_similar_items(item_name)

# i = 0
# for element in rec.get_similar_items(item_name):
#     print(rec.get_title_from_index(element[0]),"--- sim score: ", (str(element[1])[:5]))
#     i = i+1
#     if i > 50:
#         break