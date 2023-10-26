from . import views
from django.db import router
from django.urls import path
from rest_framework_nested import routers
# from django.contrib.auth.views import LogoutView

from .views import (
    LoginView,
    LogoutView,
)



urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]

urlpatterns =  urlpatterns
# router = routers.DefaultRouter()
# router.register("register/teacher", views.RegisterTeacherView,basename="teacher"),
# # router.register("event_management_users", views.EventManagementUsersView)
# # router.register('eventteamlistsubcatagory',views.EventManagementSubcategoryViewSet,basename='MyModel')


# urlpatterns = router.urls + urlpatterns
