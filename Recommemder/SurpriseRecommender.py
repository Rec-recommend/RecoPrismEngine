#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from surprise import KNNWithMeans, KNNBasic
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split

# from MovieLens import MovieLens

class CollborativeRecommender():
	def __init__(self, file_path, line_format):
		reader = Reader(line_format=line_format, rating_scale=(0, 5), skip_lines=1, sep=',')
		dataset = Dataset.load_from_file(file_path, reader)
		self.trainset = dataset.build_full_trainset()
		self.similarity_matrix = []

	def set_sim_options(self, sim_options):
		self.sim_options = sim_options

	def calc_sim_matrix(self):
		algo = KNNBasic(sim_options=self.sim_options)
		algo.fit(self.trainset)
		self.similarity_matrix = algo.compute_similarities()

	def get_similar_users(self, uid):
		similar_users = []
		user_similarity_matrix = self.similarity_matrix[uid]


		for index, similarity in enumerate(user_similarity_matrix):
			similar_users.append([int(self.trainset.to_raw_uid(index))-1, similarity])

		return sorted(similar_users, key=lambda tup: tup[1], reverse=True)


file_path = "ratings.csv"
line_format = 'user item rating timestamp'
sim_options = {'name': 'pearson_baseline', 'user_based': True}

cfr = CollborativeRecommender(file_path, line_format)
cfr.set_sim_options(sim_options)
cfr.calc_sim_matrix()

print(cfr.get_similar_users(2))






# ml = MovieLens()
# ml.loadMovieLensLatestSmall()

# Load the movielens-100k dataset  UserID::MovieID::Rating::Timestamp

# trainset, testset = train_test_split(data, test_size=.15)
# algo = KNNWithMeans(k=50, )


# # we can now query for specific predicions
# uid = str(2)  # raw user id
# iid = str(3991)  # raw item id

# # get a prediction for specific users and items.
# pred = algo.predict(uid, iid, r_ui=1, verbose=True)

# print(similar_users)
# most_sim_user_rated_movies = ml.getUserRatings(most_sim_user_id)

# for movie_id in most_sim_user_rated_movies:
# print(ml.getMovieName(movie_id))

# # run the trained model against the testset
# test_pred = algo.test(testset)

# # get RMSE
# print("User-based Model : Test Set")
# accuracy.rmse(test_pred, verbose=True)

# # if you wanted to evaluate on the trainset
# print("User-based Model : Training Set")
# train_pred = algo.test(trainset.build_testset())
# accuracy.rmse(train_pred)
