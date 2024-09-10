import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from .forms import SignUpForm
# Create your views here.
@csrf_exempt
def sign_in(request):
    return render(request, "sign_in.html")

User = get_user_model()
@csrf_exempt
def auth_receiver(request):
    token = request.POST.get('credential')
    if not token:
        return HttpResponse("No token provided", status=400)

    try:
        user_data = id_token.verify_oauth2_token(token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID'])
    except ValueError:
        return HttpResponse("Invalid token", status=403)

    email = user_data.get('email')
    if not email:
        return HttpResponse("Email not found in token", status=400)

    user = None
    form = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        form_data = {
            'username': email,
            'email': email,
            'first_name': user_data.get('given_name'),
            'last_name': user_data.get('family_name'),
        }
        form = SignUpForm(form_data)
        if form.is_valid():
            user = form.save()
        else:
            return HttpResponse(f"Error creating user: {form.errors}", status=400)
    except User.MultipleObjectsReturned:
        user = User.objects.filter(email=email).first() 

    request.session['user_data'] = {
        "email": user.email,
        "given_name": user.first_name,
        "family_name": user.last_name,
        "picture": user_data.get("picture"),
    }

    login(request, user)
    return render(request,"loggedin.html")

@csrf_exempt
def logout(request):
    del request.session['user_data']
    return redirect('sign_in')