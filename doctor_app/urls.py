from django.urls import path,include
from .views import RegisterView, LoginView,LogoutView,AppointmentAPIView,AllDocsView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('alldocs/',AllDocsView.as_view(),name='registerd'),

    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('appointment/',AppointmentAPIView.as_view(),name='appointment'),
   # path('appoint/',appview.as_view())


]