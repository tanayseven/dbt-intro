from surprise.prediction_algorithms.knns import KNNBasic
from pathlib import Path

import pandas as pd
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise import accuracy

from recommendation_system.common import get_recommendations

movies_db_path = Path.home() / 'Downloads' / 'movies_dataset'

ratings = pd.read_csv(str(movies_db_path / "ratings_small.csv"))

movie_md = pd.read_csv(str(movies_db_path / "movies_metadata.csv"))

print(ratings.head())

movie_md = movie_md[movie_md['vote_count'] > 55][['id', 'title']]

# IDs of movies with count more than 55
movie_ids = [int(x) for x in movie_md['id'].values]

# Select ratings of movies with more than 55 counts
ratings = ratings[ratings['movieId'].isin(movie_ids)]

# Reset Index
ratings.reset_index(inplace=True, drop=True)

# Print first 5 rows
print()
print()
print(ratings.head())

# Print shape
print()
print()
print(f"Shape: {ratings.shape}")

# Initialize a surprise reader object
reader = Reader(line_format='user item rating', sep=',', rating_scale=(0, 5), skip_lines=1)

# Load the data
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader=reader)

# Build trainset object(perform this only when you are using whole dataset to train)
trainset = data.build_full_trainset()
#Declaring the similarity options.
sim_options = {'name': 'cosine',
               'user_based': True}

# KNN algorithm is used to find similar items
sim_user = KNNBasic(sim_options=sim_options, verbose=False, random_state=33)

# Train the algorithm on the trainset, and predict ratings for the testset
sim_user.fit(trainset)

print()
print()
print()
print(sim_user.predict(uid=2,iid=17,r_ui=5.0))

print()
print()
print()
print(sim_user.predict(uid=671,iid=4011,r_ui=4.0))

print()
print()
print()
print(get_recommendations(ratings, movie_md, 671,10,sim_user))

