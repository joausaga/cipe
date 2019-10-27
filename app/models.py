from app.constants import SEX, SCIENTIFIC_AREA, POSITION, COMMUNICATION_CHANNELS
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


def compute_slug():
    while True:
        new_slug = get_random_string(32)
        try:
            Scientist.objects.get(slug=new_slug)
        except Scientist.DoesNotExist:
            return new_slug


class Scientist(models.Model):
    slug = models.SlugField(max_length=40, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ci = models.CharField(max_length=100, unique=True)
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
    linkedin_profile = models.URLField(null=True, blank=True)
    researchgate_profile = models.URLField(null=True, blank=True)
    academia_profile = models.URLField(null=True, blank=True)
    institutional_website = models.URLField(null=True, blank=True)
    personal_website = models.URLField(null=True, blank=True)
    orcid_profile = models.URLField(null=True, blank=True)
    has_becal_scholarship = models.BooleanField(default=False)
    end_becal_scholarship = models.DateField(blank=True, null=True)
    communication_channel = models.CharField(max_length=100, choices=COMMUNICATION_CHANNELS, default='')
    approved = models.BooleanField(default=False)
    # audit fields
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        if not self.slug:
            self.slug = compute_slug()
        return super(Scientist, self).save(*args, **kwargs)

    def __unicode__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


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
    # audit fields
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        return super(Institution, self).save(*args, **kwargs)

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
    # audit fields
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        return super(Affiliation, self).save(*args, **kwargs)

    def __unicode__(self):
        return f"{self.scientist}, {self.institution}"

    def __str__(self):
        return f"{self.scientist}, {self.institution}"

    class Meta:
        unique_together = ('scientist', 'institution')