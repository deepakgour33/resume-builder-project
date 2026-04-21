from django import forms
from .models import ResumeProfile

class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeProfile
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'photo': forms.FileInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'linkedin': forms.URLInput(attrs={
            'class':'form-control',
            'placeholder':'Optional - https://linkedin.com/in/yourname'
            }),
            'github': forms.URLInput(attrs={
            'class':'form-control',
            'placeholder':'Optional - https://github.com/yourname'
            }),
            'objective': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'skills': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'strengths': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'education': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'cgpa': forms.TextInput(attrs={'class':'form-control'}),
            'experience': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'projects': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'certifications': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'achievements': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'hobbies': forms.Textarea(attrs={'class':'form-control','rows':2}),
            'languages': forms.Textarea(attrs={'class':'form-control','rows':2}),
        }