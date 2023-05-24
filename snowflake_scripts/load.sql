create or replace file format movie_file_load_format
    skip_header = 1
    type = 'CSV'
    field_optionally_enclosed_by = '"';

create or replace stage credits_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/credits.csv';
copy into credits_raw
    from @credits_stage;

create or replace stage keywords_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/keywords.csv';
copy into keywords_raw
    from @keywords_stage;

create or replace stage links_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/links.csv';
copy into links_raw
    from @links_stage;

create or replace stage movie_metadata_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/movies_metadata.csv';
copy into movie_metadata_raw
    from @movie_metadata_stage
    ON_ERROR=CONTINUE; -- there were some errors in the file so had to do this

create or replace stage ratings_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/ratings.csv';
copy into ratings_raw
    from @ratings_stage;
