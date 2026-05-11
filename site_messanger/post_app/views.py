from django.shortcuts import render
from .forms import *
from .models import *
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class PostCreateView(LoginRequiredMixin, FormView):
    template_name = 'post_app/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('chat')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs["links"] = self.request.POST.getlist(key = "link")
            kwargs["images"] = self.request.FILES.getlist(key = "images")
        
        return kwargs
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            post = form.save(author = self.request.user)
            return JsonResponse(data={
                "success": True
            })
        return JsonResponse(data={
            "success": False
        })

    def form_invalid(self, form):
        return JsonResponse(data={
            "success": False,
            "errors": form.errors.get_json_data()
        })
    
    # form_valid та form_invalid методи класу FormView, що оброблють результат форми
    
class PostListView(ListView):
    template_name = 'post_app/post_list.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    # paginate_by - в ListView вказує скільки елементів буде на 1 сторінці (пагінація - розділення контенту на сторінки, для більш швидкого завантаження)
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == "XMLHttpRequest":
            page_number = request.GET.get("page")
            posts = self.get_queryset()
            paginator = Paginator(posts, self.paginate_by)
            post_list = paginator.get_page(page_number)
            if int(page_number) > paginator.num_pages:
                return JsonResponse({
                    "success" : False
                })
            else:
                return JsonResponse({
                    "success" : True,
                    "html" : render_to_string(template_name = "post_app/posts.html", context ={"posts" : post_list})
                })
        return super().get(request, *args, **kwargs)