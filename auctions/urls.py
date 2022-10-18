from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category, name="category"),



]
