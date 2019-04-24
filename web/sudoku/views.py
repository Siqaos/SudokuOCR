from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
import cv2
import numpy
import base64
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.FILES['cover'].open()
            img = cv2.imdecode(numpy.fromstring(request.FILES['cover'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            request.FILES['cover'].open()
            upFile = request.FILES['cover'].open()
            data = upFile.read()
            encoded = base64.b64encode(data)
            result = form.solve(img)
            mime = "image/png"
            mime = mime + ";" if mime else ";"
            f = {"upFile": "data:%sbase64,%s" % (mime, encoded.decode("utf-8"))}
            return render(request, 'home.html', {'result': result,'image': f})
        else:
            return render(request, 'home.html', {'form': form})