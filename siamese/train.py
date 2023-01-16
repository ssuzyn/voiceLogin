from siamese.siameseDataset import SiameseNetworkDataset
from siamese.siamese import SiameseNetwork

import torch.nn
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch import optim
import torch.nn.functional as F
import os

print("현재 디렉토리 위치 : ", os.getcwd())

class Config():
    training_dir = "./static/uploads/"
    train_batch_size = 3
    train_number_epochs = 15

# Loss 함수 정의
class ContrastiveLoss(torch.nn.Module):
    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)
        loss_contrastive = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +
                                      (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))

        return loss_contrastive


def training_time():
    folder_dataset = dset.ImageFolder(root=Config.training_dir)
    siamese_dataset = SiameseNetworkDataset(imageFolderDataset=folder_dataset,
                                        transform=transforms.Compose([transforms.Resize((100,100)),
                                                transforms.ToTensor()]), should_invert=False)
    train_dataloader = DataLoader(siamese_dataset,
                            shuffle=True,
                            num_workers=2,
                            batch_size=Config.train_batch_size)

    net = SiameseNetwork().cuda()
    criterion = ContrastiveLoss()
    optimizer = optim.Adam(net.parameters(),lr = 0.0005 )
    counter = []
    iteration_number= 0

    for epoch in range(0,Config.train_number_epochs): # 100번 학습을 진행
        for i, data in enumerate(train_dataloader,0): # 무작위로 섞인 64개 데이터가 있는 배치가 하나씩 들어온다
            img0, img1 , label = data
            img0, img1 , label = img0.cuda(), img1.cuda() , label.cuda()
            optimizer.zero_grad() # 최적화 초기화
            output1,output2 = net(img0,img1) # 모델에 입력값 대입 후 예측값 산출
            loss_contrastive = criterion(output1,output2,label) # 손실 함수 계산
            loss_contrastive.backward() # 손실 함수 기준으로 역전파 설정
            optimizer.step() # 역전파를 진행하고 가중치 업데이트
            if i %10 == 0 :
                print("Epoch number {}\n Current loss {}\n".format(epoch,loss_contrastive.item()))
                iteration_number +=10
                counter.append(iteration_number)