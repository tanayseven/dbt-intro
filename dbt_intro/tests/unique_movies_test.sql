{{ config(tags=['unit-test']) }}

{% set options = {"include_missing_columns": true} %}

{% call dbt_unit_testing.test('unique_movies', 'should generate table of distinct genres') %}
  {% call dbt_unit_testing.mock_source('movies', 'movie_metadata_raw') %}
    original_title          | id
    'The Terminator'        | 218
    'The Godfather'         | 238
    '2001: A Space Odyssey' | 62
    'The Godfather'         | 238
    'The Terminator'        | 218
    'The Godfather'         | 238
  {% endcall %}

  {% call dbt_unit_testing.expect() %}
    original_title          | id
    'The Terminator'        | 218
    'The Godfather'         | 238
    '2001: A Space Odyssey' | 62
  {% endcall %}
{% endcall %}
