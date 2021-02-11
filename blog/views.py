from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Article
import json


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return redirect('user_account')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    return render(request,'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_account')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user:
            auth.login(request,user)
            return redirect('user_account')
        else:
            messages.info(request,'Username and/or password is incorrect')
            return redirect('/')
    else:
        return redirect('/')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('user_account')
    else:
        return render(request,'register.html')

def create_user_view(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('register')
            elif pass1.isalnum() and len(pass1) >= 8:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                messages.info(request,"You have been registered. Please login.")
                return redirect('/')
            else:    
                messages.info(request,"Password doesn\'t match the requirements.")
                return redirect('register')
        else:
            messages.info(request,'Passwords don\'t match.')
            return redirect('register')    
    else:
        return render(request,'register.html')

def user_account_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        data = Article.objects.filter(author_id=user_id)
        return render(request,'user_profile.html',{'data':data})
    else:
        return redirect('/')    

def user_profile_view(request):
    if request.user.is_authenticated:
       username = request.GET['userSearch']
       user_id = User.objects.filter(username=username).values_list('id')
       if username == request.user.username:
           return redirect('user_account')
       if user_id:
           articles = Article.objects.filter(author_id=user_id[0])
           count = articles.filter(mode=1).count()
           context={
           'user_name': username,
           'count': count,
           'articles' :articles
           }
           return render(request,'profile_view.html',context) 
       else:
           messages.info(request,"No such user")
           return render(request,'profile_view.html')
       
    

def logout_view(request):
    auth.logout(request)
    return redirect('/')        

def add_new_blog_view(request):
    #print(request.FILES)
    if request.method == 'POST' and request.FILES['image']:
        user= request.user
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image'] 
        if request.POST.get('mode')=="on":
            mode = 0
        else:
            mode = 1    

        save_record = Article.objects.create(author= user,title=title,description=description,image=image,mode=mode)
        save_record.save()
        #messages.info(request,'New blog has been created')
    return redirect('user_account')    


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = User.objects.filter(username__icontains=q)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.username)
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)   