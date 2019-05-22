#!/usr/bin/python3

# pip3 install numpy matplotlib pandas scikit-learn gym opencv-python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

###### helper functions#######


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]
##################################################


# Step 1: Read CSV File
df = pd.read_csv("movie_dataset.csv")

# Step 2: extract all the features
features = [
    {"name": "genres", "weight": 1},
    {"name": "director", "weight": 1},
    {"name": "cast", "weight": 1},
    {"name": "keywords", "weight": 1},
]

# Step 3: Compute the Cosine Similarity for each feature based on the count_matrix
cv = CountVectorizer()
cosine_sim_matrices = []
total_weight = sum(feature['weight'] for feature in features)

for feature in features:
	feature_name   = feature['name']
	feature_weight = feature['weight']
	count_matrix   = cv.fit_transform(df[feature_name].fillna(''))
	cosine_sim 	   = cosine_similarity(count_matrix) * feature_weight/total_weight

	cosine_sim_matrices.append(cosine_sim)

# Step 4: Calculate the total cosine similarity matrix
total_cosine_sim = sum(cosine_sim for cosine_sim in cosine_sim_matrices)

# Step 5: Get a list of similar Movies
movie_user_likes = "Skyfall"
movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(total_cosine_sim[movie_index]))

sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

# Step 6: Print titles of top 20 movies
i = 0
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]),"--- sim score: ", (str(element[1])[:5]))
    i = i+1
    if i > 50:
        break
