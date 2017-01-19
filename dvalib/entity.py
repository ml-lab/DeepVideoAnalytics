import boto,shlex,json,os
import subprocess as sp
from boto.s3.key import Key
s3_connection = boto.connect_s3()


class WVideo(object):

    def __init__(self,dvideo,temp_dir):
        self.temp_dir = temp_dir
        self.dvideo = dvideo
        self.key = self.dvideo.key
        self.bucket = self.dvideo.bucket
        self.file_name = self.key.split('/')[-1]
        self.local_path = "{}/{}".format(self.temp_dir,self.file_name)
        self.duration = None
        self.width = None
        self.height = None
        self.metadata = {}

    def download(self):
        bucket = s3_connection.get_bucket(self.bucket)
        s3key = bucket.get_key(self.key)
        with open(self.local_path, 'w') as fh:
            s3key.get_contents_to_file(fh)

    def delete(self):
        os.remove(self.local_path)

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
        for s in frame_seconds:
            f = WFrame()
            fname = "{}_{}.jpg".format(self.file_name.split('.')[0],s)
            command = 'ffmpeg -accurate_seek -ss {} -i {} -y -frames:v 1 -vf scale=600:-1 {}/{}'.format(s,
                                                                                                     self.local_path,
                                                                                                     self.temp_dir,fname)
            extract = sp.Popen(shlex.split(command))
            extract.wait()
            if extract.returncode != 0:
                raise ValueError
            f.init_local(bucket=self.bucket,time_seconds=s,key="frames/"+fname,local_path="{}/{}".format(self.temp_dir,fname),
                         video=self)
            if extract.returncode != 0:
                raise ValueError
            f.upload()
            frames.append(f)
        return frames


class WFrame(object):
    def __init__(self, df=None,temp_dir=None):
        if df:
            self.time_seconds = df
            self.video = df.video
            self.key = df.key
            self.bucket = df.bucket
            self.local_path = "{}/{}".format(temp_dir, self.key.split('/')[-1])
        else:
            self.time_seconds = None
            self.video = None
            self.key = None
            self.bucket = None
            self.local_path = None

    def init_local(self,bucket,key,time_seconds,local_path,video):
        self.time_seconds = time_seconds
        self.video = video
        self.key = key
        self.bucket = bucket
        self.local_path = local_path

    def upload(self):
        bucket = s3_connection.get_bucket(self.bucket)
        k = Key(bucket)
        k.key = self.key
        with open(self.local_path) as fh:
            k.set_contents_from_file(fh)

    def download(self):
        bucket = s3_connection.get_bucket(self.bucket)
        s3key = bucket.get_key(self.key)
        with open(self.local_path, 'w') as fh:
            s3key.get_contents_to_file(fh)
