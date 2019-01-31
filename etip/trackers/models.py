import re
import uuid

from django.db import models


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


class Tracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    creation_date = models.DateField(auto_now_add=True)
    code_signature = models.CharField(max_length=500, default='', blank=True)
    network_signature = models.CharField(max_length=500, default='', blank=True)
    website = models.URLField()
    capability = models.ManyToManyField(Capability, blank=True)
    advertising = models.ManyToManyField(Advertising, blank=True)
    analytic = models.ManyToManyField(Analytic, blank=True)
    network = models.ManyToManyField(Network, blank=True)
    is_in_exodus = models.BooleanField(default=False)
    maven_repository = models.CharField(max_length=500, default='', blank=True)
    artifact_id = models.CharField(max_length=500, default='', blank=True)
    group_id = models.CharField(max_length=500, default='', blank=True)
    gradle = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.name

    def code_signature_collision(self):
        collisions = []
        signatures = Tracker.objects.all()
        for t in signatures:
            if re.search(self.code_signature, t.code_signature) and len(self.code_signature) > 4:
                if self.id != t.id:
                    collisions.append(t.name)
        return collisions

    def network_signature_collision(self):
        collisions = []
        signatures = Tracker.objects.all()
        for t in signatures:
            if re.search(self.network_signature, t.network_signature) and len(self.network_signature) > 4:
                if self.id != t.id:
                    collisions.append(t.name)
        return collisions

    def progress(self):
        p = 0
        if len(self.description) > 180:
            p += 15
        if len(self.short_description) > 25:
            p += 15
        if len(self.code_signature) > 3:
            p += 10
        if len(self.network_signature) > 3:
            p += 10
        if len(self.website) > 2:
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
        if len(self.description) < 180:
            missing.append('Long description')
        if len(self.short_description) < 25:
            missing.append('Short description')
        if len(self.code_signature) <= 3:
            missing.append('Code signature')
        if len(self.network_signature) <= 3:
            missing.append('Network signature')
        if len(self.website) < 3:
            missing.append('Website')
        if self.capability.count() < 1:
            missing.append('Capabilities')
        if self.analytic.count() < 1:
            missing.append('Analytics')
        if self.advertising.count() < 1:
            missing.append('Advertising')
        if self.network.count() < 1:
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
