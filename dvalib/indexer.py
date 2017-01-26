import numpy as np
import torch
import PIL
from torch.autograd import Variable
from torchvision import transforms
from dvalib import resnet


class Indexer(object):

    def __init__(self):
        self.net = None
        self.transform = None

    def load(self):
        if self.net is None:
            self.net = resnet.resnet18(pretrained=True)
            self.transform = transforms.Compose([
                transforms.Scale(224),
                transforms.ToTensor(),
                transforms.Normalize(mean = [ 0.485, 0.456, 0.406 ],std = [ 0.229, 0.224, 0.225 ]),
                ])

    def apply(self,path):
        self.load()
        tensor = self.transform(PIL.Image.open(path).convert('RGB'))
        return self.net(Variable(tensor.unsqueeze_(0))).data.numpy()


INDEXER = Indexer()