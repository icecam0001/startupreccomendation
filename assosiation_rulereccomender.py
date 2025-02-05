# association_rules_recommender.py
from utils import total_compute, load_data
import math
class AssociationRulesRecommender:
  

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
