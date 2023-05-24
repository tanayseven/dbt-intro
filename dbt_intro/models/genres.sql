{{ config(
    materialized='table',
) }}

select distinct
    value:name as name,
    value:id as id
from
    {{ source('movies', 'movie_metadata_raw') }},
    lateral flatten(parse_json(genres), recursive => false) as value
order by id
