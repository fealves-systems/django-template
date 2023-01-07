from django import forms
from core.models import Task, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # fields = ()
        exclude = ('owner',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = ()
        exclude = ('owner',)
