from utils import total_compute, load_data, calculate_combined_item, createitemdict, precomputesimilarities
from heapq import nlargest
import math
class ItemSimilarityRecommender:

    projectdict, userdict, tagdict = load_data()
    itemdict = createitemdict(userdict)
    #precompute 100 most used items similarity dictionaries to make it easier and faster doing this with sparse usecases makes memory 
    #an issue thus I only did the top 100
    projectssorted = precomputesimilarities(projectdict, itemdict, 100) 
    def recommend(self, user_id, n=5):
        reccomenddict = {}

        for otheritem in projectdict:
            sum=0

            if otheritem in projectssorted:
                for item in userdict[user_id]:
                    if otheritem ==item:
                        sum=0
                        break
                    sum+=projectssorted[otheritem][item]
                reccomenddict[otheritem] = sum
            else:
                for item in userdict[user_id]:
                    if otheritem ==item:
                        sum=0
                        break
                    else:
                        sum+=calculate_combined_item(item, otheritem, itemdict, projectdict, 0.7, 0.3)
                reccomenddict[otheritem] = sum
        sortedbytopdict = dict(sorted(reccomenddict.items(), key=lambda x: x[1], reverse=True))
        reccomenderarray=[]
        k=0
        for i in sortedbytopdict:
            reccomenderarray.append(i)
            k+=1
            if k>=n:
                break
        return reccomenderarray
            






