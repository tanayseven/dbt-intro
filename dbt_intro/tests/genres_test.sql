{{ config(tags=['unit-test']) }}

{% set options = {"include_missing_columns": true} %}

{% call dbt_unit_testing.test('genres', 'should generate table of distinct genres') %}
  {% call dbt_unit_testing.mock_source('movies', 'movie_metadata_raw') %}
    genres                                                                                                 | uid
    '[{"id": 18, "name": "Drama"}]'                                                                        | 1
    '[{"id": 28, "name": "Action"}, {"id": 35, "name": "Comedy"}, {"id": 878, "name": "Science Fiction"}]' | 2
    '[{"id": 35, "name": "Comedy"}, {"id": 18, "name": "Drama"}]'                                          | 3
    '[{"id": 28, "name": "Action"}, {"id": 80, "name": "Crime"}, {"id": 18, "name": "Drama"}]'             | 4
  {% endcall %}

  {% call dbt_unit_testing.expect() %}
    genre_detail      | genre_id
    'Drama'           | 18
    'Action'          | 28
    'Comedy'          | 35
    'Crime'           | 80
    'Science Fiction' | 878
  {% endcall %}
{% endcall %}
