from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from template_helpers import Page
from staticpages.models import StaticPageForm
from staticpages.models import StaticPage
from blog.models import Blog
from blog.models import BlogPost
from blog.forms import BlogForm
from blog.forms import BlogPostForm

from django.template import RequestContext
def index(request):
    page = Page()
    page.title = ""
    page.choices = [
        ('Flat Pages',reverse('admin_flatPageMain')),
        ('Blogs',reverse('admin_blogMain')),
        ]
    return render_to_response('menu.html',{'page':page})

def _addurls(item,editHandler,deleteHandler):
    item.editUrl,item.deleteUrl = reverse(editHandler,kwargs={'id':item.id}),reverse(deleteHandler,kwargs={'id':item.id})
    return item

def _makeAttrSetter(attr):
    def f(x,val):
        x.__dict__[attr] = val
        return x
    return f

def blogMain(request):
    page = Page()
    page.title = "blog management"
    page.choices = [
        ('Main admin menu',reverse('admin_index')),
        ]

    setBlogLink = _makeAttrSetter('selectUrl')
    setBlogDeleteLink = _makeAttrSetter('deleteUrl')
        
    staticPage_set = map(
        lambda x:setBlogLink(
            setBlogDeleteLink(x,reverse('admin_blogDelete',kwargs={'id':x.id})),
            reverse('admin_blog',kwargs={'id':x.id})),
        Blog.objects.only('id','name').all())
    
    return render_to_response('admin/blog_main.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('admin_blogCreate'),
                               })

def blog(request,id):
    page = Page()
    page.title = "blog management"
    page.choices = [
        ('Main blog menu',reverse('admin_blogMain')),
        ]
    blog = Blog.objects.get(pk=id)

    setEditLink = _makeAttrSetter('editUrl')
    setDeleteLink = _makeAttrSetter('deleteUrl')

    blogPost_set = map(
        lambda x:setEditLink(
            setDeleteLink(x,reverse('admin_blogPostDelete',kwargs={'id':x.id})),
            reverse('admin_blogPostEdit',kwargs={'id':x.id})),
        blog.blogpost_set.all())
    
    return render_to_response('admin/blog_main.html',
                              {'page':page,
                               'item_set':blogPost_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('admin_blogPostCreate', kwargs={'blog_id':id}),
                               })



##############
# Blog Post  #
##############

def blogPostCreate(request,blog_id):
    page = Page()
    page.title = "Create new blog post"
    page.choices = [
        ('Blog menu',reverse('admin_blog',kwargs={'id':blog_id})),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = BlogPostForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #print form.cleaned_data['slug']
            form.save()
            return HttpResponseRedirect(reverse('admin_blogPostMain')) # Redirect after POST
    else:
        form = BlogPostForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('admin_blogPostCreate',kwargs={'blog_id':blog_id}),
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

#########
# Blog  #
#########

def blogCreate(request):
    page = Page()
    page.title = "Create new blog"
    page.choices = [
        ('Blog menu',reverse('admin_blogMain')),
        ]
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            print form.cleaned_data['slug']
            
            form.save()
            return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST
    else:
        form = BlogForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('admin_blogCreate'),
        'page': page},context_instance=RequestContext(request))

def blogEdit(request,id):
    page = Page()
    page.title = "Edit blog"
    page.choices = [
        ('Blog menu',reverse('admin_blogMain')),
        ]
    blog = get_object_or_404(Blog,pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST,instance=blog)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST
    else:
        form = BlogForm(instance=blog) 

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('blogEdit',kwargs={'id':id}),
        'page': page},context_instance=RequestContext(request))

def blogDelete(request,id):
    blog = get_object_or_404(Blog,pk=id)
    blog.delete()
    return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST



def flatPageMain(request):
    page = Page()
    page.title = "Static page management"
    page.choices = [
        ('Main admin menu',reverse('admin_index')),
        ]

    staticPage_set = map(lambda x:_addurls(x,'staticPageEdit','staticPageDelete'),StaticPage.objects.all())

    return render_to_response('admin/item_list.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('staticPageCreate'),
                               })


def staticPageMain(request):
    page = Page()
    page.title = "Static page management"
    page.choices = [
        ('Main admin menu',reverse('admin_index')),
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


