from django.urls import path
from auths import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = "auths"

urlpatterns =[
    path("signup", views.SignUp.as_view(), name='signup'),
    path("jwt-login", views.JWTLogin.as_view(), name='jwt-login'),
    # path("logout", views.Logout.as_view()),
]
