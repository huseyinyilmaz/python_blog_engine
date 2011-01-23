from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.db import IntegrityError
from django.utils import simplejson
from django.http import HttpResponse
from django.http import Http404
from staticpages.models import StaticPageForm
from staticpages.models import StaticPage
from blog.models import Blog
from blog.models import BlogPost
from blog.models import Tag
from blog.models import Category

from blog.forms import BlogForm
from blog.forms import BlogPostForm

from django.template import RequestContext
def index(request):
    page = {
        'title' : "",
        'choices' : [
            ('Flat Pages',reverse('admin_flatPageMain')),
            ('Blogs',reverse('admin_blogMain')),
        ]}
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
    page = {
        'title' : "blog management",
        'choices' : [
            ('Main admin menu',reverse('admin_index')),
            ]
        }
    
    setBlogLink = _makeAttrSetter('selectUrl')
    setBlogDeleteLink = _makeAttrSetter('deleteUrl')
        
    staticPage_set = map(
        lambda x:setBlogLink(
            setBlogDeleteLink(x,reverse('admin_blogDelete',kwargs={'id':x.id})),
            reverse('admin_blog',kwargs={'id':x.id})),
        Blog.objects.only('id','name').all().order_by('name'))
    
    return render_to_response('admin/blog_main.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('admin_blogCreate'),
                               })

def blog(request,id):
    blog = Blog.objects.get(pk=id)
    page = {
        'blog' : blog,
        'title' : "Blog options for '%s'"%blog.name,
        'choices' : [
            ('Main blog menu',reverse('admin_blogMain')),
            ('Edit blog',reverse('admin_blogEdit',kwargs={'id':id})),
            ]
        }

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
@commit_on_success
def blogPostCreate(request,blog_id):
    
    post = dict()
    page = {
        'title': "Create new blog post",
        'post': post,
        'blog_url':reverse('admin_blogPostCreate',kwargs={'blog_id':blog_id}),
        'next_url': reverse('admin_blog',kwargs={'id':blog_id}),
        'tag_url': reverse('admin_tag',kwargs={'blog_id':blog_id}),
        }

    if request.method == 'POST': # If the form has been submitted...

        response = {'result':'ok'}
        blogPost = simplejson.loads(request.POST.keys()[0])

        new_post = BlogPost(content=blogPost['content'],
                            teaser=blogPost['teaser'],
                            title=blogPost['title'],
                            slug=blogPost['slug'],
                            blog_id=blog_id,)
        try:
            new_post.save()
        except IntegrityError as e:
            response['result'] = 'error'
            response['slug_error'] = 'There is another post with slug value "%s"'%blogPost['slug']
            response['error'] = e.args[0]
            response['errorTitle'] = "Integrity Error"
        return HttpResponse(simplejson.dumps(response),mimetype='text/html')

    else:
        post.update({'title':"",
                     'slug' :"",
                     'published':True,
                     'teaser':"",
                     'content':""})

        def objFactory(source):
            result = dict()
            result['name'] = source.name
            result['selected'] = False
            return result
        
        post['tags'] = map(objFactory,Tag.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))
        post['categories'] = map(objFactory,Category.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))

        page['post_json'] = simplejson.dumps(post)


    return render_to_response('admin/blogpostpage.html',
        {
        'formAction': reverse('admin_blogPostCreate',kwargs={'blog_id':blog_id}),
        'page': page})

@commit_on_success
def blogPostEdit(request,id):
    blogPost = get_object_or_404(BlogPost,pk=id)
    blog_id = blogPost.blog.id
    page = {
        'title' : "Edit blogPost post",
        'choices' : [
            ('Blog menu',reverse('blogPostMain',kwargs={'id':blog_id})),
            ],
        }
    
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

@commit_on_success
def blogPostDelete(request,id):
    blogPost = get_object_or_404(BlogPost,pk=id)
    blogPost.delete()
    return HttpResponseRedirect(reverse('admin_blog',kwargs={'id':id}))#Redirect after process


#########
# Blog  #
#########

def blogCreate(request):
    page = {
        'title' : "Create new blog",
        'choices' : [
            ('Blog menu',reverse('admin_blogMain')),
            ],
        }
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST
    else:
        form = BlogForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('admin_blogCreate'),
        'page': page},context_instance=RequestContext(request))

def blogEdit(request,id):
    page = {
        'title' : "Edit blog",
        'choices' : [
            ('Blog menu',reverse('admin_blogMain')),
            ],
        }
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
        'formAction': reverse('admin_blogEdit',kwargs={'id':id}),
        'page': page},context_instance=RequestContext(request))

def blogDelete(request,id):
    blog = get_object_or_404(Blog,pk=id)
    blog.delete()
    return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST



def flatPageMain(request):
    page = object()
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
    page = object()
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
    page = object()
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
    page = object()
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
    page = object()
    page.title = ""
    page.choices = [
        ('Main Menu',reverse('index')),
        ]
    page.choices += map(lambda x:(x.name,reverse('blogPostMain',kwargs={'id':x.id})),Blog.objects.all())
    return render_to_response('menu.html',{'page':page})

def blogPostMain(request,id):
    page = object()
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


########
# Tags #
########

def tag(request,blog_id,id=None):
    return None
