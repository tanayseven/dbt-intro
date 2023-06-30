import pickle
from pathlib import Path

import pandas as pd
import snowflake.connector
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD

from recommendation_system.common import get_recommendations, get_snowflake_vars, get_recommendations_without_movie

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
print("Loading ratings...")
if not (Path.cwd() / "ratings.pickle").exists():
    sql = 'select * from intro.intro.ratings_raw;'
    cs.execute(sql)
    ratings = cs.fetch_pandas_all()
    pd.to_pickle(ratings, "./ratings.pickle")
else:
    ratings = pd.read_pickle("./ratings.pickle")

print("Loading movies...")
if not (Path.cwd() / "movies_md.pickle").exists():
    sql = 'select * from intro.intro_target.movies_filtered_data;'
    cs.execute(sql)
    movie_md = cs.fetch_pandas_all()
    pd.to_pickle(movie_md, "./movie_md.pickle")
else:
    movie_md = pd.read_pickle("./movie_md.pickle")

# TODO move this to DBT
movie_md = movie_md[movie_md['VOTE_COUNT'] > 55][['ID', 'TITLE']]

# Initialize a surprise reader object
reader = Reader(line_format='user item rating', sep=',', rating_scale=(0, 5), skip_lines=1)

# Load the data
data = Dataset.load_from_df(ratings[['USER_ID', 'MOVIE_ID', 'RATING']], reader=reader)
# print("Data set to train the model on")
# print(data.df.head())

# Build trainset object(perform this only when you are using whole dataset to train)
print("Building trainset...")
trainset_pickle = Path.cwd() / "trainset.pickle"
if not trainset_pickle.exists():
    trainset = data.build_full_trainset()
    with open(trainset_pickle, 'wb') as f:
        pickle.dump(trainset, f)
else:
    with open(str(trainset_pickle), "rb") as f:
        trainset = pickle.load(f)

# Initialize model
svd_pickle = Path.cwd() / "svd.pickle"
if not svd_pickle.exists():
    svd = SVD()
    svd.fit(trainset)
    with open(svd_pickle, 'wb') as f:
        pickle.dump(svd, f)
else:
    with open(str(trainset_pickle), "rb") as f:
        svd = pickle.load(f)

print("Predicting...")
print(svd.predict(uid=3, iid=2959, r_ui=5.0))

print("Pulling recommendations...")
# recommendations = get_recommendations_without_movie(data=ratings, user_id=654, top_n=10, algo=svd)
recommendations = get_recommendations(data=ratings, user_id=654, top_n=10, algo=svd, movie_md=movie_md)
print(recommendations)
