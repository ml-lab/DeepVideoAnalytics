import django,os
from dvalib import indexer

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dva.settings")
    django.setup()
    from dvaapp import tasks
    from dvaapp.models import Video
    for v in Video.objects.all():
        tasks.perform_indexing(v.pk)