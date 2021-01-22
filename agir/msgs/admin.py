from django.contrib import admin
from reversion.admin import VersionAdmin

from agir.msgs.models import SupportGroupMessage


@admin.register(SupportGroupMessage)
class SupportGroupMessageAdmin(VersionAdmin):
    autocomplete_fields = ("supportgroup", "linked_event")
    readonly_fields = ("author",)
