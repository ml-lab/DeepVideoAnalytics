from __future__ import absolute_import
import subprocess,sys,shutil,os,glob,time
from django.conf import settings
from celery import shared_task
from .models import Video, Frame, Detection, TEvent, Query, IndexEntries,QueryResults
from dvalib import entity
import json
import zipfile



@shared_task
def perform_indexing(video_id):
    dv = Video.objects.get(id=video_id)
    video = entity.WVideo(dv, settings.MEDIA_ROOT)
    frames = Frame.objects.all().filter(video=dv)
    for index_results in video.index_frames(frames):
        i = IndexEntries()
        i.video = dv
        i.count = index_results['count']
        i.algorithm = index_results['index_name']
        i.save()

@shared_task
def query_by_image(query_id):
    dq = Query.objects.get(id=query_id)
    Q = entity.WQuery(dquery=dq, media_dir=settings.MEDIA_ROOT)
    results = Q.find()
    dq.results = True
    for algo,rlist in results.iteritems():
        for r in rlist:
            qr = QueryResults()
            qr.query = dq
            qr.frame_id = r['frame_primary_key']
            qr.video_id = r['video_primary_key']
            qr.algorithm = algo
            qr.distance = r['dist']
        qr.save()
    dq.results_metadata = json.dumps(results)
    dq.save()
    return results


@shared_task
def extract_frames(video_id):
    start = TEvent()
    start.video_id = video_id
    start.started = True
    start.save()
    dv = Video.objects.get(id=video_id)
    v = entity.WVideo(dvideo=dv, media_dir=settings.MEDIA_ROOT)
    time.sleep(3) # otherwise ffprobe randomly fails
    if not dv.dataset:
        v.get_metadata()
        dv.metadata = v.metadata
        dv.length_in_seconds = v.duration
        dv.height = v.height
        dv.width = v.width
        dv.save()
    frames = v.extract_frames()
    for f in frames:
        df = Frame()
        df.time_seconds = f.time_seconds
        df.video = dv
        df.save()
    # perform_detection_video.apply_async(args=[dv.id, ], queue=settings.Q_DETECTOR)
    finished = TEvent()
    finished.completed = True
    finished.video_id = video_id
    finished.save()
    perform_indexing.apply_async(args=[video_id],queue=settings.Q_INDEXER)
    return 0

# @shared_task
# def perform_detection_video(video_id):
#     from . import wmodels
#     frame_paths = []
#     frame_dict = {}
#     try:
#         os.mkdir(TEMP_DIR)
#     except:
#         pass
#     dv = Video.objects.get(id=video_id)
#     frames = Frame.objects.all().filter(video=dv)
#     for df in frames:
#         f = wmodels.WFrame(df,temp_dir=TEMP_DIR)
#         f.download()
#         frame_paths.append(f.local_path)
#         frame_dict[f.key.split('/')[-1].split('.')[0]] = df
#     return yolo_detect(frame_paths,frame_dict,dv)
# def yolo_detect(frame_paths,frame_dict,source_video=None):
#     darknet_dir = '/Users/aub3/Dropbox/Projects/DCA/darknet' if sys.platform == 'darwin' else '/home/ec2-user//darknet'
#     with open('{}/data/images.txt'.format(darknet_dir),'w') as out:
#         for path in frame_paths:
#             out.write('{}\n'.format(path))
#     args = ["./darknet", 'yolo', 'valid', 'cfg/yolo.cfg', 'yolo.weights']
#     returncode = subprocess.call(args,cwd=darknet_dir)
#     if returncode == 0:
#         for fname in glob.glob('{}/results/*.txt'.format(darknet_dir)):
#             object_name = fname.split('/')[-1].split('.')[0]
#             for line in file(fname):
#                 frame_id,confidence,top_x,top_y,bottom_x,bottom_y=line.strip().split()
#                 confidence,top_x,top_y,bottom_x,bottom_y = \
#                     float(confidence),float(top_x),float(top_y),float(bottom_x),float(bottom_y)
#                 if confidence > 0.05:
#                     dd = Detection()
#                     if source_video:
#                         dd.video = source_video
#                     dd.frame = frame_dict[frame_id]
#                     dd.object_name = object_name
#                     dd.confidence = confidence
#                     dd.x = top_x
#                     dd.y = top_y
#                     dd.w = bottom_x - top_x
#                     dd.h = bottom_y - top_y
#                     dd.save()
#     return returncode

