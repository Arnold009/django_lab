import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import * 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate
# Create your views here.

def test(request):
    return HttpResponse("hello ")

def testPage(request):
    return render(request , "test.html")

def index(request):  ## render the home page not base
    return render(request , "index.html")

def LoginPage(request): ## render the login page
    return render(request , "login.html")

def signupPage(request): ## render the signup page
    return render(request , "signup.html")

def verify_emailPage(request): ## render the forgot pwd page to verify email
    return render(request, "verify_email.html")    

def signup(request):   ## validate the form and create a user record
    if request.method == "POST":  #validate the form method
        ##fetch the inputs
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        cPassword = request.POST.get('cpassword', '').strip()
        
        ###### Validate the inputs
        if not firstname or not lastname:    
            messages.warning(request , "Enter valid names !! Please check it .... ")
            return redirect("signuppage")       
        if not email:
            messages.warning(request , "Email should not be empty !! ")
            return redirect("signuppage")       
        if not phone and len(phone) != 10:
            messages.warning(request , "Phone number should be of 10 digits only !! ")
            return redirect("signuppage")       
        if not password or not cPassword:
            messages.warning(request, "Password and Confirm Password are requestuired.")
            return redirect("signuppage")
        if len(password)<6 or len(cPassword)<6:
            messages.warning(request, "Password and Confirm Password must requestuire min. 6 digits.")
            return redirect("signuppage")
        if password != cPassword:
                messages.warning(request, "Password and Confirm Password should be same.")
                return redirect("signuppage")       
        
        ### check the whether the email is already in use or not 
        user_exists = User.objects.filter(email=email).exists()
        print(user_exists)
        if user_exists:
            messages.error(request , " Email is already taken !! try with another !! ")
            return redirect("signuppage")
        else: 
            ### create the user
            new_user = User.objects.create(
                firstname = firstname,
                lastname = lastname,
                email = email,
                phone = phone,
                password = make_password(password) # encrypted pwd
            )
            print(new_user)
            if new_user :
                messages.success(request , " Signup successfull !! ")
                return redirect("loginpage")
            else: 
                messages.error(request, "Error in creating new user !! try again ")
                return redirect("signuppage")
    else:
        messages.error(request , " Bad requestuest method !! ")
        return redirect("signuppage")       


