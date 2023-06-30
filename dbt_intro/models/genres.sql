{{ config(
    materialized='table',
    schema='target',
) }}

select distinct
    value:name::varchar as genre_detail,
    value:id as genre_id
from
    {{ source('movies', 'movie_metadata_raw') }},
    lateral flatten(parse_json(genres), recursive => false) as value
order by genre_id
