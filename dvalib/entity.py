import boto,shlex,json,os
import subprocess as sp
from boto.s3.key import Key
s3_connection = boto.connect_s3()


class WVideo(object):

    def __init__(self,dvideo,media_dir):
        self.dvideo = dvideo
        self.key = self.dvideo.key
        self.primary_key = self.dvideo.pk
        self.bucket = self.dvideo.bucket
        self.file_name = self.key.split('/')[-1]
        self.media_dir = media_dir
        self.local_path = "{}/{}/video/{}.mp4".format(self.media_dir,self.primary_key,self.primary_key)
        self.duration = None
        self.width = None
        self.height = None
        self.metadata = {}

    def download(self):
        bucket = s3_connection.get_bucket(self.bucket)
        s3key = bucket.get_key(self.key)
        with open(self.local_path, 'w') as fh:
            s3key.get_contents_to_file(fh)

    def get_metadata(self):
        command = ['ffprobe','-i',self.local_path,'-print_format','json','-show_format','-show_streams','-v','quiet']
        p = sp.Popen(command,stdout=sp.PIPE,stderr=sp.STDOUT,stdin=sp.PIPE)
        p.wait()
        output, _ = p.communicate()
        self.metadata = json.loads(output)
        try:
            self.duration = float(self.metadata['format']['duration'])
            self.width = float(self.metadata['streams'][0]['width'])
            self.height = float(self.metadata['streams'][0]['height'])
        except:
            raise ValueError,str(self.metadata)

    def extract_frames(self):
        frames = []
        frame_seconds = set()
        for i in range(int(self.duration)):
            if i % 10 == 0:
                frame_seconds.add(i)
                frame_seconds.add(i+1)
        output_dir = "{}/{}/{}/".format(self.media_dir,self.primary_key,'frames')
        for s in frame_seconds:
            fname = "{}.jpg".format(s)
            command = 'ffmpeg -accurate_seek -ss {} -i {} -y -frames:v 1 -vf scale=600:-1 {}/{}'.format(s,
                                                                                                     self.local_path,
                                                                                                     output_dir,fname)
            extract = sp.Popen(shlex.split(command))
            extract.wait()
            if extract.returncode != 0:
                raise ValueError
            f = WFrame(time_seconds=s,video=self)
            if extract.returncode != 0:
                raise ValueError
            frames.append(f)
        return frames


class WFrame(object):

    def __init__(self,time_seconds=None,video=None):
        if video:
            self.time_seconds = time_seconds
            self.video = video
        else:
            self.time_seconds = None
            self.video = None

    def local_path(self):
        return "{}/{}/{}/{}.jpg".format(self.video.media_dir,self.video.primary_kcy,'frames',self.time_seconds)
