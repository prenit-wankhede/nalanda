from django.urls import path
from academy import views as academy_views


urlpatterns = [
    path("", academy_views.home, name="academy_home"),
    path("admissions", academy_views.admissions, name="admissions"),
    path("alumni", academy_views.alumni, name="alumni"),
    path("journey", academy_views.journey, name="journey"),
    path(
        "academic-resources",
        academy_views.academic_resources,
        name="academic_resources",
    ),
    path("career", academy_views.career, name="career"),
    path("contact", academy_views.contact_us, name="contact_us"),
    path("contribute", academy_views.contribute, name="contribute"),
    path("about", academy_views.about_us, name="about_us"),
]
