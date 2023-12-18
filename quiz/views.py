from .models import Topic, Quiz, Result, Question
from .forms import QuizForm, ChoiceForm, BaseChoiceFormSet, UserUpdateForm, ProfileUpdateForm, QuizCommentForm, QuestionForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, PageNotAnInteger
from django.views import generic
from django import forms
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import timedelta

def about(request):
    return render(request, 'about.html')

def index(request):
    topics = Topic.objects.all()
    quizzes = Quiz.objects.order_by('?')[:5]
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'topics': topics,
        'num_visits': num_visits,
        'quizzes': quizzes,
    }
    return render(request, 'index.html', context=context)

def quiz_list(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    paginator = Paginator(Quiz.objects.filter(topic=topic), 3)
    page_number = request.GET.get('page')
    quizzes = paginator.get_page(page_number)
    context = {
        'topic': topic,
        'quizzes': quizzes,
    }
    return render(request, 'quiz_list.html', context=context)

def quiz_result(request, result_id):
    result = Result.objects.get(id=result_id)
    context = {
        'result': result,
    }
    return render(request, 'quiz_result.html', context=context)

class QuizListView(generic.ListView):
    model = Quiz
    paginate_by = 3
    template_name = 'quizzes.html'

def quiz_history(request):
    user_results = Result.objects.filter(user=request.user).order_by('-start_time')
    query = request.GET.get('query')
    if query:
        user_results = user_results.filter(quiz__title__icontains=query)
    paginator = Paginator(user_results, 5)
    page_number = request.GET.get('page')
    try:
        results = paginator.page(page_number)
    except PageNotAnInteger:
        results = paginator.page(1)
    context = {
        'user_results': results,
        'paginator': paginator,
    }
    return render(request, 'quiz_history.html', context=context)

class QuizByUserListView(LoginRequiredMixin, generic.ListView):
    model = Quiz
    paginate_by = 5
    template_name = 'quiz_by_user_list.html'

    def get_queryset(self):
        user_quizzes = Quiz.objects.filter(user=self.request.user)
        query = self.request.GET.get('query')
        if query:
            user_quizzes = user_quizzes.filter(title__icontains=query)
        return user_quizzes

class QuizByUserUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Quiz
    template_name = 'update_quiz.html'
    fields = ['topic', 'title', 'description', 'image']
    success_message = "Quiz is updated"

    def get_success_url(self):
        return reverse_lazy('quiz_info', kwargs={'quiz_id': self.object.pk})

class QuizByUserDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Quiz
    template_name = 'quiz_by_user_delete.html'
    success_url = reverse_lazy('quiz_by_user_list')
    success_message = "Quiz is deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
def search(request):
    query = request.GET.get('query')
    search_results = Quiz.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'quizzes': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'The user with the email {email} is already registered!')
                    return redirect('register')
                else:

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')

class QuizInfoView(FormMixin, DetailView):
    model = Quiz
    template_name = 'quiz_info.html'
    form_class = QuizCommentForm
    pk_url_kwarg = 'quiz_id'

    def get_success_url(self):
        return reverse('quiz_info', kwargs={'quiz_id': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.quiz = self.object
        form.instance.user = self.request.user
        form.save()
        return super(QuizInfoView, self).form_valid(form)

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            score = 0
            for question in quiz.question_set.all():
                selected_choice_id = request.POST.get(f'question_{question.id}')
                if question.choice_set.get(id=selected_choice_id).is_correct:
                    score += 1
            result = Result.objects.create(user=request.user if request.user.is_authenticated else None, quiz=quiz,
                                           score=score, start_time=quiz.start_time)
            result.end_time = timezone.now()
            result.time_taken = result.end_time - result.start_time
            result.time_taken = timedelta(seconds=result.time_taken.seconds)
            result.save()
        return redirect('quiz_result', result_id=result.id)
    else:
        quiz.start_time = timezone.now()
        quiz.save()
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'form': form})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES, is_creating_quiz=True)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            return redirect('create_question', quiz_id=quiz.id)
    else:
        form = QuizForm(is_creating_quiz=True)
    return render(request, 'create_quiz.html', {'form': form})

def create_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('create_choice', quiz_id=quiz.id, question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form, 'quiz': quiz})

def create_choice(request, quiz_id, question_id):
    quiz = Quiz.objects.get(id=quiz_id)
    question = Question.objects.get(id=question_id)
    ChoiceFormSet = forms.formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=4)
    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            action = request.POST.get('action')
            if action == 'save_and_add':
                return redirect('create_question', quiz_id=quiz.id)
            elif action == 'save_quiz':
                messages.success(request, f"New quiz is created")
                return redirect('quiz_info', quiz_id=quiz.id)
    else:
        formset = ChoiceFormSet()
    return render(request, 'create_choice.html', {'formset': formset, 'quiz': quiz, 'question': question})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile is updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context=context)
