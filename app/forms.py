from django import forms
from app.models import Scientist


class ScientistForm(forms.ModelForm):
    class Meta:
        model = Scientist
        fields = [
            'first_name',
            'last_name',
            'sex',
            'email',
            'scientific_area',
            'position',
            'twitter_handler',
            'gscholar_profile',
            'scopus_profile',
            'orcid'
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'sex': 'Sexo',
            'scientific_area': 'Area de Investigación',
            'position': 'Posición',
            'twitter_handler': 'Usuario de Twitter (sin @)',
            'gscholar_profile': 'Perfil de Google Scholar',
            'scopus_profile': 'Perfil de Scopus',
            'orcid': 'Orcid'
        }
