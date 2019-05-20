#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np 
from surprise import KNNWithMeans, KNNBasic
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split


from MovieLens import MovieLens

# ml = MovieLens()
# ml.loadMovieLensLatestSmall()

# Load the movielens-100k dataset  UserID::MovieID::Rating::Timestamp
reader = Reader(line_format='user item rating timestamp', rating_scale=(0, 5), skip_lines=1, sep=',')
data = Dataset.load_from_file('../ml-latest-small/ratings.csv',reader)

# trainset, testset = train_test_split(data, test_size=.15)
trainset = data.build_full_trainset()
sim_options={'name': 'pearson_baseline', 'user_based': True}

# algo = KNNWithMeans(k=50, )
algo = KNNBasic(sim_options=sim_options)
algo.fit(trainset)


# we can now query for specific predicions
uid = str(2)  # raw user id
iid = str(3991)  # raw item id

# get a prediction for specific users and items.
pred = algo.predict(uid, iid, r_ui=1, verbose=True)
user_similarities = []

similarity_matrix = algo.compute_similarities()
user_similarity_matrix = similarity_matrix[int(uid)-1]

for index, similarity in enumerate(user_similarity_matrix):
        user_similarities.append([index,similarity])


similar_users = sorted(user_similarities, key=lambda tup: tup[1], reverse=True)
print(similar_users)
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