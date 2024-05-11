{{ config(
    materialized='view',
    database='movies',
    schema='target',
) }}

select distinct rating.user_id,
                language.original_title,
                language.LANGUAGE_NAME,
                rating.RATING
from {{ source('movies', 'ratings_raw') }} rating
         inner join
    {{ ref('movies_by_language') }} language
         on rating.MOVIE_ID = language.MOVIE_UID