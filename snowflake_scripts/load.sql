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
copy into movie_metadata_raw (
        uid,
        adult,
        belongs_to_collection,
        budget,
        genres,
        homepage,
        id,
        imdb_id,
        original_language,
        original_title,
        overview,
        popularity,
        poster_path,
        production_companies,
        production_countries,
        release_date,
        revenue,
        runtime,
        spoken_languages,
        status,
        tagline,
        title,
        video,
        vote_average,
        vote_count
    )
    from (
        select
            metadata$file_row_number as uid,
            mms.$1 as adult,
            mms.$2 as belongs_to_collection,
            mms.$3 as budget,
            mms.$4 as genres,
            mms.$5 as homepage,
            mms.$6 as id,
            mms.$7 as imdb_id,
            mms.$8 as original_language,
            mms.$9 as original_title,
            mms.$10 as overview,
            mms.$11 as popularity,
            mms.$12 as poster_path,
            mms.$13 as production_companies,
            mms.$14 as production_countries,
            mms.$15 as release_date,
            mms.$16 as revenue,
            mms.$17 as runtime,
            mms.$18 as spoken_languages,
            mms.$19 as status,
            mms.$20 as tagline,
            mms.$21 as title,
            mms.$22 as video,
            mms.$23 as vote_average,
            mms.$24 as vote_count
        from @movie_metadata_stage as mms
    )
    ON_ERROR=CONTINUE; -- there were some errors in the file so had to do this

create or replace stage ratings_stage
    file_format = movie_file_load_format
    url = 's3://tanayseven-dbt-intro/ratings.csv';
copy into ratings_raw
    from @ratings_stage;
