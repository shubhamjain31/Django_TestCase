from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import generic

from .models import Question

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.ListView):
    model = Question
    template_name = 'results.html'

def vote(request, question_id):
    choice = request.POST.get('choice')

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=choice)
    except:
        return render(request, 'detail.html')
    else:
        selected_choice.vote += 1
        selected_choice.save()
    return redirect(reverse('polls:results', args=(question_id,)))