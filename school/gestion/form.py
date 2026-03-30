from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, Etudiant, Matiere

class Custom(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Etudiant'),
        ('teacher', 'Enseignant'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    classe = forms.CharField(max_length=50, required=False, label="Classe")
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        
    )
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "role", "classe","password1", "password2");

class NoteForm(forms.Form):
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.all(),
        label='Etudiant'
    )
    matiere = forms.CharField(
        max_length=100,
        required=True,
        label='Matiere'
    )
    valeur = forms.FloatField(
        label='Note',
        min_value=0,
        max_value=20
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('enseignant', None)
        super().__init__(*args, **kwargs)