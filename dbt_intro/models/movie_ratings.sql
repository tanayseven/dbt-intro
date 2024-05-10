{{ config(
    materialized='table',
    database='movies',
    schema='target',
) }}

With movie_avg_rating as (
    select movie_id, avg(rating) as rating, count(1) as no_of_reviewers
    from {{ source('movies', 'ratings_raw') }}
                                      group by movie_id
)
select distinct movie.*,movie_rating.rating,movie_rating.no_of_reviewers
from {{ ref('movies_by_genre') }}  as movie
    inner join
  movie_avg_rating as movie_rating
on movie.movie_id = movie_rating.movie_id