from django.db import models
from app.constants import SEX, SCIENTIFIC_AREA, POSITION, COMMUNICATION_CHANNELS


class Scientist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    scientific_area = models.CharField(max_length=100, choices=SCIENTIFIC_AREA, default='')
    position = models.CharField(max_length=100, choices=POSITION, default='')
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=50, null=True, blank=True, choices=SEX)
    twitter_handler = models.CharField(max_length=100, null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    gscholar_profile = models.URLField(null=True, blank=True)
    scopus_profile = models.URLField(null=True, blank=True)
    institutional_website = models.URLField(null=True, blank=True)
    personal_website = models.URLField(null=True, blank=True)
    orcid_profile = models.URLField(null=True, blank=True)
    has_becal_scholarship = models.BooleanField(default=False)
    end_becal_scholarship = models.DateField(blank=True, null=True)
    communication_channel = models.CharField(max_length=100, choices=COMMUNICATION_CHANNELS, default='')
    approved = models.BooleanField(default=False)

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
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    web_page = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Affiliation(models.Model):
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    current = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return f"{self.scientist}, {self.institution}"

    def __str__(self):
        return f"{self.scientist}, {self.institution}"

    class Meta:
        unique_together = ('scientist', 'institution')