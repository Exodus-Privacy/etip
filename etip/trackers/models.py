import re
import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_in_exodus = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Capability(Category):
    pass


class Advertising(Category):
    pass


class Analytic(Category):
    pass


class Network(Category):
    pass


class TrackerCategory(Category):
    pass


class Tracker(models.Model):
    MIN_SIGNATURE_SIZE = 4
    MIN_DESCRIPTION_SIZE = 180
    MIN_WEBSITE_SIZE = 3
    EXPORTABLE_FIELDS = [
        'name', 'code_signature', 'network_signature', 'website'
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateField(auto_now_add=True)
    code_signature = models.CharField(max_length=500, default='', blank=True)
    network_signature = models.CharField(max_length=500, default='', blank=True)
    website = models.URLField()
    category = models.ManyToManyField(TrackerCategory, blank=True)
    is_in_exodus = models.BooleanField(default=False)
    capability = models.ManyToManyField(Capability, blank=True)
    advertising = models.ManyToManyField(Advertising, blank=True)
    analytic = models.ManyToManyField(Analytic, blank=True)
    network = models.ManyToManyField(Network, blank=True)
    maven_repository = models.CharField(max_length=500, default='', blank=True)
    artifact_id = models.CharField(max_length=500, default='', blank=True)
    group_id = models.CharField(max_length=500, default='', blank=True)
    gradle = models.CharField(max_length=500, default='', blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        try:
            re.compile(self.code_signature)
        except re.error:
            raise ValidationError(
                {'code_signature': "Must be a valid regex."}
            )

    def has_any_signature_collision(self):
        trackers = Tracker.objects.all().exclude(id=self.id)
        for t in trackers:
            if self._has_same_code_signature(t) \
                    or self._has_same_network_signature(t):
                return True
        return False

    def get_trackers_with_code_signature_collision(self):
        collisions = []
        trackers = Tracker.objects.all().exclude(id=self.id)
        for t in trackers:
            if self._has_same_code_signature(t):
                collisions.append(t.name)
        return collisions

    def get_trackers_with_network_signature_collision(self):
        collisions = []
        trackers = Tracker.objects.all().exclude(id=self.id)
        for t in trackers:
            if self._has_same_network_signature(t):
                collisions.append(t.name)
        return collisions

    def _has_same_network_signature(self, tracker):
        return re.search(self.network_signature, tracker.network_signature) \
            and len(self.network_signature) > self.MIN_SIGNATURE_SIZE

    def _has_same_code_signature(self, tracker):
        return re.search(self.code_signature, tracker.code_signature) \
            and len(self.code_signature) > self.MIN_SIGNATURE_SIZE

    def progress(self):
        p = 0
        if self.category.count() > 0:
            p += 15
        if len(self.description) >= self.MIN_DESCRIPTION_SIZE:
            p += 15
        if len(self.code_signature) >= self.MIN_SIGNATURE_SIZE:
            p += 10
        if len(self.network_signature) >= self.MIN_SIGNATURE_SIZE:
            p += 10
        if len(self.website) >= self.MIN_WEBSITE_SIZE:
            p += 10
        if self.capability.count() > 0:
            p += 10
        if self.analytic.count() > 0:
            p += 10
        if self.advertising.count() > 0:
            p += 10
        if self.network.count() > 0:
            p += 6
        if self.maven_repository:
            p += 1
        if self.artifact_id:
            p += 1
        if self.group_id:
            p += 1
        if self.gradle:
            p += 1
        return p

    def missing_fields(self):
        missing = []
        if self.category.count() == 0:
            missing.append('Categories')
        if len(self.description) < self.MIN_DESCRIPTION_SIZE:
            missing.append('Description')
        if len(self.code_signature) < self.MIN_SIGNATURE_SIZE:
            missing.append('Code signature')
        if len(self.network_signature) < self.MIN_SIGNATURE_SIZE:
            missing.append('Network signature')
        if len(self.website) < self.MIN_WEBSITE_SIZE:
            missing.append('Website')
        if self.capability.count() == 0:
            missing.append('Capabilities')
        if self.analytic.count() == 0:
            missing.append('Analytics')
        if self.advertising.count() == 0:
            missing.append('Advertising')
        if self.network.count() == 0:
            missing.append('Networks')
        if not self.maven_repository:
            missing.append('Maven repository')
        if not self.artifact_id:
            missing.append('Artifact ID')
        if not self.group_id:
            missing.append('Group ID')
        if not self.gradle:
            missing.append('Gradle')
        return missing
