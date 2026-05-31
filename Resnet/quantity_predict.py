# -*-coding:utf-8-*-
import os
import sys
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
from torch.autograd import Variable

device = torch.device("cpu")

def load_checkpoint(filepath):
    checkpoint = torch.load(filepath, map_location=device)
    model = checkpoint['model_ft']
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    return model

def process_image(image_path):
    img = Image.open(image_path).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return preprocess(img)

if __name__ == '__main__':
    weights_path = os.path.join(".", "weights", "new_opencv_ckpt_b84_e200.pth")

    print("🔄 조교의 ResNet 뇌를 장착하는 중...")
    model = load_checkpoint(weights_path)
    model.eval()

    # 다중 이미지 탐색을 위한 폴더 경로 설정
    target_dir = os.path.join("..", "Fooddata", "test")

    if not os.path.exists(target_dir):
        print(f"❌ [에러] 탐색할 폴더가 없습니다! 경로 확인: {target_dir}")
        sys.exit()

    # 폴더 내 지원하는 이미지 파일들만 확장자 필터링하여 리스트업
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG')
    image_files = [f for f in os.listdir(target_dir) if f.endswith(valid_extensions)]

    if not image_files:
        print(f"🔍 폴더 내에 분석 가능한 이미지 파일이 없습니다: {target_dir}")
        sys.exit()

    class_names = ['Q1 (아주 적음)', 'Q2 (적음)', 'Q3 (보통 양)', 'Q4 (많음)', 'Q5 (아주 많음)']

    print(f"📂 총 {len(image_files)}개의 이미지를 발견했습니다. 순차 분석을 시작합니다.")
    print('===============================================================')

    # 모든 이미지를 순회하며 예측 루프 가동
    for file_name in image_files:
        target_image_path = os.path.join(target_dir, file_name)

        img_tensor = process_image(target_image_path)
        img_tensor = np.expand_dims(img_tensor, 0)
        img_tensor = torch.from_numpy(img_tensor)

        inputs = Variable(img_tensor).to(device)
        with torch.no_grad():
            logits = model.forward(inputs)
            probs = F.softmax(logits, dim=1)
            conf, pred_class_idx = torch.max(probs, 1)

        idx = pred_class_idx.item()
        confidence_score = conf.item()

        if confidence_score < 0.60:
            if idx > 0:
                idx = idx - 1

        result_grade = class_names[idx]

        print(f"📁 파일명 : {file_name}")
        print(f"📊 등급   : {result_grade}")
        print(f"🔥 확신도 : {confidence_score * 100:.2f}%")
        print('---------------------------------------------------------------')

    print("🎉 모든 이미지에 대한 양 추정 연산이 종료되었습니다.")
    print('===============================================================')