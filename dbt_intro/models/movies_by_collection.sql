{{ config(
    materialized='table',
    database='intro',
    schema='target',
) }}

select
    try_parse_json(belongs_to_collection):name::varchar as collection_name,
    try_parse_json(belongs_to_collection):id::number as collection_id,
    original_title as movie_name,
    uid
from
    {{ source('movies', 'movie_metadata_raw') }}
where belongs_to_collection is not null
order by collection_id
