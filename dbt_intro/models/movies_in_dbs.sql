{{ config(
    materialized='table',
) }}

select distinct
    uid,
    original_title,
    {{ prefix_link('imdb') }} || links.imdb_id as imdb_link,
    {{ prefix_link('tmdb') }} || links.tmdb_id as tmdb_link
from
    {{ source('movies', 'movie_metadata_raw') }} as movies_metadata
    inner join {{ source('movies', 'links_raw') }} as links
    on movies_metadata.uid = links.movie_id
order by uid