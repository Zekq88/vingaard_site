import os
import io
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_MODEL_PATH = os.path.join(BASE_DIR, "new_saved_model.pth")

IMG_SIZE = 225

def build_model(device: torch.device) -> nn.Module:
    model = nn.Sequential(
        nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.AdaptiveAvgPool2d((1,1)), nn.Flatten(),
        nn.Dropout(0.3),
        nn.Linear(128, 4)
    ).to(device)

    if os.path.exists(NEW_MODEL_PATH):
        print(f"Loading saved weights from {NEW_MODEL_PATH} ...")
        state_dict = torch.load(NEW_MODEL_PATH, map_location=device)
        #model.load_state_dict(state_dict)
        model.load_state_dict(state_dict)
    else:
        print("Training model from scratch with initialized weights.")
    
    model.eval()
    return model

class ImageClassifier:

    """
    A Wrapper!
    """
    def __init__(self):
        
        self.device = torch.device("cpu")
        self.model = build_model(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
        ])

        self.labels = ["cat", "dog", "horses", "human"]

    def predict_bytes(self, img_bytes: bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        x = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(x)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

        max_idx = probs.argmax()
        label = self.labels[max_idx]
        confidence = float(probs[max_idx])
        all_probs = {cls: float(p) for cls, p in zip(self.labels, probs)}

        
        return label, confidence, all_probs