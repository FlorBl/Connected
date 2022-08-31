from django.conf import settings
from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.welcome, name="welcome1"),
    path("welcome", views.index, name="index"),
    path("afterLogout", views.afterLogout, name="afterLogout"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("post-message", views.postmessage, name="postmessage"),
    path("like/<int:id>", views.like, name="like"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("editpost/<int:id>", views.editpost, name="editpost"),
    path("notifications", views.notifications, name="notifications"),
    path("updateInfo", views.updateInfo, name="updateInfo"),
    path("jsonresponse/<str:username>", views.jsonresponse, name="jsonresponse"),
    path("jsonresponse2/<str:username>", views.jsonresponse2, name="jsonresponse2"),
    path("allUsers", views.allUsers, name="allUsers"),
    path("mobile", views.mobile, name="mobile")
    
    
]

