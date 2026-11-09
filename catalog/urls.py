from django.urls import path

from . import api, views


app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("editions/<int:pk>/", views.edition_detail, name="edition"),
    path("categories/<int:pk>/", views.category_detail, name="category"),
    path("polls/<int:pk>/", views.poll_detail, name="poll"),
    path("polls/<int:pk>/vote/", views.vote, name="vote"),
    path("my-votes/", views.my_votes, name="my-votes"),
    path("api/categorias/", api.categories, name="api-categories"),
]
