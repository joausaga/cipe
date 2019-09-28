from django import forms
from app.constants import SEX, SCIENTIFIC_AREA, POSITION, COMMUNICATION_CHANNELS

SEX_EMPTY = [('','Indique su sexo')] + list(SEX)
SCI_AREA_EMPTY = [('','Indique su área de actuación')] + list(SCIENTIFIC_AREA)
POSITION_EMPTY = [('','Indique su nivel académico')] + list(POSITION)
CHANNEL_EMPTY = [('','Indique un canal de comunicación')] + list(COMMUNICATION_CHANNELS)
BECAL = [(False, 'Es becario BECAL?'), (False, 'No'), (True, 'Si')]


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Nombre'
        }
    ))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Apellido'
        }
    ))
    sex = forms.ChoiceField(label='Sexo', choices=SEX_EMPTY, required=False, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email'
        }
    ))
    phone_number = forms.CharField(label='Teléfono Móvil', required=False, help_text='No olvide el código de país',
                                   widget=forms.TextInput(
                                       attrs={
                                           'class':'form-control',
                                           'placeholder':'Teléfono Móvil'
                                       }
    ))
    has_becal_scholarship = forms.ChoiceField(label='Es becario de BECAL?', choices=BECAL, required=False, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    scientific_area = forms.ChoiceField(label='Area de Actuación', choices=SCI_AREA_EMPTY, widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    position = forms.ChoiceField(label='Nivel Académico', choices=POSITION_EMPTY, widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    communication_channel = forms.ChoiceField(label='Canal Comunicación', required=False, choices=CHANNEL_EMPTY,
                                              help_text='Si desea mantener contacto con los investigadores registrados '
                                                        'en este sitio (se utilizará el que elija la mayoría)',
                                              widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    twitter_handler = forms.CharField(label='Usuario de Twitter', help_text='sin @', required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Usuario de Twitter'
        }
    ))
    facebook_profile = forms.URLField(label='Enlace a Perfil en Facebook', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Perfil de Facebook'
        }
    ))
    gscholar_profile = forms.URLField(label='Perfil de Google Scholar', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Perfil de Google Scholar'
        }
    ))
    scopus_profile = forms.URLField(label='Perfil Scopus', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Perfil Scopus'
        }
    ))
    personal_website = forms.URLField(label='Página web personal', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Página web personal'
        }
    ))
    institutional_website = forms.URLField(label='Perfil en web institucional', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Perfil en web institucional'
        }
    ))
    orcid = forms.CharField(label='Perfile Orcid', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Perfil Orcid'
        }
    ))
    location_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lat = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lng = forms.CharField(widget=forms.HiddenInput(), required=False)