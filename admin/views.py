from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from template_helpers import Page
from staticpages.models import StaticPageForm
from staticpages.models import StaticPage
from blog.models import Blog
from blog.models import BlogPost
from blog.models import BlogForm
from blog.models import BlogPostForm

from django.template import RequestContext
def index(request):
    """
    Main admin page this is mapted to /admin/
    """
    page = Page()
    page.title = ""
    page.choices = [
        ('menuMain',reverse('menuMain')),
        ('Static Pages',reverse('staticPageMain')),
        ('Blogs',reverse('blogMain')),
        ('Blog Posts',reverse('blogListMain')),
        ]
    return render_to_response('menu.html',{'page':page})

def _addurls(item,editHandler,deleteHandler):
    item.editUrl,item.deleteUrl = reverse(editHandler,kwargs={'id':item.id}),reverse(deleteHandler,kwargs={'id':item.id})
    return item

def menuMain(request):
    page = Page()
    page.title += " Administration"
    page.choices = [
        ('Main admin menu',reverse('index')),
        ]
    return render_to_response('menu.html',{'page':page})

def blogMain(request):
    page = Page()
    page.title = "blog management"
    page.choices = [
        ('Main admin menu',reverse('index')),
        ]

    staticPage_set = map(lambda x:_addurls(x,'blogEdit','blogDelete'),Blog.objects.all())

    return render_to_response('admin/item_list.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('blogCreate'),
                               })


def staticPageMain(request):
    page = Page()
    page.title = "Static page management"
    page.choices = [
        ('Main admin menu',reverse('index')),
        ]

    staticPage_set = map(lambda x:_addurls(x,'staticPageEdit','staticPageDelete'),StaticPage.objects.all())

    return render_to_response('admin/item_list.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('staticPageCreate'),
                               })

def staticPageCreate(request):
    page = Page()
    page.title = "Create new static page"
    page.choices = [
        ('Static page menu',reverse('staticPageMain')),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = StaticPageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #print form.cleaned_data['slug']
            form.save()
            return HttpResponseRedirect(reverse('staticPageMain')) # Redirect after POST
    else:
        form = StaticPageForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('staticPageCreate'),
        'page': page},context_instance=RequestContext(request))


def staticPageEdit(request,id):
    page = Page()
    page.title = "Edit static page"
    page.choices = [
        ('Static page menu',reverse('staticPageMain')),
        ]
    staticPage = get_object_or_404(StaticPage,pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = StaticPageForm(request.POST,instance=staticPage)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('staticPageMain')) # Redirect after POST
    else:
        form = StaticPageForm(instance=staticPage) 

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('staticPageEdit',kwargs={'id':id}),
        'page': page},context_instance=RequestContext(request))

def staticPageDelete(request,id):
    staticPage = get_object_or_404(StaticPage,pk=id)
    staticPage.delete()
    return HttpResponseRedirect(reverse('staticPageMain')) # Redirect after POST


def blogCreate(request):
    page = Page()
    page.title = "Create new blog"
    page.choices = [
        ('Blog menu',reverse('blogMain')),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #print form.cleaned_data['slug']
            form.save()
            return HttpResponseRedirect(reverse('blogMain')) # Redirect after POST
    else:
        form = BlogForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('blogCreate'),
        'page': page},context_instance=RequestContext(request))

def blogEdit(request,id):
    page = Page()
    page.title = "Edit blog"
    page.choices = [
        ('Blog menu',reverse('blogMain')),
        ]
    blog = get_object_or_404(Blog,pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST,instance=blog)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('blogMain')) # Redirect after POST
    else:
        form = BlogForm(instance=blog) 

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('blogEdit',kwargs={'id':id}),
        'page': page},context_instance=RequestContext(request))

def blogDelete(request,id):
    blog = get_object_or_404(Blog,pk=id)
    blog.delete()
    return HttpResponseRedirect(reverse('blogMain')) # Redirect after POST

def blogListMain(request):
    """
    Blog list for main blog post page
    """
    page = Page()
    page.title = ""
    page.choices = [
        ('Main Menu',reverse('index')),
        ]
    page.choices += map(lambda x:(x.name,reverse('blogPostMain',kwargs={'id':x.id})),Blog.objects.all())
    return render_to_response('menu.html',{'page':page})

def blogPostMain(request,id):
    page = Page()
    page.title = "Blog Post Management"
    page.choices = [
        ('Main admin menu',reverse('index')),
        ]

    staticPage_set = map(lambda x:_addurls(x,'blogPostEdit','blogPostDelete'),Blog.objects.get(pk=id).blogpost_set.all())

    return render_to_response('admin/item_list.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('blogPostCreate',kwargs={'blog_id':id}),
                               })


def blogPostCreate(request,blog_id):
    page = Page()
    page.title = "Create new blog post"
    page.choices = [
        ('Blog menu',reverse('blogPostMain',kwargs={'id':blog_id})),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = BlogPostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #print form.cleaned_data['slug']
            form.save()
            return HttpResponseRedirect(reverse('blogPostMain')) # Redirect after POST
    else:
        form = BlogPostForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('blogPostCreate',kwargs={'blog_id':blog_id}),
        'page': page},context_instance=RequestContext(request))

def blogPostEdit(request,id):
    blogPost = get_object_or_404(BlogPost,pk=id)
    blog_id = blogPost.blog.id
    page = Page()
    page.title = "Edit blogPost post"
    page.choices = [
        ('Blog menu',reverse('blogPostMain',kwargs={'id':blog_id})),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = BlogPostForm(request.POST,instance=blogPost)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('blogPostMain')) # Redirect after POST
    else:
        form = BlogPostForm(instance=blogPost) 

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('blogPostEdit',kwargs={'id':id,'blog_id':blog_id}),
        'page': page},context_instance=RequestContext(request))

def blogPostDelete(request,id):
    blogPost = get_object_or_404(BlogPost,pk=id)
    blogPost.delete()
    return HttpResponseRedirect(reverse('blogPostMain')) # Redirect after POST
