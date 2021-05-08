from reversion.admin import VersionAdmin
from django.contrib import admin

from trackers.models import Tracker, Capability, Advertising, \
    Analytic, Network, TrackerCategory, TrackerApproval


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

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []

        if not request.user.is_superuser:
            return excluded + ['is_in_exodus', 'exodus_matches']

        return excluded


@admin.register(TrackerApproval)
class TrackerApprovalModelAdmin(VersionAdmin):
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


@admin.register(TrackerCategory)
class TrackerCategoryModelAdmin(VersionAdmin):
    pass
