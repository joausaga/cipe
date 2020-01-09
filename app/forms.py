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
    ci = forms.CharField(label='Cédula de Identidad *', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su cédula de identidad'
        }
    ))
    birth_date = forms.DateField(
        label='Fecha de Nacimiento *',
        required=True,
        help_text='',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker',
                'placeholder': 'Ingrese su nacimiento'
            }
        )
    )
    sex = forms.ChoiceField(label='Sexo *', choices=SEX_EMPTY, required=True, widget=forms.Select(
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
    end_becal_scholarship = forms.DateField(
        label='Fecha estimada de retorno',
        required=False,
        help_text='',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker',
                'placeholder': '',
                'style': 'display:none;'
            }
        )
    )
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
            'placeholder':'Ingrese el enlace a su perfil de Google Scholar'
        }
    ))
    scopus_profile = forms.URLField(label='Perfil de Scopus', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese el enlace a su perfil de Scopus'
        }
    ))
    researchgate_profile = forms.URLField(label='Perfil en Research Gate', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Research Gate'
        }
    ))
    academia_profile = forms.URLField(label='Perfil en Academia', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil en Academia'
        }
    ))
    orcid_profile = forms.CharField(label='Perfil Orcid', required=False, widget=forms.URLInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese el enlace a su perfil Orcid'
        }
    ))
    linkedin_profile = forms.URLField(label='Perfil en Linkedin', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil en Linkedin'
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
    twitter_handler = forms.CharField(label='Usuario de Twitter', help_text='sin @', required=False,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Ingrese su usuario de Twitter'
                                          }
                                      ))
    facebook_profile = forms.URLField(label='Perfil de Facebook', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Facebook',
        }
    ))
    location_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lat = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lng = forms.CharField(widget=forms.HiddenInput(), required=False)


class RegistrationEditForm(forms.Form):
    first_name = forms.CharField(label='Nombre *', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre'
        }
    ))
    last_name = forms.CharField(label='Apellido *', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido'
        }
    ))
    birth_date = forms.DateField(
        label='Fecha de Nacimiento *',
        required=True,
        help_text='',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(
            attrs={
                'class': 'datepicker',
                'placeholder': 'Ingrese su nacimiento'
            }
        )
    )
    sex = forms.ChoiceField(label='Sexo *', choices=SEX_EMPTY, required=True, widget=forms.Select(
        attrs={
            'class': 'form-control'
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
            'class': 'form-control'
        }
    ))
    position = forms.ChoiceField(label='Nivel Académico *', choices=POSITION_EMPTY, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    gscholar_profile = forms.URLField(label='Perfil de Google Scholar', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Google Scholar'
        }
    ))
    scopus_profile = forms.URLField(label='Perfil de Scopus', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Scopus'
        }
    ))
    researchgate_profile = forms.URLField(label='Perfil en Research Gate', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Research Gate'
        }
    ))
    academia_profile = forms.URLField(label='Perfil en Academia', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil en Academia'
        }
    ))
    orcid_profile = forms.CharField(label='Perfil Orcid', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil Orcid'
        }
    ))
    linkedin_profile = forms.URLField(label='Perfil en Linkedin', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil en Linkedin'
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
    twitter_handler = forms.CharField(label='Usuario de Twitter', help_text='sin @', required=False,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Ingrese su usuario de Twitter'
                                          }
                                      ))
    facebook_profile = forms.URLField(label='Perfil de Facebook', required=False, widget=forms.URLInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el enlace a su perfil de Facebook',
        }
    ))
    ci = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lat = forms.CharField(widget=forms.HiddenInput(), required=False)
    location_lng = forms.CharField(widget=forms.HiddenInput(), required=False)