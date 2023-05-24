{{ config(tags=['unit-test']) }}

{% set options = {"include_missing_columns": true} %}

{% call dbt_unit_testing.test('movies_in_dbs', 'should generate movies_in_dbs with correct links') %}
  {% call dbt_unit_testing.mock_source('movies', 'movie_metadata_raw') %}
    original_title      | uid
    'Toy Story'         | 1
    'Jumanji'           | 2
    'Grumpier Old Men'  | 3
    'Waiting to Exhale' | 4
  {% endcall %}

  {% call dbt_unit_testing.mock_source('movies', 'links_raw') %}
    imdb_id   | tmdb_id | movie_id
    '0114709' | 862     | 1
    '0113497' | 8844    | 2
    '0113228' | 15602   | 3
    '0114885' | 31357   | 4
  {% endcall %}

  {% call dbt_unit_testing.expect() %}
    original_title      | uid | imdb_link                               | tmdb_link
    'Toy Story'         | 1   | 'https://www.imdb.com/title/tt0114709'  | 'https://www.themoviedb.org/movie/862'
    'Jumanji'           | 2   | 'https://www.imdb.com/title/tt0113497'  | 'https://www.themoviedb.org/movie/8844'
    'Grumpier Old Men'  | 3   | 'https://www.imdb.com/title/tt0113228'  | 'https://www.themoviedb.org/movie/15602'
    'Waiting to Exhale' | 4   | 'https://www.imdb.com/title/tt0114885'  | 'https://www.themoviedb.org/movie/31357'
  {% endcall %}
{% endcall %}
