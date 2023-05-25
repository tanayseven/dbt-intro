{{ config(
    materialized='table',
) }}

select
    movies_metadata.original_title as original_title,
    movies_metadata.uid as movie_uid,
    language.code as language_code,
    language.language_english as language_name
from
    {{ source('movies', 'movie_metadata_raw') }} as movies_metadata
    join {{ ref('language') }}
    on movies_metadata.original_language = language.code
