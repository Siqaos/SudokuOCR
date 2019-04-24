from django import forms
from .models import Post
import cv2
from .sudoku import solve

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['cover']
    def solve(self,img):
        result = solve(img)
        data = result.split()
        return data
        
