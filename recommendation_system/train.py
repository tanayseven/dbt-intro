from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm
import snowflake.connector
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD

from recommendation_system.common import get_snowflake_vars


def get_recommendations(data, user_id, top_n, algo):
    recommendations = []
    user_movie_interactions_matrix = data.pivot(index='USER_ID', columns='MOVIE_ID', values='RATING')
    non_interacted_movies = user_movie_interactions_matrix.loc[user_id][
        user_movie_interactions_matrix.loc[user_id].isnull()
    ].index.tolist()
    for item_id in non_interacted_movies:
        est = algo.predict(user_id, item_id).est
        recommendations.append((item_id, user_id, est))
    recommendations.sort(key=lambda x: x[2], reverse=True)
    recommendations = recommendations[:top_n]

    recommendations_dict = {"ITEM_ID": [], "USER_ID": [], "ESTIMATE": []}
    for recommendation in recommendations:
        recommendations_dict["ITEM_ID"].append(recommendation[0])
        recommendations_dict["USER_ID"].append(recommendation[1])
        recommendations_dict["ESTIMATE"].append(recommendation[2])
    df = pd.DataFrame(recommendations_dict)
    # df = df.reset_index(drop=True, inplace=True)
    # print(df)
    return df


sf_vars = get_snowflake_vars()
ctx = snowflake.connector.connect(
    user=sf_vars['user'],
    password=sf_vars['password'],
    account=sf_vars['account'],
    database=sf_vars['database'],
    schema=sf_vars['schema'],
)

cs = ctx.cursor()
sql = 'select * from movies.landing.ratings_raw;'
cs.execute(sql)
ratings = cs.fetch_pandas_all()
cs.close()

cs = ctx.cursor()
sql = 'select * from movies.target.movies_filtered_data;'
cs.execute(sql)
movie_md = cs.fetch_pandas_all()
print("Loaded all the data")

movie_md = movie_md[movie_md['VOTE_COUNT'] > 55][['ID', 'TITLE']]
movie_ids = [int(x) for x in movie_md['ID'].values]
ratings = ratings[ratings['MOVIE_ID'].isin(movie_ids)]
ratings.reset_index(inplace=True, drop=True)
reader = Reader(line_format='user item rating', sep=',', rating_scale=(0, 5), skip_lines=1)
data = Dataset.load_from_df(ratings[['USER_ID', 'MOVIE_ID', 'RATING']], reader=reader)
print('Training model')
trainset = data.build_full_trainset()
svd = SVD()
svd.fit(trainset)
print('Predicting results')
users = ratings['USER_ID'].unique()[:20]
recommendations_df = pd.DataFrame({"ITEM_ID": [], "USER_ID": [], "ESTIMATE": []})
recommendations_df.reset_index(drop=True, inplace=True)
for user in tqdm(users):
    new_recommendations_df = get_recommendations(data=ratings, user_id=654, top_n=10, algo=svd)
    recommendations_df = pd.concat([recommendations_df, new_recommendations_df], ignore_index=True)

print("Saving to DB...")
engine = create_engine(URL(
    user=sf_vars['user'],
    password=sf_vars['password'],
    account=sf_vars['account'],
    database=sf_vars['database'],
    schema=sf_vars['schema'],
))
connection = engine.connect()
recommendations_df.to_sql('movie_recommendations', schema='target', con=engine, index=False)
connection.close()
engine.dispose()
