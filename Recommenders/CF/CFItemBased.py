from Recommenders.CF.CFAlgo import CFAlgo
import numpy as np
import pandas as pd

class CFItemBased(CFAlgo):

    def get_recommendations(self, item_raw_id, trainset, similarity_matrix):
        item_inner_id 			= trainset.to_inner_iid(int(item_raw_id))
        items_similarity_matrix = similarity_matrix[item_inner_id]
        similar_items 			= []

        for index, similarity in enumerate(items_similarity_matrix):
            item_ratings    = trainset.ir[index]
            item_avg_rating = np.average(np.array(item_ratings), axis=0)[1]
            if(len(item_ratings) > 15 and item_avg_rating >3):
                similar_items.append([int(trainset.to_raw_iid(index)), similarity])

        return sorted(similar_items, key=lambda tup: tup[1], reverse=True)[:50]
