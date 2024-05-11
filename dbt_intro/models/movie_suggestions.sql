{{ config(
    materialized='view',
    database='movies',
    schema='target',
) }}

select distinct recommendations.user_id,
                recommendations.item_id as movie_id,
                movie.title,
                movie.vote_count,
                recommendations.ESTIMATE
from movies.target.movie_recommendations as recommendations
         inner join {{ ref("movies_filtered_data") }} as  movie
             on recommendations.item_id = movie.id