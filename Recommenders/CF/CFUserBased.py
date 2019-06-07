from Recommenders.CF.CFAlgo import CFAlgo
import numpy as np

class CFUserBased(CFAlgo):

    def __get_similar_users(self, user_raw_id, trainset, similarity_matrix):
        user_inner_id 		   = trainset.to_inner_uid(int(user_raw_id))
        user_similarity_matrix = similarity_matrix[user_inner_id]
        similar_users 		   = []

        for index, similarity in enumerate(user_similarity_matrix):
            similar_users.append([int(trainset.to_raw_uid(index)), similarity])

        return sorted(similar_users, key=lambda tup: tup[1], reverse=True)[:10]

    def get_recommendations(self, user_raw_id, trainset, similarity_matrix):
        similar_users = self.__get_similar_users(user_raw_id, trainset, similarity_matrix)
        recommendations = []
        for user in similar_users:
            user_raw_id     = str(user[0])
            user_similarity = user[1]
            user_ratings    = trainset.ur[int(trainset.to_inner_uid(int(user_raw_id)))]
            user_avg_rating = np.average(np.array(user_ratings), axis=0)[1]
            for user_rating in user_ratings:
                user_rating_value = user_rating[1]
                item_index 		  = user_rating[0]
                item_ratings 	  = trainset.ir[item_index]
                item_avg_rating   = np.average(np.array(item_ratings), axis=0)[1]
                if(len(item_ratings) > 15 and item_avg_rating >3):
                    item_raw_id = trainset.to_raw_iid(item_index)
                    recommendation_value = float((user_rating_value-user_avg_rating) * user_similarity**2)
                    if(recommendation_value != 0):
                        recommendations.append([int(item_raw_id), recommendation_value])

        return sorted(recommendations, key=lambda tup: tup[1], reverse=True)[:70]
