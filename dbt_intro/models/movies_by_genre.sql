{{ config(
    materialized='table',
    database='movies',
    schema='target',
) }}

select distinct
    id as movie_id,
    original_title as movie_name,
    value:name::varchar as genre_detail,
    value:id as genre_id
from
    {{ source('movies', 'movie_metadata_raw') }},
    lateral flatten(parse_json(genres), recursive => false) as value
order by genre_id
