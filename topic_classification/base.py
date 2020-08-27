import sys, os
import torch
import numpy as np 


def np_softmax(x, dim=-1):
    e = np.exp(x)
    return e / np.sum(e, axis=-1, keepdims=True)

class TopicCLassifier(object):

    def __init__(self, pretrained_model, topics, use_cuda=True, verbose=True):
        super().__init__()

        self.device = torch.device("cuda" if torch.cuda.is_available() and use_cuda else "cpu")
        self.topics = topics

        # Supress stdout printing for model downloads
        if not verbose:
            sys.stdout = open(os.devnull, 'w')
            self._initialize(pretrained_model)
            sys.stdout = sys.__stdout__
        else:
            self._initialize(pretrained_model)
        
    def _initialize(self, pretrained_model):
        raise NotImplementedError

    def __call__(self, context, batch_size=1):
        raise NotImplementedError