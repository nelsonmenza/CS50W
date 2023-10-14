from django import forms

from .models import Bid, Comment, Listing


class ListingForm(forms.ModelForm):
    """
    Form for creating or updating a listing.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Listing
        fields = ['title', 'description', 'categories',
                  'starting_bid', 'web_page', 'img']


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to a listing.
    """
    class Meta:
        model = Comment
        fields = ['body']


class BidForm(forms.ModelForm):
    """
    Form for placing bids on a listing.
    """
    class Meta:
        model = Bid
        fields = ['amount']
