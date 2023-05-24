{{ config(
    materialized='table',
) }}

select distinct
    value:name::varchar as name,
    value:id as genre_id
from
    {{ source('movies', 'movie_metadata_raw') }},
    lateral flatten(parse_json(genres), recursive => false) as value
order by genre_id
