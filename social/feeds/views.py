from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib import messages

from .models import Post, Post_like
from .forms import PostForm
from .utils import create_slug
from user.models import Users
from comment.models import Comment, Replay
#from django.contrib.contenttypes.models import ContentType


def list_post(request):
    #return HttpResponse("<h1> list </h1>")
    #print(request.user)
    #print(request.user.is_authenticated())
    if not request.user.is_authenticated():
        return redirect("home")
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
   
    #queryset = Post.objects.all()
    join_date = request.user.date_joined
    queryset = Post.objects.filter(timestamp__gte=join_date)
    
    '''for i in queryset:
        print(i.get_absolute_url())'''
    
    
    #r = Post_like()
    #print(r)
    #print(r.post.id)

   
    # search function starts
    from django.db.models import Q
    query = request.GET.get('q')
    if query:
        queryset = Post.objects.filter(Q(content__icontains=query))
        print(queryset)
                                    # | Q(content__icontains=query)).distinct()
                                    # end search functions'''

   
   
    paginator = Paginator(queryset,10) # Show 10 posts per page
    page_request = 'page'
    page = request.GET.get(page_request)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        pages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (eg 9999), deliver last page of results
        pages = paginator.page(paginator.num_pages) 
    temp = Post_like.objects.filter(user=request.user)
    #print(temp)
    like = []
    for l in temp:
        #print(l.__class__)
        t1 = Post.objects.get(pk=l)
        like.append(t1.slug)
    #print(like)
    #print(Users.objects.get(user=request.user))
    profile = Users.objects.get(user=request.user)
    #print(profile)
    #status = profile.status
    context = {  
        #'objects':queryset,
        'objects':pages,
        "title":"list ",
        "like":like,
        #"status":status,
        "page_request":page_request,
        "profile":profile,
        "home":"active",
        }
    return render(request, "list.html", context)


   
def create_post(request):
    if not request.user.is_authenticated():
        return redirect("home")
    #return HttpResponse("<h1> create </h1>")
    #form = PostForm()
    '''if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        print(title, content)
        Post.objects.create(title=title, content=content)'''
    '''if not request.user.is_staff or not request.user.is_superuser:
        raise Http404'''
    #if not request.user.is_authenticated():
        #raise Http404
    #form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        content = request.POST.get("post")
        image = request.FILES.get("image")
        slug = create_slug()
        #print(image)
        #filename, extension = image.split(".")
        #name = create_shortcode(instance)
        #print(title, content)
        Post.objects.create(user=request.user, slug=slug, content=content, image=image).save()
        #post = Post.objects.create(user=request.user, content=content,)
        #name = create_shortcode(post)
        #post.shortcode = name
        #post.image="%s.%s"%(name, extension)
        #post.save()
        #instance = form.save(commit=False)
        #print(form.cleaned_data.get("title"))
        #instance.save()
        #return HttpResponseRedirect(instance.get_absolute_url())
        return redirect("list")

    #context = {"form":form}
    return render(request, "profile.html",)


def detail_post(request, id=None):
    if not request.user.is_authenticated():
        return redirect("home")
    #return HttpResponse("<h1> detail </h1>")
    post_detail = get_object_or_404(Post, pk=id)
    post_like = get_object_or_404(Post_like, user=request.user, post=post_detail)
    #print(post_detail, post_like)
    #content_type = ContentType.objects.get_for_model(Post)
    #obj_id = post_detail.id
    comments = Comment.objects.filter( post=post_detail)
    context = {
        'object':post_detail,
        'comments':comments,
        "likes":post_detail.likes,
        "liked":"True",
        }
    return render(request, "detail.html", context)

def update_post(request, id=None):
    if not request.user.is_authenticated():
        return redirect("home")
    #return HttpResponse("<h1> update </h1>")
    post_detail = get_object_or_404(Post, pk=id)
    if request.user == post_detail.user:
        form = PostForm(request.POST or None, request.FILES or None, instance=post_detail)
        if form.is_valid():
            #content = request.POST.get("content")
            #Post.objects.get(user=request.user, content=content).save()
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "<a href=#>Successfully Updated</a>")
            #return HttpResponseRedirect(instance.get_absolute_url())
            return redirect("detail", post_detail.pk)
        else:
            #messages.error(request, "Not Updated")
            context = {
                'object':post_detail,
                'form':form,
                'title':"Edit Post",
                }
        return render(request, "update.html", context)
    return redirect("detail", post_detail.pk)


def delete_post(request, id=None):
    if not request.user.is_authenticated():
        return redirect("home")
    post_detail = get_object_or_404(Post, pk=id)
    if request.user == post_detail.user:
        post_detail.delete()
        messages.success(request, "Successfully Deleted")
    return redirect("list")


def likes(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    new_like, created = Post_like.objects.get_or_create(user=request.user, post=post_detail)
    #print(new_like)
    if not created: 
        new_like.delete()
        Post_like.objects.count_likes(post_detail, -1)
    else:
        #new_like = Post_like.objects.create(user=request.user, post=post_detail, like="L")
        new_like.like = "L"
        new_like.save()
        Post_like.objects.count_likes(post_detail, 1)
        
    print(request)
    return redirect("list")


def chats(request):
    if not request.user.is_authenticated():
        return redirect("home")
    return render(request, "chat.html")