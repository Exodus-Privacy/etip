from reversion.admin import VersionAdmin
from django.contrib import admin

from trackers.models import \
    Tracker, Capability, Advertising, Analytic, Network, TrackerCategory


@admin.register(Tracker)
class TrackerModelAdmin(VersionAdmin):
    date_hierarchy = 'created'
    search_fields = ['name']
    list_display = (
        'name',
        'code_signature',
        'network_signature',
        'categories'
    )
    list_filter = ('is_in_exodus',)

    def categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])


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


@admin.register(TrackerCategory)
class TrackerCategoryModelAdmin(VersionAdmin):
    pass
