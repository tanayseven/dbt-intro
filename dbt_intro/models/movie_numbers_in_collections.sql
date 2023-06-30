{{ config(
    materialized='view',
    database='movies',
    schema='target',
) }}

select
    movies_by_collection.collection_name,
    count(movies_by_collection.uid) as total_movies
from
    {{ ref('movies_by_collection') }} as movies_by_collection
where collection_name is not null
group by collection_name
order by total_movies desc
