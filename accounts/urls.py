from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns =[
    path("", views.UserDetailsView.as_view(), name='user-detail'),
    path("locations/", views.LocationListView.as_view()),
]