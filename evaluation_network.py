import torch
import torch.nn as nn

class EvaluationNet(nn.Module):
    def __init__(self):
        super(EvaluationNet, self).__init__()
        self.fc1 = nn.Linear(1851, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 128)
        self.fc4 = nn.Linear(128, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x