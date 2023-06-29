{{ config(
    materialized='table',
) }}

select distinct
    value:name::varchar || '|' || value:id as genre_detail,
    'another-value' as another_value
from
    {{ source('movies', 'movie_metadata_raw') }},
    lateral flatten(parse_json(genres), recursive => false) as value
order by genre_id
