from django.contrib import admin

from .models import Book ,Genres,Comments,Rating_star_system,Users_stars


admin.site.register(Book)
admin.site.register(Genres)
admin.site.register(Comments)
admin.site.register(Rating_star_system)
admin.site.register(Users_stars)


