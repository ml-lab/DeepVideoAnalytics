from django.contrib import admin
from .models import Video,Frame,Dataset,Detection,TEvent

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    pass


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    pass


@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    pass


@admin.register(TEvent)
class TEventAdmin(admin.ModelAdmin):
    pass


