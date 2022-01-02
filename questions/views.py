from django.shortcuts import render, get_object_or_404

from .forms import QuestionForm
from .models import Question


# Create your views here.
def question_update_view(request, number):
    obj = get_object_or_404(Question, id=number)
    form = QuestionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "question/question_update.html", context)
