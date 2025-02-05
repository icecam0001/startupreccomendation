# association_rules_recommender.py
from utils import total_compute, load_data
import math
class AssociationRulesRecommender:
    """
    Recommends projects based on co-contribution patterns
    
    TODO:
    1. For each project pair (i,j), calculate:
       - Count users who contributed to both
       - Count users who contributed to j
       - Score = P(i|j) = (both_count / j_count)
    2. For a given project, find others with highest association scores
    
    Hints:
    - Store scores in a dictionary {(proj1, proj2): score}
    - Consider minimum support (ignore very rare co-occurrences)
    - Remember to handle divide-by-zero cases
    """
    #figure out how to improt these functinos from these files

    def recommend(self, project_id, numberofrecs=10, lowoccpenalty=0.5):
        _, userinteractiondict = load_data()
        totals = {}
        probability = {}
        
        for i in userinteractiondict:
            if project_id in userinteractiondict[i]:
                for x in userinteractiondict[i]:
                    totals[x] = totals.get(x, 0) + 1
                    if x != project_id:
                        probability[x] = probability.get(x, 0) + 1
            else:
                for x in userinteractiondict[i]:
                    totals[x] = totals.get(x, 0) + 1

        projectprobabiliy = totals.get(project_id, 0)
        
        for i in probability:
            try:
                probability[i] = (probability[i]/projectprobabiliy) * (1 - math.exp(-probability[i]*lowoccpenalty))
            except ZeroDivisionError:
                print("Error dividing by zero reinput a different occurance value")
            except Exception as e:
                print(f"Unexpected error: {e}")
        
        probability = dict(sorted(probability.items(), key=lambda item: item[1], reverse=True))
        return list(probability.keys())[:numberofrecs]
