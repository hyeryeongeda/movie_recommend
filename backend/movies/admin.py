# movies/admin.py
from django.contrib import admin
from .models import Movie, Genre, Person, Rating, Review, WatchList, MovieCast, MovieGenre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_year', 'country')
    search_fields = ('title',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(WatchList)
admin.site.register(MovieCast)
admin.site.register(MovieGenre)
