from django.shortcuts import render
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView
from accounts.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
# Create your views here.

User = get_user_model()


def home_page(request):
    return render(request, 'accounts/index.html', {})
@csrf_exempt
def login_user(request, template_name=None, extra_context=None):
    if request.method == 'POST':
        print(request.POST.get('username'),"sssssss")
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user=User.objects.filter(email=email)
        
        user = authenticate(username=email, password=password)
        
        print(user,"ss")

        if user:
            if user.is_superuser:
                
                login(request, user)
                return redirect('admin:index')
            if user.status == 0:
                login(request, user)
                messages.error(request, 'login successfull')
                return redirect('accounts:home_page')
            

            else:
                messages.error(request, 'Email or password not correct')
                return redirect('accounts:login')
          
            
        else:
            messages.error(request, 'Email or password not correct')
            return redirect('accounts:login')
    else:
        

        return render(request, 'accounts/login.html', {})


def register(request):
    if request.method == 'POST':
            
        
       
            # if not request.POST.get('email', None) :
            #     messages.error(request, 'Registration failed! Please enter details.')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # if User.objects.filter(email=request.POST.get('email', None)):
            #     messages.error(request, 'User already exist with this email id.')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

       

            user = User.objects.create(
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                password=request.POST.get('password'),
                date_of_birth=request.POST.get('date_of_birth'),
                class_name=request.POST.get('class_name')
            )
            

            user.set_password(user.password)
            user.save()
            messages.info(request, 'Signed Up Successfully')
            return redirect('accounts:login')
    else:
        class_names=class_name.objects.all()
        print(class_names)

        
   
        return render(request, 'accounts/signup.html', {"class_names":class_names})

@login_required(login_url='/user/login')
def profile(request):
    if request.method=="POST":

        user=User.objects.get(id=request.user.id)  
        if user.is_superuser:
            return redirect('admin:index')
        try:  
                  
            
                try:
                    user=User.objects.get(id=request.user.id)                       
                    if request.POST.get('first_name'):
                        user.first_name=request.POST.get('first_name')
                    if request.POST.get('last_name'):
                        user.last_name=request.POST.get('last_name')
                    if request.POST.get('email'):
                        user.email  =request.POST.get('email')            
                    if request.POST.get('date_of_birth'):
                        user.date_of_birth=date_of_birth 
                    if request.POST.get('class_name'):
                        user.class_name=class_name 
                    user.save()              
                except:               
                    user=User.objects.create(first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),                                    
                                        email=request.POST.get('email'),
                                        date_of_birth=request.POST.get('date_of_birth'),
                                        class_name=request.POST.get('class_name'),
                                        
                                        )                                                      
                
                    
               
                messages.success(request, 'Profile Edited successfully')
                return redirect(request.META.get("HTTP_REFERER"))
            
        except Exception as e:
            print(e)
            messages.warning(request, "Unable To Save Profile Update.")
            return redirect(request.META.get("HTTP_REFERER")) 


    else:
            class_names=class_name.objects.all()
            
       
            user=User.objects.all()
            
            return render(request, "accounts/profile.html",
                            {"class_names":class_names})



def logout(request):
    if request.user.is_superuser:
        auth.logout(request)
        return redirect('accounts:signup') 
        
    else:

        try:
            auth.logout(request)
            return redirect('accounts:login')
        except Exception:
            return render(request, settings.EXCEPTION_TEMPLATE)