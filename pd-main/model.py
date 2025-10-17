import torch
import torch.nn as nn
import torch.nn.functional as F

# Example: Simple classifier model
default_input_size = 10
default_num_classes = 2

class SimpleNet(nn.Module):
    def __init__(self, input_size=default_input_size, num_classes=default_num_classes):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 32)
        self.fc2 = nn.Linear(32, num_classes)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load or initialize model
def load_model():
    model = SimpleNet()
    model.eval()
    return model

# Inference function
def predict(input_list):
    model = load_model()
    with torch.no_grad():
        x = torch.tensor([input_list], dtype=torch.float32)
        logits = model(x)
        probs = torch.softmax(logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
        return {"class": int(pred), "probs": probs.numpy().tolist()[0]}