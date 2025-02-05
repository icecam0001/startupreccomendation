from utils import total_compute, load_data
import datetime
import math
class TrendingReccomender:

    def rank_projects(self, gravity=1.5, top_n=10):
        projectinteractiondict, _ = load_data()
        ranking = {}
        for i in projectinteractiondict:
            if projectinteractiondict[i]["solo"] ==True:
                post_timestamp = datetime.datetime.strptime(projectinteractiondict[i]["created_timestamp"], '%Y-%m-%d %H:%M:%S')
                hours_since_post = (datetime.datetime.now() - post_timestamp).total_seconds() / 3600
                post_interactions = projectinteractiondict[i]["contributor_count"]
                ranking[i] = math.log10(post_interactions)/(hours_since_post**gravity)
        ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
        n=0
        returnmatrix=[]
        for j in ranking:
            if n==top_n:
                break
            returnmatrix.append(j)
            n+=1
        return returnmatrix