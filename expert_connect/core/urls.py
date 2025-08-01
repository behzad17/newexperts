from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("profile/create/", views.create_profile, name="create_profile"),
    path("profiles/", views.profile_list, name="profile_list"),
    path("experts/", views.experts_list, name="experts_list"),
    path("podcasts/", views.podcasts_list, name="podcasts_list"),
    path("profile/<int:user_id>/", views.profile_detail, name="profile_detail"),
    path("profile/<int:user_id>/like/", views.like_toggle, name="like_toggle"),
    path("profile/<int:user_id>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("profile/<int:user_id>/comment/", views.add_comment, name="add_comment"),
    path("messages/", views.inbox, name="inbox"),
    path("messages/send/<int:user_id>/", views.send_message, name="send_message"),
    path("messages/<int:user_id>/", views.conversation_detail, name="conversation_detail"),
]
