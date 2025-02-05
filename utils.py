import csv
import math
x=0

def load_data():
    global x
    project_dict = {}
    with open('projects.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            project_id = row.pop('project_id')
            project_dict[project_id] = row

    user_interaction_dict = {}
    user_tag_dict = {}  
    with open('interactions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            project_id = row['project_id']
            user_id = row['user_id']
            if user_id in user_interaction_dict:
                user_interaction_dict[user_id].append(project_id)
            else:
                user_interaction_dict[user_id] = [project_id]
                user_tag_dict[user_id] = {}  
    

    for user_id in user_interaction_dict:
        for project_id in user_interaction_dict[user_id]:
            x+=1
            project_tag = project_dict[project_id]['tag']  
            if project_tag in user_tag_dict[user_id]:
                user_tag_dict[user_id][project_tag] += 1/(math.log(len(project_dict[project_id]['tag'])))
            else:
                user_tag_dict[user_id][project_tag] = 1/(math.log(len(project_dict[project_id]['tag'])))
    
    
    return project_dict, user_interaction_dict, user_tag_dict 
def total_compute():
        return x   
def calculate_similarity_binary(vec1, vec2):
    dotproduct = 0

    for g in vec1:
        if g in vec2:
            dotproduct+=1
    magnitude1 = math.sqrt(len(vec1))  
    magnitude2 = math.sqrt(len(vec2))  

    if magnitude1 * magnitude2 == 0:
        return 0

    similarityscore = dotproduct/(magnitude2*magnitude1)

    return similarityscore
#runTFIDF
def calculate_similarity_tags(user_tag_profile1, user_tag_profile2):
    dotproduct = 0
    for tag in user_tag_profile1:
        if tag in user_tag_profile2:
            dotproduct += user_tag_profile2[tag] * user_tag_profile1[tag]
    
    magnitude1 = math.sqrt(sum(value**2 for value in user_tag_profile1.values()))
    magnitude2 = math.sqrt(sum(value**2 for value in user_tag_profile2.values()))
    
    if magnitude1 * magnitude2 == 0:
        return 0
        
    similarity_score = dotproduct / (magnitude2 * magnitude1)
    return similarity_score

def calculate_combined_similarity(user1, user2, user_interaction_dict, user_tag_dict, project_weight=0.5, tag_weight=0.5):
    project_similarity = calculate_similarity_binary(
        user_interaction_dict[user1],
        user_interaction_dict[user2]
    )
    
    tag_similarity = calculate_similarity_tags(
        user_tag_dict[user1],
        user_tag_dict[user2]
    )
    
    return (project_weight * project_similarity) + (tag_weight * tag_similarity)