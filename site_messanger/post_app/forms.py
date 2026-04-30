from .models import *
from django import forms 


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label = "Оберіть теги",
        queryset = PostTag.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Post
        fields = ['title', 'topic', 'content']
        widget = {
            "title" : forms.TextInput(attrs= {
                "placeholder" : "Назва"
            }),
            "topic" : forms.TextInput(attrs= {
                "placeholder" : "Тема"
            }),
            "content" : forms.Textarea(attrs= {
                "rows": 5,
                "placeholder" : "Текст"
            } )
        }
        # labels - cловник в класі форми, що зберігає заголовки полей для вводу
        labels = {
            "title" : "Назва публікації",
            "topic" : "Тема публікації",
            "content" : "Зміст публікації", 
        }
