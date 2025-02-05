import csv
import math
from utils import load_data, calculate_similarity_binary

class ItemItemRecommender:
    
    def recommend(self, project_id, number_of_recs=10):
        project_dict, user_interaction_dict, user_tag_dict = load_data()
        similarity_matrix = {}
        
        for other_project_id in project_dict:
            if other_project_id != project_id:
                # Compute similarity between projects based on users who interacted with both
                users_of_project = set(user for user, projects in user_interaction_dict.items() if project_id in projects)
                users_of_other_project = set(user for user, projects in user_interaction_dict.items() if other_project_id in projects)
                
                common_users = users_of_project.intersection(users_of_other_project)
                
                similarity_score = calculate_similarity_binary(
                    [1 for _ in users_of_project], 
                    [1 for _ in users_of_other_project if _ in common_users]
                )
                
                similarity_matrix[other_project_id] = similarity_score
        
        sorted_projects = sorted(similarity_matrix.items(), key=lambda x: x[1], reverse=True)
        
        return [project for project, _ in sorted_projects[:number_of_recs]]




