from django.http import Http404
from django.http import HttpResponse

from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404

from blog.models import BlogPost
from django.core.urlresolvers import reverse

##################
# CREATE COMMENT #
##################
def createComment(request,id):
    data = request.POST
    email = data.get('email')

    # if email is exist make it lowercase
    if email:
        email = email.lower()

    blogPost = get_object_or_404(BlogPost,id=id)

    comment = models.Comment()
    comment.name = data.get('name')
    comment.email = email
    comment.website = data.get('website')
    comment.blogpost = blogPost
    comment.value = data.get('value')
    comment.save()

    return HttpResponseRedirect(reverse('blog_post')+'#comment_confirmed')

    
