from django.contrib import admin
from app.models import Scientist, Affiliation, Institution


@admin.register(Scientist)
class ScientistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'scientific_area', 'affiliation', 'position', 'approved')
    ordering = ('last_name',)

    def affiliation(self, obj):
        return Affiliation.objects.filter(scientist=obj)[0].institution
    affiliation.short_description = 'Affiliation'


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city')
    ordering = ('name', 'country', 'city')


@admin.register(Affiliation)
class AffiliationnAdmin(admin.ModelAdmin):
    list_display = ('scientist', 'institution', 'joined_date')
    ordering = ('scientist', 'institution', 'joined_date')