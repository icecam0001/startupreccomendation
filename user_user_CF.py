from utils import total_compute, load_data, calculate_combined_similarity
from heapq import nlargest
import math
# user_similarity_recommender.py
class UserSimilarityRecommender:

    
    def recommend(self, user_id, n=30):
        projectdict, userdictionary, tagdict = load_data()
        fullneighborhood = {}
        scoreneighborhood = {}
        for user in userdictionary:
            similarityscore = calculate_combined_similarity(user, user_id, userdictionary, tagdict, 0.6, 0.4)
            fullneighborhood[user] = similarityscore
        fullneighborhood = dict(nlargest(30, fullneighborhood.items(), key=lambda item: item[1]))
        for user in fullneighborhood:
            for item in userdictionary[user]:
                if scoreneighborhood.__contains__(item):
                    scoreneighborhood[item]+=1
                else:
                    scoreneighborhood[item] = 1
        for item in scoreneighborhood:
            scoreneighborhood[item] = scoreneighborhood[item]/math.sqrt(projectdict[item]['contributor_count'])
        topnitems = [item[0] for item in nlargest(n, scoreneighborhood.items(), key=lambda item: item[1])]
        return topnitems
        