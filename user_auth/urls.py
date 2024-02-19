from django.urls import path
from .views import user_login, user_signup, user_logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='user_logout'),
    path('signup', user_signup, name='user_signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)