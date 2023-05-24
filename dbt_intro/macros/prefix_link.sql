{% macro prefix_link(type) %}
    {% if type == 'imdb' %}
        'https://www.imdb.com/title/tt'
    {% elif type == 'tmdb' %}
        'https://www.themoviedb.org/movie/'
    {% else %}
        ''
    {% endif %}
{% endmacro %}
