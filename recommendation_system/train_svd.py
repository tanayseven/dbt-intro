import os
from pathlib import Path

import pandas as pd
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD
import snowflake.connector

from recommendation_system.common import get_recommendations, get_snowflake_vars

movies_db_path = Path.home() / 'Downloads' / 'movies_dataset'


sf_vars = get_snowflake_vars()

ctx = snowflake.connector.connect(
    user=sf_vars['user'],
    password=sf_vars['password'],
    account=sf_vars['account'],
    database=sf_vars['database'],
    schema=sf_vars['schema'],
)
cs = ctx.cursor()

sql = 'select * from intro.intro.ratings_raw;'
cs.execute(sql)
ratings = cs.fetch_pandas_all()

sql = 'select * from intro.intro.movie_metadata_raw;'
cs.execute(sql)
movie_md = cs.fetch_pandas_all()

print(ratings.head())

movie_md = movie_md[int(movie_md['VOTE_COUNT']) > 55][['id', 'title']]

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
print()
print()
print(trainset)

# Initialize model
svd = SVD()

# cross-validate
svd.fit(trainset)

print()
print()
print()
print(get_recommendations(data=ratings, movie_md=movie_md, user_id=1, top_n=10, algo=svd))
