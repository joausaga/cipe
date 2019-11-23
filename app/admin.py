from app.models import Scientist, Affiliation, Institution
from django import forms
from django.contrib import admin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from app.utils import get_location_info_from_name

import csv
import datetime
import logging
import re


logger = logging.getLogger(__name__)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


# Take from
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
class ExportCsvMixin:

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected"


@admin.register(Scientist)
class ScientistAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('first_name', 'last_name', 'email', 'scientific_area', 'affiliation', 'position', 'approved')
    ordering = ('last_name',)
    change_list_template = "admin/scientist_changelist.html"
    list_filter = ('has_becal_scholarship',)

    def affiliation(self, obj):
        return Affiliation.objects.filter(scientist=obj)[0].institution
    affiliation.short_description = 'Affiliation'

    def __adjust_dict_keys(self, row_dict):
        new_dict = {}
        for key, value in row_dict.items():
            new_dict[key.strip()] = value
        return new_dict

    def __get_date(self, str_end_date):
        try:
            return datetime.datetime.strptime(str_end_date, '%m/%d/%Y')
        except ValueError:
            try:
                return datetime.datetime.strptime(str_end_date, '%d/%m/%Y')
            except ValueError:
                return datetime.datetime.strptime(str_end_date, '%d/%m/%y')

    def __process_becal_csv(self, csv_reader):
        current_year = datetime.datetime.now().year
        for row in csv_reader:
            row = self.__adjust_dict_keys(row)
            logger.info(f"Processing record: {row['ci']}")
            ci = re.sub(r'[^0-9]+', '', row['ci'])
            scholarship_end_date = self.__get_date(row['fecha_fin_estudio'])
            institution_join_date = self.__get_date(row['fecha_inicio_estudio'])
            try:
                Scientist.objects.get(ci=ci)
                logger.info(f"Scientist already in the database")
            except Scientist.DoesNotExist:
                with transaction.atomic():
                    year_of_birth = current_year - int(row['edad'])
                    tentative_birth_date = datetime.datetime(year_of_birth, 1, 1)
                    if 'doctorado' in row['tipo_beca'].lower():
                        position = 'doctorando'
                    elif 'maest' in row['tipo_beca'].lower():
                        position = 'master_academico'
                    else:
                        raise Exception(f"Cannot recognize the position {row['tipo_beca']}")
                    # get location info
                    try:
                        inst_obj = Institution.objects.get(name__iexact=row['universidad'].strip())
                    except Institution.DoesNotExist:
                        success, address, postal_code, city, region, country, latitude, longitude = \
                            get_location_info_from_name(row['universidad'].strip())
                        if not success:
                            raise Exception(f"Could not get information of location {row['universidad']}")
                        else:
                            inst_dict = {
                                'name': row['universidad'].strip().title(),
                                'country': country,
                                'city': city,
                                'region': region,
                                'postal_code': postal_code,
                                'address': address,
                                'latitude': latitude,
                                'longitude': longitude
                            }
                            inst_obj = Institution(**inst_dict)
                            inst_obj.save()
                            logger.info(f"Institution {inst_dict} created!")
                    scientist_dict = {
                        'first_name': row['nombres'].strip().title(),
                        'last_name': row['apellidos'].strip().title(),
                        'ci': ci,
                        'email': ci + '@cipe.temporal',
                        'sex': row['sexo'].strip().lower() if row['sexo'].strip() in ['Masculino', 'Femenino'] else 'otro',
                        'birth_date': tentative_birth_date,
                        'position': position,
                        'scientific_area': row['area_estudio_agregado'].strip(),
                        'has_becal_scholarship': True,
                        'end_becal_scholarship': scholarship_end_date,
                        'approved': True
                    }
                    scientist_obj = Scientist(**scientist_dict)
                    scientist_obj.save()
                    logger.info(f"Scientist {scientist_obj} created!")
                    affiliation_obj, created = Affiliation.objects.get_or_create(scientist=scientist_obj,
                                                                                 institution=inst_obj,
                                                                                 defaults={'scientist': scientist_obj,
                                                                                           'institution': inst_obj,
                                                                                           'joined_date': institution_join_date})

    def __decode_utf8(self, input_iter):
        for l in input_iter:
            yield l.decode('utf-8')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_reader = csv.DictReader(self.__decode_utf8(csv_file))
            # Create Scientist objects from passed in data
            self.__process_becal_csv(csv_reader)
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city')
    ordering = ('name', 'country', 'city')


@admin.register(Affiliation)
class AffiliationnAdmin(admin.ModelAdmin):
    list_display = ('scientist', 'institution', 'joined_date')
    ordering = ('scientist', 'institution', 'joined_date')