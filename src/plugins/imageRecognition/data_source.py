import torch
import pickle
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from typing import List, Dict
from PIL import Image

model = EfficientNet.from_name('efficientnet-b4', num_classes=108)
model.load_state_dict(torch.load('./src/plugins/imageRecognition/EfficientNet_0.82.pth',
                                 map_location='cpu'))
model.eval()
device = torch.device("cpu")

preprocess_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


with open('./src/plugins/imageRecognition/label.pickle', 'rb') as file:
    LABELS = pickle.load(file)


def predict(img: Image) -> List[Dict[str, float]]:
    image_tensor = preprocess_transform(img)
    image_tensor.unsqueeze_(0)
    image_tensor = image_tensor.to(device)
    out = model(image_tensor)

    percentage = torch.nn.functional.softmax(out, dim=1)[0:5] * 100

    _, indices = torch.sort(out, descending=True)

    return [{"name": LABELS[i], "score": percentage[0][i].item()} for i in indices[0] if percentage[0][i].item() > 50]


