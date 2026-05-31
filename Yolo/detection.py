# -*-coding:utf-8-*-
import argparse
import os
import sys
import shutil
import random
import time
from pathlib import Path

import torch
import cv2
from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)

os.chdir(current_dir)

from models import *
from utils.datasets import *
from utils.utils import *
if current_dir in sys.path:
    sys.path.remove(current_dir)
sys.path.insert(0, current_dir)
from xml_utils import load_food_name_map, build_and_save_xml

import numpy as np
import platform as pf
import psutil
import pandas as pd

# 🧠 [서버 메모리 캐싱용 전역 변수 선언]
_model = None
_names = None
_food_map = None
_device = None

def init_yolo_model(cfg='yolov3-spp-403cls.cfg', names_path='403food.names', weights='best_403food_e200b150v2.pt', device_id='cpu'):
    """ 서버 부팅 시 가중치 파일을 VRAM/RAM에 딱 한 번만 상주시키는 적립식 캐싱 엔진 """
    global _model, _names, _food_map, _device

    import utils.torch_utils as torch_utils
    _device = torch_utils.select_device(device=device_id)

    imgsz = 320
    _model = Darknet(check_file(cfg), imgsz)

    attempt_download(weights)
    if weights.endswith('.pt'):
        _model.load_state_dict(torch.load(weights, map_location=_device)['model'], strict=False)
    else:
        load_darknet_weights(_model, weights)

    _model.to(_device).eval()
    _names = load_classes(check_file(names_path))
    _food_map = load_food_name_map()
    print("🎯 [AI 전역 모델] YOLOv3 가중치 인라인 메모리 탑재 성공!")

def ToF(file, cat):
    return "T"

def run_yolo_detection(image_path, output_dir, conf_thres=0.15, iou_thres=0.5):
    """
    ⚙️ [정민's 최적화 빌드] subprocess 없이 Flask 가상환경 내부에서 직접 구동되는 핵심 연산 함수
    """
    global _model, _names, _food_map, _device

    # 혹시 초기화가 안 되어 있다면 자동 가동
    if _model is None:
        init_yolo_model()

    imgsz = 320

    # 🛡️ [권한 충돌 해제] 폴더 자체를 지우지 말고, 출력 폴더가 없으면 생성만 해둠 (rmtree 지뢰 제거)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 비동기 단일 이미지 로더 구동
    dataset = LoadImages(image_path, img_size=imgsz)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(_names))]

    detected_objects = []

    # 더미 추론 (Warmup)
    img = torch.zeros((1, 3, imgsz, imgsz), device=_device)
    _ = _model(img.float()) if _device.type != 'cpu' else None

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(_device).float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = _model(img, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, multi_label=False)

        for i, det in enumerate(pred):
            p, im0 = (path, im0s)
            save_path = str(Path(output_dir) / Path(p).name)

            if det is not None and len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # 📝 [필승 방어선 검증용] XML 빌드 및 저장 트리거 바로 당기기
                build_and_save_xml(Path(output_dir), Path(p), save_path, det, _names, _food_map)

                for *xyxy, conf, cls in reversed(det):
                    current_name = _names[int(cls)]
                    if current_name == "00000000":
                        continue

                    # 최종 검출 종목 리스트 적립
                    detected_objects.append({
                        'name': current_name,
                        'conf': float(conf)
                    })

                    # 실시간 모바일 뷰어 매핑용 드로잉 박스 챡!
                    plot_one_box(xyxy, im0, label='%s %.2f' % (current_name, conf), color=colors[int(cls)])

                # 박스 그려진 실물 이미지 저장 업데이트
                cv2.imwrite(save_path, im0)

    # 🛡️ XML이 진짜 저장되었는지 2차 정밀 검증 후 Boolean 리턴
    file_basename = os.path.splitext(os.path.basename(image_path))[0]
    expected_xml = os.path.join(output_dir, f"{file_basename}.xml")

    if os.path.exists(expected_xml) and len(detected_objects) > 0:
        return True, detected_objects[0]['name']  # 첫 번째로 잡힌 주 음식을 토스
    else:
        return False, None


# 터미널 단독 실행용 호환성 뼈대 유지
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='../Fooddata/test', help='source')
    parser.add_argument('--output', type=str, default='../Yolo_output', help='output folder')
    opt = parser.parse_args()

    init_yolo_model()
    # 단독 테스트 폴더 내 이미지 순회 가동용
    if os.path.isdir(opt.source):
        for f in os.listdir(opt.source):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                run_yolo_detection(os.path.join(opt.source, f), opt.output)