from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import League, Team, Fixture


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'season']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kibabii Premier League'}),
            'season': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024/25'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter team name'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Fixture
        fields = ['home_score', 'away_score', 'played_on']
        widgets = {
            'home_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'away_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'played_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        home = cleaned_data.get('home_score')
        away = cleaned_data.get('away_score')
        if home is None or away is None:
            raise forms.ValidationError("Both scores are required.")
        return cleaned_data