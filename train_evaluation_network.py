from training_data_utils import load_training_data
import os
import sqlite3
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn as nn
from evaluation_network import EvaluationNet

# Define the database path
db_folder = "G:\\VS Code\\Mahjong_Data"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "mahjong_eval_net_training_data.db")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

data, targets = load_training_data(conn, decay=0.95)

# Create data loader
dataset = TensorDataset(data, targets)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Initialize model, optimizer, and loss function
model_save_path = "G:\\VS Code\\Mahjong AI\\Evaluation_Network.pth"
model = EvaluationNet()

optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

if os.path.exists(model_save_path):
    # Loading the model and optimizer state
    checkpoint = torch.load(model_save_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1  # To continue from the last saved epoch
    print(f"Evaluation Model loaded successfully. Resuming training at epoch {start_epoch+1}.")
else:
    start_epoch = 0
    print("No saved model found. Initializing new Evaluation Model.")

# Training Loop
num_epochs = 41
for epoch in range(start_epoch, start_epoch + num_epochs):
    model.train()
    total_loss = 0

    for batch_data, batch_targets in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_data)
        batch_targets = batch_targets.unsqueeze(1)
        loss = criterion(predictions, batch_targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{start_epoch+num_epochs}, Loss: {total_loss/len(train_loader)}")

# Save both model and optimizer states
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch,
}, model_save_path)

