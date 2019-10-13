from django import forms
from app.constants import SEX, SCIENTIFIC_AREA, POSITION, COMMUNICATION_CHANNELS

SEX_EMPTY = [('','Indique su sexo')] + list(SEX)
SCI_AREA_EMPTY = [('','Seleccione un área')] + list(SCIENTIFIC_AREA)
POSITION_EMPTY = [('','Seleccione su nivel académico')] + list(POSITION)
CHANNEL_EMPTY = [('','Indique un canal de comunicación')] + list(COMMUNICATION_CHANNELS)
BECAL = [(False, 'Indique si es becario de BECAL'), (False, 'No'), (True, 'Si')]


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Nombre *', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su nombre'
        }
    ))
    last_name = forms.CharField(label='Apellido *', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su apellido'
        }
    ))
    sex = forms.ChoiceField(label='Sexo *', choices=SEX_EMPTY, required=False, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(label='Email *', widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su correo electrónico'
        }
    ))
    has_becal_scholarship = forms.ChoiceField(label='Es becario de BECAL?', choices=BECAL, required=False,
                                              widget=forms.Select(
                                                attrs={
                                                    'class': 'form-control',
                                                    'onchange': "showBecalEndDate();"
                                                })
                                              )
    end_becal_scholarship = forms.DateField(label='Fecha estimada de retorno', required=False, help_text='',
                                            input_formats=['%d/%m/%Y'],
                                            widget=forms.TextInput(
                                                attrs={
                                                    'class': 'datepicker',
                                                    'placeholder': '',
                                                    'style': 'display:none;'
                                                }
                                            ))
    scientific_area = forms.ChoiceField(label='Area de Actuación *', choices=SCI_AREA_EMPTY, widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    position = forms.ChoiceField(label='Nivel Académico *', choices=POSITION_EMPTY, widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    gscholar_profile = forms.URLField(label='Perfil de Google Scholar', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese el enlance su perfil de Google Scholar'
        }
    ))
    scopus_profile = forms.URLField(label='Perfil de Scopus', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese el enlacen a su perfil de Scopus'
        }
    ))
    orcid = forms.CharField(label='Perfile Orcid', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese el enlace a su perfil Orcid'
        }
    ))
    twitter_handler = forms.CharField(label='Usuario de Twitter', help_text='sin @', required=False,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Ingrese su usuario de Twitter'
                                          }
                                      ))
    personal_website = forms.URLField(label='Página web personal', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su página web personal'
        }
    ))
    institutional_website = forms.URLField(label='Perfil en web institucional', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil en la web institucional'
        }
    ))
    facebook_profile = forms.URLField(label='', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Facebook',
        }
    ))
    location_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lat = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lng = forms.CharField(widget=forms.HiddenInput(), required=False)