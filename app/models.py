from django.db import models
from app.constants import SEX, SCIENTIFIC_AREA, POSITION


class Scientist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    scientific_area = models.CharField(max_length=100, choices=SCIENTIFIC_AREA, default='')
    position = models.CharField(max_length=100, choices=POSITION, default='')
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=50, null=True, blank=True, choices=SEX)
    twitter_handler = models.CharField(max_length=100, null=True, blank=True)
    gscholar_profile = models.URLField(null=True, blank=True)
    scopus_profile = models.URLField(null=True, blank=True)
    orcid = models.CharField(max_length=100, null=True, blank=True)
    becal = models.BooleanField(default=False)

    def __unicode__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Institution(models.Model):
    name = models.TextField(max_length=300)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    web_page = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Affiliation(models.Model):
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    joined_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return f"{self.scientist.first_name} {self.scientist.last_name}, {self.institution.name}"

    def __str__(self):
        return f"{self.scientist.first_name} {self.scientist.last_name}, {self.institution.name}"

    class Meta:
        unique_together = ('scientist', 'institution')