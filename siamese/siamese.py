import torch.nn as nn

# Convolution 계층 정의
class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(1, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),
            
            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),


        )

        self.fc1 = nn.Sequential(
            nn.Linear(8*100*100, 500), # 입력층(80,000) -> 은닉층1(500)으로 가는 연산산
            nn.ReLU(inplace=True),

            nn.Linear(500, 500), # 은닉층1(500) -> 은닉층2(500)으로 가는 연산
            nn.ReLU(inplace=True),

            nn.Linear(500, 5)) # 은닉층2(500) -> 출력층(5)으로 가는 연산산

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2): # 모델 연산의 순서를 정의
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2