from reversion.admin import VersionAdmin
from django.contrib import admin

from trackers.models import Tracker, Capability, Advertising, Analytic, Network


@admin.register(Tracker)
class TrackerModelAdmin(VersionAdmin):
    pass


@admin.register(Capability)
class CapabilityModelAdmin(VersionAdmin):
    pass


@admin.register(Advertising)
class AdvertisingModelAdmin(VersionAdmin):
    pass


@admin.register(Analytic)
class AnalyticModelAdmin(VersionAdmin):
    pass


@admin.register(Network)
class NetworkModelAdmin(VersionAdmin):
    pass
