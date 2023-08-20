from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    comment_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
