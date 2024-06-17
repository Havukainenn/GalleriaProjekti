from django import forms
from .models import Image, Folder

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['folder', 'file', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)  # Only user's folders
