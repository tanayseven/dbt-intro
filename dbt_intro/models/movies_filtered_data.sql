{{ config(
    materialized='table',
    database='movies',
    schema='target',
) }}

select
    title as title,
    id as id,
    vote_count::number as vote_count
from {{ source('movies', 'movie_metadata_raw') }}
