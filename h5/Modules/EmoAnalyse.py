import PIL.Image
import paddle
import paddle.nn.functional as F
from paddle.io import DataLoader
from paddle.io import Dataset
from paddle.vision.models import vgg19
from paddle.vision.transforms import Compose, Resize, Normalize, ToTensor

transform = Compose([
    Resize((48, 48)),
    ToTensor(),
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

VGGmodel = vgg19(num_classes=7)
VGGmodel.set_state_dict(paddle.load("Srcs/EmoAnalyse.model"))
VGGmodel.eval()

label = {'angry': 0, 'disgusted': 1, 'fearful': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprised': 6}


class EmotionDataset(Dataset):
    def __init__(self, picture, transform: Compose = None):
        super().__init__()
        self.transform = transform
        self.images = []
        self.labelHash = {}

        self.labelHash["test"] = len(self.labelHash)
        self.images.append(["test", picture])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        label, img_data = self.images[idx]
        img = self.transform(img_data)
        label = self.labelHash[label]
        return label, img


def predict(picture):
    dataset = EmotionDataset(picture, transform)
    loader = DataLoader(dataset, batch_size=1)
    for batch_id, (labels, images) in enumerate(loader()):
        output = F.softmax(VGGmodel(images),axis=-1).tolist()[0]
        pre = {
            key: output[value] for key, value in label.items()
        }
        return pre


if __name__ == '__main__':
    a = PIL.Image.open(r'D:\我的文档\Documents\项目\python\AI创意赛\SpeechRecog\UI\MainWindow\1.png')
    print(predict(a))
