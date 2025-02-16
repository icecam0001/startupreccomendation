from utils import total_compute, load_data, calculate_combined_item, create_item_dict, precompute_similarities
from heapq import nlargest
import math

class ItemSimilarityRecommender:
   project_dict, user_dict, tag_dict = load_data()
   item_dict = create_item_dict(user_dict)
   #precompute 100 most used items similarity dictionaries to make it easier and faster doing this with sparse usecases makes memory 
   #an issue thus I only did the top 100
   projects_sorted = precompute_similarities(project_dict, item_dict, 100) 

   def recommend(self, user_id, n=5):
       recommend_dict = {}
       for other_item in project_dict:
           total_score = 0
           if other_item in projects_sorted:
               for curr_item in user_dict[user_id]:
                   if other_item == curr_item:
                       total_score = 0
                       break
                   total_score += projects_sorted[other_item][curr_item]
               recommend_dict[other_item] = total_score
           else:
               for curr_item in user_dict[user_id]:
                   if other_item == curr_item:
                       total_score = 0
                       break
                   else:
                       total_score += calculate_combined_item(curr_item, other_item, item_dict, project_dict, 0.7, 0.3)
               recommend_dict[other_item] = total_score

       top_n_items = nlargest(n, recommend_dict.items(), key=lambda x: x[1])
       return [item[0] for item in top_n_items]
            






