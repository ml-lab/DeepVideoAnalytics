import django,os
from dvalib import indexer

if __name__ == '__main__':
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dva.settings")
    # django.setup()
    # from dvaapp import tasks
    # tasks.perform_indexing(7)
    indexer.INDEXER.load_index("/Users/aub3/media/")
    indexer.INDEXER.load_index("/Users/aub3/media/")
    indexer.INDEXER.nearest("/Users/aub3/media/7/frames/0.jpg")