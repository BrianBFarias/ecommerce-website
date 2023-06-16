from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:item_id>/product", views.product, name="product"),
    path("login", views.login_view, name="login"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>/remove", views.remove, name="remove"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:item_id>/close", views.close, name="close"),
    path("<int:item_id>", views.bid, name="bid"),
    path("<int:item_id>/watchlist", views.add_watchlist, name="add_watchlist"),
    path("category", views.category, name="category"),
    path("<slug:category>/category", views.chosen_category, name="chosen_category"),
    path("<int:item_id>/comment", views.comment, name="comment")

]
