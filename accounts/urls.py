from django.urls import path
from .views import RegisterView, LoginView, EnterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('enter/', EnterView.as_view(), name='enter'),
]
