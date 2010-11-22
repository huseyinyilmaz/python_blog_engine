from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from mysite.polls.models import Choice, Poll

def main(request):
    None
    # p = get_object_or_404(Poll, pk=poll_id)
    # try:
    #     selected_choice = p.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the poll voting form.
    #     return render_to_response('polls/poll_detail.html', {
    #         'object': p,
    #         'error_message': "You didn't select a choice.",
    #         })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     #print 'huseyin deneme : %s'%reverse('mysite.polls.views.results', args=(p.id,))
    #     return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))


