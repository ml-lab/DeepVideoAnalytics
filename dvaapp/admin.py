from django.contrib import admin
from .models import Video,Frame,Detection,TEvent,IndexEntries


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    pass


@admin.register(IndexEntries)
class IndexEntriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    pass


@admin.register(TEvent)
class TEventAdmin(admin.ModelAdmin):
    pass


