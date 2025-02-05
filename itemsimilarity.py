class ItemSimilarityRecommender:
    """
    Implements item-item collaborative filtering using binary cosine similarity
    
    TODO:
    1. Represent each project as binary vector (user contributed=1, didn't=0)
    2. Compute cosine similarity between project vectors
    3. For user's projects, find similar ones they haven't contributed to
    4. Aggregate similar projects' scores
    
    Hints:
    - Can pre-compute project similarity matrix
    - Consider minimum number of common contributors
    - May want to normalize by project popularity
    """
    def recommend(self, user_id, n=5):
        pass


