from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and hasattr(self.user, 'department') and self.user.department:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(department=self.user.department)
        else:
            self.fields['subject'].queryset = self.fields['subject'].queryset.none()


        self.fields['file'].required = False

    class Meta:
        model = Note
        fields = [
            'title',
            'description',
            'file',
            'subject',
            'professor',
            'semester'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded'}),
            'file': forms.FileInput(attrs={'class': 'w-full'}),
            'subject': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'professor': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'semester': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'e.g. Fall 2024'}),
        }