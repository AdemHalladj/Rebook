from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView)
from .views import register , search , reservebook , addbook , addReview , addPicture

urlpatterns = [
    path("login/" , TokenObtainPairView.as_view() , name = 'token_obtain_pair'),
    path("register/" , register , name = 'register'),
    path("search/" , search , name = 'search'),
    path("reservebook/" , reservebook , name = 'reservebook'),
    path("addbook/" , addbook , name = 'addbook'),
    path("addReview/" , addReview , name = 'addReview'),
    path("addPicture/" , addPicture , name = 'addPicture'),
    path("refresh/" , TokenRefreshView.as_view() , name = 'token_refresh'),

]