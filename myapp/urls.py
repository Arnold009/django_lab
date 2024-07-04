from django.urls import path
from .views import *

urlpatterns = [
    path("test/", test, name="test"),
    path("testpg/", testPage, name="testpg"),
    path("index/", index, name="index"),
    path("loginpg/", LoginPage, name="loginpage"),
    path("signuppg/", signupPage, name="signuppage"),
    path("verifyemail/", verify_emailPage, name="verify_email"),
    
    
    
    
    path("signup/", signup, name="signup"),
]

