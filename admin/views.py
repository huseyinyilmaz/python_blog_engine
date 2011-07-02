from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.db import IntegrityError
from django.utils import simplejson
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from staticpage.forms import StaticPageForm
from staticpage.models import StaticPage
from blog.models import Blog
from blog.models import BlogPost
from blog.models import Tag
from blog.models import Category
from django.template.defaultfilters import slugify
from blog.forms import BlogForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

MAIN_DESCRIPTION = "<p>Welcome to admin utility for Python Blog Engine. With This utility, you can Create/Editblogs and blogposts. Blogs will be available in '/blog/blog_slug/' url.(replace blog_slug value with slug of your blog).</p><p>Static pages are backed by database. so you can create new static pages simply by adding one from admin menu. They are available in '/sp/staticpage_slug/'</p>"
BLOG_MAIN_DESCRIPTION = "<ul><li>Press create button to create a new blog</li><li>Select a blog and press delete button to delete it.</li><li>Select a blog and press select button to goto blog menu. You can edit blog or do blog post operations from blog menu.</li></ul>"
BLOG_DESCRIPTION = "<ul><li>Press edit blog button to edit current blog</li><li>Press create button to create a new blog post</li><li>Select a blog post and press delete button to delete it</li><li>Select a blog post and pres edit button to edit it</li></ul>"
STATIC_PAGES_DESCRIPTION = "<ul><li>Press create button to create a new static page</li><li>Select a static page and press delete button to delete it</li><li>Select a static page and pres edit button to edit it</li></ul>"
@login_required
def index(request):
    page = {
        'title' : "",
        'choices' : [
            ('Static Pages',reverse('admin_staticPageMain')),
            ('Blogs',reverse('admin_blogMain')),
            ],
        'description':MAIN_DESCRIPTION,
        }
    return render_to_response('list.html',{'page':page,'user':request.user},)

def _addurls(item,editHandler,deleteHandler):
    item.editUrl,item.deleteUrl = reverse(editHandler,kwargs={'id':item.id}),reverse(deleteHandler,kwargs={'id':item.id})
    return item

def _makeAttrSetter(attr):
    def f(x,val):
        x.__dict__[attr] = val
        return x
    return f

#########
# Blog  #
#########
@login_required
def blogMain(request):
    page = {
        'title' : "blog management",
        'choices' : [
            ('Main admin menu',reverse('admin_index')),
            ],
        'description':BLOG_MAIN_DESCRIPTION,
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
                               'user':request.user,
                               })

@login_required
def blog(request,id):
    blog = Blog.objects.get(pk=id)
    page = {
        'blog' : blog,
        'title' : "Blog options for '%s'"%blog.name,
        'choices' : [
            ('Main blog menu',reverse('admin_blogMain')),
            ('Edit blog',reverse('admin_blogEdit',kwargs={'id':id})),
            ],
        'description':BLOG_DESCRIPTION,
        }

    setEditLink = _makeAttrSetter('selectUrl')
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
                               'user':request.user,
                               })


@login_required
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

@login_required
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

@login_required
def blogDelete(request,id):
    blog = get_object_or_404(Blog,pk=id)
    blog.delete()
    return HttpResponseRedirect(reverse('admin_blogMain')) # Redirect after POST



##############
# Blog Post  #
##############

@login_required
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
                               'user':request.user,
                               })


@login_required
@commit_on_success
def blogPostCreate(request,blog_id):
    post = dict()
    page = {
        'title': "Create new blog post",
        'post': post,
        'blog_url':reverse('admin_blogPostCreate',kwargs={'blog_id':blog_id}),
        'next_url': reverse('admin_blog',kwargs={'id':blog_id}),
        'tag_url': reverse('admin_tag',kwargs={'blog_id':blog_id}),
        'category_url': reverse('admin_category',kwargs={'blog_id':blog_id}),
        }

    if request.method == 'POST': # If the form has been submitted...
        
        response = {'result':'ok'}
        blogPost = simplejson.loads(request.raw_post_data )
        tags = Tag.objects.filter(blog__id=blog_id,id__in = map(lambda x: x['id'],blogPost['tags']))
        categories = Category.objects.filter(blog__id=blog_id,id__in = map(lambda x: x['id'],blogPost['categories']))

        new_post = BlogPost(content=blogPost['content'],
                            teaser=blogPost['teaser'],
                            title=blogPost['title'],
                            slug=blogPost['slug'],
                            published=blogPost['published'],
                            comments_closed=blogPost['comments_closed'],
                            max_comment_count=blogPost['max_comment_count'],
                            blog_id=blog_id,
                            )
        try:
            # we need to save the object in order to add manytomany field
            new_post.save()
        except IntegrityError as e:
            response['result'] = 'error'
            response['slug_error'] = 'There is another post with slug value "%s"'%blogPost['slug']
            response['error'] = e.args[0]
            response['errorTitle'] = "Integrity Error"
        new_post.tags.add(*tags)
        new_post.categories.add(*categories)
        try:
            #this one saves many to many relationship
            new_post.save()
        except IntegrityError as e:
            response['result'] = 'error'
            response['slug_error'] = 'Error while adding tags to post'
            response['error'] = e.args[0]
            response['errorTitle'] = "Integrity Error"
        return HttpResponse(simplejson.dumps(response),mimetype='text/html')
    #get request: render page first time
    post.update({'title':"",
                 'slug' :"",
                 'published':True,
                 'teaser':"",
                 'content':"",
                 'comments_closed':False,
                 'max_comment_count':100})

    def objFactory(source):
        result = dict()
        result['name'] = source.name
        result['selected'] = False
        result['id'] = source.id
        return result
        
    post['tags'] = map(objFactory,Tag.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))
    post['categories'] = map(objFactory,Category.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))

    page['post_json'] = simplejson.dumps(post)

    return render_to_response('admin/blogpostpage.html',
        {
        'formAction': reverse('admin_blogPostCreate',kwargs={'blog_id':blog_id}),
        'page': page,
        'user':request.user,
})

@login_required
@commit_on_success
def blogPostEdit(request,id):
    post = dict()
    postObj = get_object_or_404(BlogPost,id = id)
    post['id']= postObj.id
    post['title']= postObj.title
    post['slug']= postObj.slug
    post['teaser']= postObj.teaser
    post['content']= postObj.content
    post['published']= postObj.published
    post['comments_closed']=postObj.comments_closed
    post['max_comment_count']=postObj.max_comment_count
    blog_id = postObj.blog_id
    page = {
        'title': "Edit blog post",
        'post': post,
        'blog_url':reverse('admin_blogPostEdit',kwargs={'id':id}),
        'next_url': reverse('admin_blog',kwargs={'id':blog_id}),
        'tag_url': reverse('admin_tag',kwargs={'blog_id':blog_id}),
        'category_url': reverse('admin_category',kwargs={'blog_id':blog_id}),
        }

    if request.method == 'PUT': # If the form has been submitted...

        response = {'result':'ok'}
        blogPost = simplejson.loads(request.raw_post_data)

        updated_tag_ids = set( map(lambda x: x['id'],blogPost['tags']) )
        org_tag_list = zip(*postObj.tags.values_list('id').all())
        org_tag_ids = set(org_tag_list[0]) if org_tag_list else set()
        new_tag_ids = updated_tag_ids - org_tag_ids
        old_tag_ids = org_tag_ids - updated_tag_ids
                            
        new_tags = Tag.objects.filter(blog__id=blog_id,id__in = new_tag_ids) if new_tag_ids else []
        old_tags = Tag.objects.filter(blog__id=blog_id,id__in = old_tag_ids) if old_tag_ids else []


        updated_category_ids = set( map(lambda x: x['id'],blogPost['categories']) )
        org_category_list = zip(*postObj.categories.values_list('id').all())
        org_category_ids = set(org_category_list[0]) if org_category_list else set()
        new_category_ids = updated_category_ids - org_category_ids
        old_category_ids = org_category_ids - updated_category_ids
                            
        new_categories = Category.objects.filter(blog__id=blog_id,id__in = new_category_ids) if new_category_ids else []
        old_categories = Category.objects.filter(blog__id=blog_id,id__in = old_category_ids) if old_category_ids else []

        

        postObj.content = blogPost['content']
        postObj.teaser = blogPost['teaser']
        postObj.title = blogPost['title']
        postObj.slug = blogPost['slug']
        postObj.published = blogPost['published']
        postObj.comments_closed = blogPost['comments_closed']
        postObj.max_comment_count = blogPost['max_comment_count']

        try:
            # we need to save the object in order to add manytomany field
           postObj.validate_unique()
        except ValidationError as e:
            response['result'] = 'error'
            response['slug_error'] = 'There is another post with slug value "%s"'%blogPost['slug']
            response['error'] = e.args[0]
            response['errorTitle'] = "Integrity Error"

        if new_tags:
            postObj.tags.add(*new_tags)
        if old_tags:
            postObj.tags.remove(*old_tags)
        if new_categories:
            postObj.categories.add(*new_categories)
        if old_categories:
            postObj.categories.remove(*old_categories) 

        try:
            postObj.save()
        except IntegrityError as e:
            response['result'] = 'error'
            response['slug_error'] = 'Error while adding tags to post'
            response['error'] = e.args[0]
            response['errorTitle'] = "Integrity Error"
        return HttpResponse(simplejson.dumps(response),mimetype='text/html')

    #get request: render page first time
    # get tuple of tag and category ids
    zipped_tags = zip(*postObj.tags.values_list('id').all())
    tag_ids = zipped_tags[0] if zipped_tags else []
    zipped_categories = zip(*postObj.categories.values_list('id').all())
    category_ids = zipped_categories[0] if zipped_categories else []

    def objFactoryCreator(id_list):
        def objFactory(source):
            result = dict()
            result['name'] = source.name
            result['selected'] = (source.id in id_list)
            result['id'] = source.id
            return result
        return objFactory
        
    post['tags'] = map(objFactoryCreator(tag_ids),Tag.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))
    post['categories'] = map(objFactoryCreator(category_ids),Category.objects.filter(blog__id=blog_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name'))

    page['post_json'] = simplejson.dumps(post)

    return render_to_response('admin/blogpostpage.html',
        {
        'formAction': reverse('admin_blogPostEdit',kwargs={'id':id}),
        'page': page,
        'user':request.user,
        })

@login_required
@commit_on_success
def blogPostDelete(request,id):
    blogPost = get_object_or_404(BlogPost,pk=id)
    blog_id = blogPost.blog_id
    blogPost.delete()
    return HttpResponseRedirect(reverse('admin_blog',kwargs={'id':blog_id}))#Redirect after process


################
# Static pages #
################

@login_required
def staticPageMain(request):
    page = {
        'title' : "Static page management",
        'choices' : [
            ('Main admin menu',reverse('admin_index')),
            ],
        'description':STATIC_PAGES_DESCRIPTION,
        }

    
    staticPage_set = map(lambda x:_addurls(x,'admin_staticPageEdit','admin_staticPageDelete'),StaticPage.objects.all())

    return render_to_response('admin/item_list.html',
                              {'page':page,
                               'item_set':staticPage_set,
                               'item_display_label':'Name',
                               'createUrl':reverse('admin_staticPageCreate'),
                               'user':request.user,
                               })

@login_required
@commit_on_success
def staticPageCreate(request):
    page = {
        'title' : "Create new static",
        'choices' : [
            ('Static page menu',reverse('admin_staticPageMain')),
            ],
        }
    if request.method == 'POST': # If the form has been submitted...
        form = StaticPageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            return HttpResponseRedirect(reverse('admin_staticPageMain')) # Redirect after POST
    else:
        form = StaticPageForm() # An unbound form

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('admin_staticPageCreate'),
        'page': page,
         },context_instance=RequestContext(request))

@login_required
@commit_on_success
def staticPageEdit(request,id):
    page = {
        'title' : "Edit static page",
        'choices' : [
            ('Static page menu',reverse('admin_staticPageMain')),
            ],
        }
    staticpage = get_object_or_404(StaticPage,pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = StaticPageForm(request.POST,instance=staticpage)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('admin_staticPageMain')) # Redirect after POST
    else:
        form = StaticPageForm(instance=staticpage) 

    return render_to_response('admin/formpage.html',
        {'form': form,
        'formAction': reverse('admin_staticPageEdit',kwargs={'id':id}),
        'page': page,},context_instance=RequestContext(request))

@login_required
@commit_on_success
def staticPageDelete(request,id):
    static = get_object_or_404(StaticPage,pk=id)
    static.delete()
    return HttpResponseRedirect(reverse('admin_staticPageMain')) # Redirect after POST


#######################
# Tags and Categories #
#######################
@login_required
@commit_on_success
def widget(request, item_class, blogpost_connection, blog_id, id):
    if request.method == 'POST':
        item = simplejson.loads(request.POST.keys()[0])
        item['name'] = slugify(item['name'])
        item['selected'] = True
        # if ther eis another tag with the same slug value raise an error
        if item_class.objects.filter(name=item['name']).exists():
            return HttpResponseServerError('Duplicated Name')
        if not item['name']:
            return HttpResponseServerError('Name cannot be empty')
        new_item = item_class()
        new_item.blog_id = blog_id
        new_item.name = item['name']
        new_item.save()
        item['id'] = new_item.id
        return HttpResponse(simplejson.dumps(item),mimetype='text/html')
    elif request.method == 'DELETE':
        item = get_object_or_404(item_class,id=id)
        item_json = {'id': item.id,'name': item.name,'selected': False}
        item.delete()
        return HttpResponse(simplejson.dumps(item_json),mimetype='text/html')
    elif request.method == 'PUT':
        item_json  = simplejson.loads(request.raw_post_data)
        item_json['name'] = slugify(item_json['name'])
        item = None
        try:
            item = item_class.objects.get(id=item_json['id'])
        except item_class.DoesNotExist:
            return HttpResponseServerError('Edited item does not exist')
        item.name = item_json['name']
        item.save()
        return HttpResponse(simplejson.dumps(item_json),mimetype='text/html')
    return HttpResponse('',mimetype='text/html')

def tag(request,blog_id,id=None):
    return widget(request,Tag,BlogPost.tags,blog_id,id)

def category(request,blog_id,id=None):
    return widget(request,Category,BlogPost.categories,blog_id,id)

