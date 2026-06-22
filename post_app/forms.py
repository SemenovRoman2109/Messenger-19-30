from .models import *
from django import forms 
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# io - модуль для роботи з пам'ятю комп'ютера 
MAX_IMAGE_SIZE = 5 * 1024 * 1024

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def clean(self, data, initial = None):
        # isinstance(змінна, клас) - перевіряє чи належить змінна класу(типу даних)
        if isinstance(data, (list, tuple)):
            list_files = []
            for file in data:
                clean_file = super().clean(file, initial)
                list_files.append(clean_file)
            return list_files
        return super().clean(file, initial)

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label = "Оберіть теги",
        queryset = PostTag.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple
    )
    images = MultipleFileField(
        label = 'Зображення',
        required= False,
        widget= MultiFileInput(
            attrs= {'multiple': True, "accept": "images/*"}
        )
    )
    class Meta:
        model = Post
        fields = ['title', 'topic', 'content']
        widget = {
            "title" : forms.TextInput(attrs= {"placeholder" : "Назва"}),
            "topic" : forms.TextInput(attrs= {"placeholder" : "Тема"}),
            "content" : forms.Textarea(attrs= {"rows": 5, "placeholder" : "Текст"})
        }
        # labels - cловник в класі форми, що зберігає заголовки полей для вводу
        labels = {
            "title" : "Назва публікації",
            "topic" : "Тема публікації",
            "content" : "Зміст публікації", 
        }
    # __init__ - метод в формі, що спрацює при отримані даних ( допомагає передати додаткові значення )
    def __init__(self, *args, links = None, images = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.links_list = []
        self.images_list = []

        if links:
            for link in links:
                clean_link = link.strip()
                if clean_link:
                    self.links_list.append(clean_link)
        
        if images:
            self.images_list = list(images)

    def clean(self):
        cleaned_data = super().clean()

        url_field = forms.URLField()
        image_field = forms.ImageField()

        for link in self.links_list:
            try:
                url_field.clean(link)
            except forms.ValidationError:
                self.add_error(field = None, error = f"Некоректне посилання: {link}")

        for image in self.images_list:
            try:
                image_field.clean(image)
            except forms.ValidationError:
                self.add_error(field = None, error = "Некоректне зображення")

        return cleaned_data
    
    def save(self, author, commit = True):
        post = super().save(commit = False)
        post.author = author
         
        if commit:
            post.save()
            post.tags.set(self.cleaned_data.get("tags"))
            print(self.links_list, self.images_list)
            for link in self.links_list:
                PostLink.objects.create(url = link, post = post)
            
            for image in self.images_list:
                PostImage.objects.create(
                    post = post,
                    original_image = image,
                    compressed_image = self.compress_image(image)
                )
        return post
            
    def compress_image(self, image):
        image.seek(0)
        img = Image.open(image)
        img = img.convert("RGB")
        quality = 85
        width = img.size[0]
        height = img.size[1]
        # BytesIO - клас, для збереження файлів в оперативній пам'яті (буфері)
        # Image.open(шлях або зображення) - відкриває зображення
        # ContentFile - клас для створення файлів в django ( з django.core.files.base )
        while True:
            buffer_img = BytesIO()
            img.save(buffer_img, format = "JPEG", quality = quality, optimize = True)
            if buffer_img.tell() <  MAX_IMAGE_SIZE:
                break
            else:
                if quality > 40:
                    quality -= 10
                else:
                    width = int(width * 0.9) 
                    height = int(height * 0.9) 
                    img = img.resize((height, width))
        image.seek(0)
        file_name = image.name.rsplit(".", 1)[0]
        image_name = f"compressed_{file_name}.jpeg"
        return ContentFile(buffer_img.getvalue(), name = image_name)
