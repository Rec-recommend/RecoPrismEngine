#!/usr/bin/env python3

from CollborativeRecommender import CollborativeRecommender
import pandas as pd

# dict for movies names and ids
# --------------------------------

movies_df = pd.read_csv('./Recommenders/movies.csv')
movieID_to_name = {}

for index, row in movies_df.iterrows():
	movieID = int(row[0])
	movieName = row[1]
	movieID_to_name[movieID] = movieName

# --------------------------------

file_path = "./Recommenders/ratings.1.csv"
line_format = 'user item rating'
sim_options = {'name': 'pearson_baseline', 'user_based': False, 'min_support': 15}

cfr = CollborativeRecommender(sim_options, file_path, line_format)


movies = ['115617', '2424', '54001', '88163']

for movie in movies:
	res = cfr.get_recommendations(movie)
	for movie in res:
		print(movieID_to_name[movie[0]] , " ---- " , movie[1])
	print("--------------------------------------")

















# class CollborativeRecommenderFactory():

# 	@staticmethod
# 	def get_cf_recommender(sim_options, file_path, line_format):
# 		if sim_options['user_based'] == True:
# 			return CFUserBased(sim_options, file_path, line_format)
# 		else:
# 			return CFItemBased(sim_options, file_path, line_format)


	# def hybrid(self, msql_id):
	# 	similar_users = self.get_similar_users(msql_id)[:5]
	# 	user_liked_movies = []
	# 	recommendations = []
	# 	for user in similar_users:
	# 		user_raw_id     = str(user[0])
	# 		user_similarity = user[1]
	# 		user_ratings    = self.trainset.ur[int(self.trainset.to_inner_uid(user_raw_id))]
	# 		user_avg_rating = np.average(np.array(user_ratings), axis=0)[1]
	# 		for user_rating in user_ratings:
	# 			user_rating_value = user_rating[1]
	# 			item_index 		  = user_rating[0]
	# 			item_raw_id = self.trainset.to_raw_iid(item_index)
	# 			user_liked_movies.append(item_raw_id)
	# 	return user_liked_movies



# print(res)
# print(res2)
# # print(res3)
# for s in res2:
#     print(*s)

# print("------------------------------------")

# for s in res3:
#     print(*s)

# print(cfr.hybrid(2))









# r = redis.Redis(host='localhost', port=6379, db=0)
# self.similarity_matrix = json.loads(r.get('sim_matrix2'))
# sim_matrix_json = json.dumps(self.similarity_matrix.tolist())
# r.set('sim_matrix2', sim_matrix_json)
# r.get('sim_matrix')