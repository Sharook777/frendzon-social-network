from django.shortcuts import render, redirect, get_object_or_404

from .models import Users
from .forms import LoginForm, RegisterForm
from feeds.models import Post

from django.contrib import auth
from django.contrib.auth.models import User


def home(request):
    form = LoginForm(request.POST or None )
    if not request.user.is_authenticated():
        template = "home.html"
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            #print(username, password)
        
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("list")
    else:
        return redirect("list")
                #raise ValidationError("Invalid username and Password")
    context = {
        "title": "Login",
        "form": form,
        "link":True,
        }
    
    return render(request, template, context )


def register(request):
    from .utils import create_slug
    form = RegisterForm(request.POST or None, request.FILES or None)
    context = {
        "title": "Sign Up",
        "form": form,
        }
    template = "home.html"
    if request.user.is_authenticated():
        return redirect(home)
    if request.method == 'POST':
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        gender = request.POST.get("gender")
        mail_id = request.POST.get("mail_id")
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_no = request.POST.get("phone_no")
        profile_pic = request.FILES.get("profile_pic")
        
        if gender =="1":
            gender = 'M'
        else:
            gender = 'F'
        if form.is_valid():
            user=User.objects.create(
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=mail_id,
                )
            user.set_password(password)
            user.save()
            
            slug = create_slug()
            Users.objects.create(
                user=user,
                firstname=firstname,
                lastname=lastname,
                slug=slug,
                gender=gender,
                mail_id=mail_id,
                username=username,
                password=password,
                phone_no=phone_no,
                profile_pic=profile_pic,
                ).save()
                
            '''welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            feed = Post(user=user, post=welcome_post)
            feed.save()'''
            return redirect(home)
    return render(request, template, context )

def profile(request, member=None):
    if not request.user.is_authenticated():
        return redirect("home")
    
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    #my_post = request.user.date_joined
    user = Users.objects.get(pk=member)
    #queryset = Post.objects.filter(user=request.user)
    queryset = Post.objects.filter(user=user.user)
    #url = user.get_absolute_url()
    paginator = Paginator(queryset,10) # Show 10 posts per page
    page_request = 'page'
    page = request.GET.get(page_request)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages) 
    profile = Users.objects.get(user=request.user)
    #print(user, request.user)
    if user == request.user: 
        context = {  
            'objects':pages,
            "page_request":page_request,
            "profile":user,
            "post":"active",
            "pro":"active",
            #"url":url,
            }
    else:
        context = {  
            'objects':pages,
            "page_request":page_request,
            "profile":user,
            "post":"active",
            "pro":"active",
            }
    return render(request, 'profile.html', context)




from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from user.forms import ChangePasswordForm

@login_required
def password(request):
    user = request.user
    user1 = Users.objects.get(user=user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            user1.password = new_password
            user1.save()
            #messages.add_message(request, messages.SUCCESS,
            #                     'Your password was successfully changed.')
            return redirect('password')

    else:
        form = ChangePasswordForm(instance=user)
    context = {
        'form':form,
        'name':"Change Password",
        'password':"active",
        'profile':user1,
        }

    return render(request, 'form.html', context)


from user.forms import Picture_change_Form, Status_change_form, Edit_Form
def pro_pic(request):
    if not request.user.is_authenticated():
        return redirect("home")
    user = get_object_or_404(Users, username=request.user)
    if request.method == 'POST':
        form = Picture_change_Form(request.FILES or None, instance=user)
        print("picture", form.is_valid())
        if form.is_valid():
            print("picture")
            image = request.FILES.get("profile_pic")
            print(image)
            user.profile_pic = image
            user.save()
            from feeds.utils import create_slug
            content ='Changed Profile picture '
            slug = create_slug()
            Post.objects.create(user=request.user, slug=slug, content=content, image=image).save()
            return redirect('pro_pic')
    else:
        form = Picture_change_Form()
    context = {
        'form':form,
        'name':"Change Profile Picture",
        'picture':"active",
        'profile':user,
        }
    return render(request, 'form.html', context)

def status_change(request):
    if not request.user.is_authenticated():
        return redirect("home")
    user = get_object_or_404(Users, username=request.user)
    if request.method == 'POST':
        form = Status_change_form(request.POST or None, instance=user)
        if form.is_valid():
            status = request.POST.get("status")
            user.status = status
            user.save()
            from feeds.utils import create_slug
            content ='Changed Status: "%s"'%(status)
            slug = create_slug()
            Post.objects.create(user=request.user, slug=slug, content=content).save()
            return redirect('status')
    else:
        form = Status_change_form()
    context = {
        'form':form,
        'name':"Change Status",
        'status':"active",
        'profile':user,
        }
    return render(request, 'form.html', context)

def settings(request):
    if not request.user.is_authenticated():
        return redirect("home")
    
    user = get_object_or_404(Users, user=request.user)
    if request.user == user.user:
        form = Edit_Form(request.POST or None, request.FILES or None, instance=user)
        #profile = Users.objects.get(user=request.user)
        if form.is_valid():
            #content = request.POST.get("content")
            #Post.objects.get(user=request.user, content=content).save()
            instance = form.save(commit=False)
            instance.save()
            #messages.success(request, "<a href=#>Successfully Updated</a>")
            #return HttpResponseRedirect(instance.get_absolute_url())
            return redirect("settings")
        else:
            #messages.error(request, "Not Updated")
            '''context = {
                'object':user,
                'form':form,
                }'''
            context = {
                'form':form,
                'name':"Edit Profile Details",
                'edit':"active",
                'profile':user,
                }
        return render(request, "form.html", context)
    
    context = {
        'form':form,
        'name':"Edit Profile Details",
        'profile':"active",
        }
    return render(request, 'form.html', context)


def gallery(request, member=None):
    if not request.user.is_authenticated():
        return redirect("home")
    #user = get_object_or_404(Users, pk=member)
    user = Users.objects.get(pk=member)
    print("user slug",user.username, request.user)
    #images = Post.objects.get(user=user.username)
    images = Post.objects.all()
    print(images)
    context = {
            "image":images,
            "gallery":"active",
            'profile':user,
            "post":"active",
        }
    return render(request, 'gallery.html',context)


def about(request, member=None):
    if not request.user.is_authenticated():
        return redirect("home")
    #user = get_object_or_404(Users, username=request.user)
    user = get_object_or_404(Users, pk=member)
    #print("  about",user)
    context = {
            "about":"active",
            'profile':user,
            "post":"active",
        }
    return render(request, 'about.html',context)

def profile_del(request):
    if not request.user.is_authenticated():
        return redirect("home")
    profile_detail = get_object_or_404(Users, user=request.user)
    profile = get_object_or_404(User, user=request.user)
    if request.user == profile_detail.user:
        profile_detail.delete()
        profile.delete()
        messages.success(request, "Successfully Deleted")
    return redirect("home")

from bug.models import Bug
from bug.forms import BugForm
def bug(request):
    if not request.user.is_authenticated():
        return redirect("home")
    form = BugForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            message = request.POST.get("message")
            Bug.objects.create(user=request.user,message=message).save()
            return redirect("list")
    context = { 
        'form':form,
        'title':"Report Problem",
        }
    return render(request, 'update.html', context)

def logout(request):
    auth.logout(request)
    return redirect(home)