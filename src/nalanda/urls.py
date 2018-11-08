from django.urls import path
from nalanda import views as nalanda_views


urlpatterns = [path("", nalanda_views.home, name="nalanda_home")]
