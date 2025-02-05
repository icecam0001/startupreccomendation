from utils import  load_data, calculate_similarity_tags
import datetime
import math
class TrendingReccomender:

    def rank_projects(self, person_id, numbertorank):
        projectinteractiondict,_, usertagdict= load_data()
        projectsimilaritymatrix = {}
        for project in projectinteractiondict:
            similarity = calculate_similarity_tags(project["tags"], usertagdict[person_id])
            projectsimilaritymatrix[project] = similarity
        projectsimilaritymatrix = dict(sorted(projectsimilaritymatrix.items(), key=lambda item: item[1], reverse=True))
        returnmatrix = []
        n=0
        for i in projectsimilaritymatrix:
            if n==numbertorank:
                break
            returnmatrix.append(i)
            n+=1
        return returnmatrix