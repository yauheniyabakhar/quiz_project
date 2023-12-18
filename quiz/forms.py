from django import forms
from django.contrib.auth.models import User
from .models import QuizComment, Profile, Quiz, Question, Choice

class QuizCommentForm(forms.ModelForm):
    class Meta:
        model = QuizComment
        fields = ('content', 'quiz', 'user',)
        widgets = {'quiz': forms.HiddenInput(), 'user': forms.HiddenInput()}

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['topic', 'title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        is_creating_quiz = kwargs.pop('is_creating_quiz', False)
        super().__init__(*args, **kwargs)

        if not is_creating_quiz:
            self.fields.pop('topic')
            self.fields.pop('title')
            self.fields.pop('description')
            self.fields.pop('image')

        if self.instance.pk:
            questions = self.instance.question_set.all()
            for question in questions:
                choices = question.choice_set.all()
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=[(choice.id, choice.text) for choice in choices],
                    widget=forms.RadioSelect,
                    label=question.text
                )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class BaseChoiceFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        correct_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_correct'):
                correct_count += 1
        if correct_count != 1:
            raise forms.ValidationError('Exactly one choice must be marked as correct.')

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
