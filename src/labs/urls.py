from django.urls import path
from labs import views as labs_views


urlpatterns = [path("", labs_views.home, name="labs_home")]
