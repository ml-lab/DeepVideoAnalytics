from __future__ import absolute_import
import subprocess,sys,shutil,os,glob,time
from django.conf import settings
from celery import shared_task
from .models import Video, Frame, Detection, TEvent


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


# @shared_task
# def perform_indexing(video_id):
#     from dvalib import entity
#     from dvalib import entity
#
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
#         frame_dict[f.local_path] = df.key
#     return inception_index(frame_paths,frame_dict,dv)

@shared_task
def extract_frames(video_id):
    import dvalib
    start = TEvent()
    start.video_id = video_id
    start.started = True
    start.save()
    dv = Video.objects.get(id=video_id)
    v = dvalib.entity.WVideo(dvideo=dv, media_dir=settings.MEDIA_ROOT)
    time.sleep(3) # otherwise ffprobe randomly fails
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
    return 0


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
#
#
# @shared_task
# def inception_index(frame_list,frame_dict,dv):
#     import numpy as np
#     from . import inception
#     indexer = inception.Indexer()
#     inception.load_network()
#     with inception.tf.Session() as sess:
#         for image_data in inception.get_batch(frame_list, batch_size=20):
#             if len(image_data):
#                 start = time.time()
#                 features, files = inception.extract_features(image_data, sess)
#                 start = time.time()
#     feat_fname = "{}/{}.feats_pool3.npy".format(TEMP_DIR,dv.id)
#     files_fname = "{}/{}.files".format(TEMP_DIR,dv.id)
#     with open(feat_fname,'w') as feats:
#         np.save(feats,np.array(features))
#     with open(files_fname,'w') as filelist:
#         filelist.write("\n".join(files))
