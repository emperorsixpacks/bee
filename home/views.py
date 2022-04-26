from .models import Contact
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AboutUsPage


def index(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
        if name and email and message:
            Contact.objects.create(name=name, message=message, email=email)
            messages.success(request, 'Message successfully received, check your email')
            return redirect('home')
    template = 'index.html'
    return render(request, template)


def about_us(request):
    about = 3#AboutUsPage.objects.get(id=1)
    about_us_section = about.about_us_section
    trust = about.why_you_can_trust_us_section
    mission = about.our_mission_section
    context = {
        'about': about_us_section,
        'trust': trust,
        'mission': mission,
    }
    template = 'about.html'
    return render(request, template, context)
