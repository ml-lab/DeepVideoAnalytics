import numpy as np
import os,glob,logging
import torch
import PIL
from torch.autograd import Variable
from torchvision import transforms
from dvalib import resnet
from scipy import spatial

class Resnet50Indexer(object):

    def __init__(self):
        self.name = "resnet50"
        self.net = None
        self.transform = None
        self.indexed_dirs = set()
        self.index, self.files, self.findex = None, {}, 0

    def load(self):
        if self.net is None:
            logging.warning("Loading the network")
            self.net = resnet.resnet50(pretrained=True)
            self.transform = transforms.Compose([
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean = [ 0.485, 0.456, 0.406 ],std = [ 0.229, 0.224, 0.225 ]),
                ])

    def apply(self,path):
        self.load()
        tensor = self.transform(PIL.Image.open(path).convert('RGB'))
        return self.net(Variable(tensor.unsqueeze_(0))).data.numpy()

    def load_index(self,path):
        temp_index = []
        for dirname in os.listdir(path +"/"):
            fname = "{}/{}/indexes/{}.npy".format(path,dirname,self.name)
            if dirname not in self.indexed_dirs and dirname != 'queries' and os.path.isfile(fname):
                logging.info("Starting {}".format(fname))
                self.indexed_dirs.add(dirname)
                try:
                    t = np.load(fname)
                    if max(t.shape) > 0:
                        temp_index.append(t)
                    else:
                        raise ValueError
                except:
                    logging.error("Could not load {}".format(fname))
                    pass
                else:
                    for i, f in enumerate(file(fname.replace(".npy", ".framelist")).readlines()):
                        time_seconds,frame_pk = f.strip().split('_')
                        self.files[self.findex] = {
                            'time_seconds':time_seconds,
                            'video_primary_key':dirname,
                            'frame_primary_key':frame_pk
                        }
                        # ENGINE.store_vector(index[-1][i, :], "{}".format(findex))
                        self.findex += 1
                    logging.info("Loaded {}".format(fname))
        if self.index is None:
            self.index = np.concatenate(temp_index)
            self.index = self.index.squeeze()
            logging.info(self.index.shape)
        elif temp_index:
            self.index = np.concatenate([self.index, np.concatenate(temp_index).squeeze()])
            logging.info(self.index.shape)

    def nearest(self,image_path,n=12):
        query_vector = self.apply(image_path)
        temp = []
        dist = []
        logging.info("started query")
        for k in xrange(self.index.shape[0]):
            temp.append(self.index[k])
            if (k+1) % 50000 == 0:
                temp = np.transpose(np.dstack(temp)[0])
                dist.append(spatial.distance.cdist(query_vector,temp))
                temp = []
        if temp:
            temp = np.transpose(np.dstack(temp)[0])
            dist.append(spatial.distance.cdist(query_vector,temp))
        dist = np.hstack(dist)
        ranked = np.squeeze(dist.argsort())
        logging.info("query finished")
        results = []
        for i, k in enumerate(ranked[:n]):
            temp = {'i':i,'algo':self.name,'dist':dist[0,k]}
            temp.update(self.files[k])
            results.append(temp)
        return results

    def index_frames(self,frames,video):
        files = []
        features = []
        media_dir = video.media_dir
        for f in frames:
            files.append("{}_{}".format(f.time_seconds,f.primary_key))
            features.append(self.apply(f.local_path()))
        feat_fname = "{}/{}/indexes/{}.npy".format(media_dir,video.primary_key,self.name)
        files_fname = "{}/{}/indexes/{}.framelist".format(media_dir, video.primary_key,self.name)
        with open(feat_fname, 'w') as feats:
            np.save(feats, np.array(features))
        with open(files_fname, 'w') as filelist:
            filelist.write("\n".join(files))
        return {'index_name':self.name,'count':len(features)}

INDEXERS = {
    'resnet50':Resnet50Indexer(),
    }