from django.shortcuts import render
from .forms import *
from .models import *
from django.views.generic import FormView
from django.urls import reverse_lazy
# Create your views here.

class PostCreateView(FormView):
    template_name = 'post_app/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('chat')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs["links"] = self.request.POST.getlist(key = "link")
            kwargs["images"] = self.request.FILES.getlist(key = "images")
        
        return kwargs
     
    # get_form_kwargs - метод в класі FormView, який допомагає вказати додаткові дані які буде відправленно в форму