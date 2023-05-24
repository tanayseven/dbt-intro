import uuid

from sqlalchemy import Column, text, PrimaryKeyConstraint
from snowflake.sqlalchemy import NUMBER, TEXT, DEC
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Credits(Base):
    __tablename__ = "credits_raw"

    cast = Column(TEXT)
    crew = Column(TEXT)
    id = Column(NUMBER, nullable=False, primary_key=True, autoincrement=False)


class Keywords(Base):
    __tablename__ = "keywords_raw"

    id = Column(NUMBER, nullable=False, primary_key=True, autoincrement=False)
    keywords = Column(TEXT)


class Links(Base):
    __tablename__ = "links_raw"

    movie_id = Column(NUMBER, nullable=False, primary_key=True, autoincrement=False)
    imdb_id = Column(TEXT)
    tmdb_id = Column(TEXT)


class MovieMetadata(Base):
    __tablename__ = "movie_metadata_raw"

    uid = Column(NUMBER, nullable=False, primary_key=True, autoincrement=False)
    adult = Column(TEXT)
    belongs_to_collection = Column(TEXT)
    budget = Column(TEXT)
    genres = Column(TEXT)
    homepage = Column(TEXT)
    id = Column(NUMBER)
    imdb_id = Column(TEXT)
    original_language = Column(TEXT)
    original_title = Column(TEXT)
    overview = Column(TEXT)
    popularity = Column(TEXT)
    poster_path = Column(TEXT)
    production_companies = Column(TEXT)
    production_countries = Column(TEXT)
    release_date = Column(TEXT)
    revenue = Column(TEXT)
    runtime = Column(TEXT)
    spoken_languages = Column(TEXT)
    status = Column(TEXT)
    tagline = Column(TEXT)
    title = Column(TEXT)
    video = Column(TEXT)
    vote_average = Column(TEXT)
    vote_count = Column(TEXT)


class Ratings(Base):
    __tablename__ = "ratings_raw"

    user_id = Column(NUMBER)
    movie_id = Column(NUMBER)
    rating = Column(DEC)
    timestamp = Column(NUMBER)
    __table_args__ = (
        PrimaryKeyConstraint(
            user_id, movie_id
        ),
    )
