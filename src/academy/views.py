from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "academy/home.html")


def admissions(request):
    return render(request, "academy/admissions.html")


def alumni(request):
    return render(request, "academy/alumni.html")


def journey(request):
    return render(request, "academy/journey.html")


def academic_resources(request):
    return render(request, "academy/academic-resources.html")


def career(request):
    return render(request, "academy/career.html")


def contact_us(request):
    return render(request, "academy/contact.html")


def contribute(request):
    return render(request, "academy/contribute.html")


def about_us(request):
    return render(request, "academy/about.html")
