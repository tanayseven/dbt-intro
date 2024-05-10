{{ config(
    materialized='table',
    database='movies',
    schema='target',
) }}

select
    *
from (
  select *,
         ROW_NUMBER() over (partition by id order by id) AS row_num
  from {{ source('movies', 'movie_metadata_raw') }}
) as subquery
where row_num = 1
