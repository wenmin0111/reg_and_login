from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    # print(User._meta.db_table)### when create a raw query and not sure what the table name is , you can always find it by printing this line.
    # User.objects.all()[0].delete()
    users = User.objects.all()
    context = {
        'users': users
    }

    return render(request, 'login_and_reg_app/index.html', context)

def create(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

    postData = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'confirm': confirm,
    }

    model_resp = User.objects.reg_fn_validation(postData)
    if model_resp[0] == True:
        # print "User successfully created, should add flash message!"
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        # print "SESSION: ", request.session['name']
        return redirect('/success')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    model_resp = User.objects.login_check(postData)
    if User.objects.login_check(postData) == True:
        return redirect('/success')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')

def success(request):
    print 'LOGIN successfully'
    context = {
        'users': User.objects.all()
    }
    return render(request, 'login_and_reg_app/success.html', context)
