# Open Source Project Recommendation System

## The Problem
One of the biggest problems in the CS community is the struggle to get experience. The field is saturated, and actual experience from internships is incredibly difficult to acquire - there just aren't enough spots. It creates this frustrating cycle where internships want developers with experience while simultaneously preventing those developers from getting it. 

There's no shortage of open-source projects on GitHub that need contributors, but there's no streamlined platform for posting and discovering these opportunities. I'm hoping this system not only helps developers find projects to contribute to but also encourages more people to build and share cool things together. I'm hoping in a couple months when this project materializes, we might see an increase in the total number of open-source projects instead of the current negative feedback loop where finding projects is as hard as finding contributors.

## How It All Fits Together
The platform uses different recommendation approaches for different parts of the user experience:

### Main Page Recommendations
- **Content-Based Tag Recommender**: Heavily weighted for newer users who do not have the data to compute accurate CF reccomendations. In the beggining users will select tags they are interested which will slowly decay with time, but in the intermediary, the system uses case-based recommendations to help developers find projects matching their skill level.
- **User-User Collaborative Filtering**: The primary recommendation algorithm, using two different similarity calculations:
  - TFIDF-weighted allows for tags who are not used often to have a higher weight when compared to tags applied to every item virtually. (Python vs Distilled Learning). These low frequency items allow for more insight into a users interests and thus are weighted higher. 
  - Standard weighting to ensure even heavily-tagged projects still have weight in recommendations

### Project Page Recommendations
- **Association Rule Mining**: Similar to Amazon's "People who bought this also bought". When viewing a project, it shows related projects based on co-contribution patterns:
```python
probability[i] = (probability[i]/projectprobabiliy) * (1 - math.exp(-probability[i]*lowoccpenalty))
```
- Uses monotonic confidence attenuation to handle rare co-occurrences
- Implemented an exponential penalty factor to balance between common and rare associations

### Learning Path
- **Trending Score Algorithm**: Powers a dedicated page for solo projects that are good for learning. This is key as it helps newcomers learn before diving into more complicated projects without consequences.
```python
ranking[i] = math.log10(post_interactions)/(hours_since_post**gravity)
```
- Focuses specifically on solo projects tagged as learning resources
- Uses time decay to keep content new and applicable
- Helps create a stepping stone from learning to contributing


## Technical Details

### Association Rule Mining
The `AssociationRulesRecommender` looks at co-contribution patterns - essentially, if someone contributed to project A, what are they likely to contribute to next? Some interesting bits:
```python
probability[i] = (probability[i]/projectprobabiliy) * (1 - math.exp(-probability[i]*lowoccpenalty))
```
- Uses monotonic confidence attenuation to handle rare co-occurrences
- Implemented an exponential penalty factor to balance between common and rare associations
- Helps surface projects that tend to share contributors

### User-User Collaborative Filtering 
The `UserSimilarityRecommender` finds similar developers based on their contribution patterns. The cool part is how it combines different similarity signals:
```python
similarity = (project_weight * project_similarity) + (tag_weight * tag_similarity)
```
- Looks at both project overlap and tag preferences
- Uses binary cosine similarity for contribution patterns
- Weights different similarity components to get better matches

### Content-Based Tag Recommender
This one's interesting because it uses TFIDF-weighted tag representations:
```python
user_tag_dict[user_id][project_tag] += 1/(math.log(len(project_dict[project_id]['tag'])))
```
- Tags are weighted by how specific they are
- Accounts for both tag frequency and importance
- Uses cosine similarity between tag profiles

### Trending Score Algorithm
Implemented a Reddit-style ranking that helps surface promising projects:
```python
ranking[i] = math.log10(post_interactions)/(hours_since_post**gravity)
```
- Time decay with configurable gravity
- Logarithmic scaling of interactions
- Particularly useful for finding active projects


### Core Similarity Calculations
The system uses several similarity metrics:

1. Tag-Based TFIDF Similarity:
```python
user_tag_dict[user_id][project_tag] += 1/(math.log(len(project_dict[project_id]['tag'])))
dotproduct = sum(user_tag_profile2[tag] * user_tag_profile1[tag] for tag in common_tags)
similarity_score = dotproduct / (magnitude2 * magnitude1)
```

2. Binary Interaction Similarity:
```python
similarityscore = dotproduct/(magnitude2*magnitude1)
```

3. Combined Similarity with configurable weights:
```python
combined = (project_weight * project_similarity) + (tag_weight * tag_similarity)
```

### Data Structures
Projects and interactions follow this structure:
```python
project = {
    'id': 'proj001',
    'tags': ['web', 'react'],
    'contributor_count': 45,
    'created_timestamp': '2024-01-01-14:30:00'
}

interaction = {
    'user_id': 'user001',
    'project_id': 'proj001',
    'timestamp': '2024-01-01-15:30:00'
}
```

## Usage
Each recommender can be used independently:
```python
# For trending projects
ranker = TrendingReccomender()
trending_projects = ranker.rank_projects(gravity=1.5, top_n=10)

# For project recommendations
recommender = AssociationRulesRecommender()
recommendations = recommender.recommend(project_id, numberofrecs=10)
```

## Technical Implementation Notes
- Built utility functions for data loading and similarity calculations
- Implemented caching for similarity matrices where needed
- Handled edge cases like zero divisions and empty vectors
- Used proper normalization in similarity calculations
- Designed for modularity to test different approaches


The core recommendation engine is working, with each algorithm serving a cool purpose! The focus has been on creating a system that guides developers from learning to contributing while helping project owners find the right contributors.
