import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
from torch.autograd import Variable
import PIL.ImageOps    
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

class Config():
    testing_dir = "./voice/uploads/" # -> 로그인할때 녹음 하나 파일이 필요하니까 디렉토리 말고 파일로
    train_batch_size = 3  #배치 사이즈 = 64
    train_number_epochs = 15  #20번 학습을 진행한다