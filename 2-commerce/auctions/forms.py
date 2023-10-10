from django import forms

from .models import Comment, Listing


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Listing
        fields = ['title', 'description', 'categories',
                  'bid', 'web_page', 'img']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
