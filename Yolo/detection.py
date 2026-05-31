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

from xml_utils import load_food_name_map, build_and_save_xml

import numpy as np
import platform as pf
import psutil
import PIL
import pandas as pd
import seaborn as sns

ONNX_EXPORT = False

def ToF(file, cat):
    return "T"

def detect(save_img=False):
    imgsz = (320, 192) if ONNX_EXPORT else opt.img_size
    out, source, weights, half, view_img, save_txt, save_xml = opt.output, opt.source, opt.weights, opt.half, opt.view_img, opt.save_txt, opt.save_xml
    webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

    food_map = load_food_name_map()

    import utils.torch_utils as torch_utils
    device = torch_utils.select_device(device='cpu' if ONNX_EXPORT else opt.device)

    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)

    model = Darknet(opt.cfg, imgsz)

    attempt_download(weights)
    if weights.endswith('.pt'):
        model.load_state_dict(torch.load(weights, map_location=device)['model'], strict=False)
    else:
        load_darknet_weights(model, weights)

    model.to(device).eval()

    half = half and device.type != 'cpu'
    if half:
        model.half()

    if webcam:
        view_img = True
        torch.backends.cudnn.benchmark = True
        dataset = LoadStreams(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    names = load_classes(opt.names)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    rslt = []
    nT, nF, nN, nND = 0, 0, 0, 0

    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)
    _ = model(img.half() if half else img.float()) if device.type != 'cpu' else None

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        t1 = torch_utils.time_synchronized()
        pred = model(img, augment=opt.augment)[0]
        t2 = torch_utils.time_synchronized()

        if half:
            pred = pred.float()

        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres,
                                   multi_label=False, classes=opt.classes, agnostic=opt.agnostic_nms)

        for i, det in enumerate(pred):
            p, s, im0 = (path[i], '%g: ' % i, im0s[i].copy()) if webcam else (path, '', im0s)

            save_path = str(Path(out) / Path(p).name)
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

            if det is not None and len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += '%g %s, ' % (n, names[int(c)])

                if save_xml:
                    build_and_save_xml(Path(out), Path(p), save_path, det, names, food_map)

                for *xyxy, conf, cls in reversed(det):
                    current_name = names[int(cls)]
                    label = '%s %.2f' % (current_name, conf)

                    if current_name == "00000000":
                        continue

                    if save_txt:
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                        with open(save_path[:save_path.rfind('.')] + '.txt', 'a') as file:
                            file.write(('%g ' * 5 + '\n') % (cls, *xywh))

                    if save_img or view_img:
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)])

                    rslt.append('{0},{1},{2}'.format(Path(p), current_name, ToF(Path(p), current_name)))
                    nT += 1

            print('%s (%.3fs)' % (s, t2 - t1))

            if view_img:
                cv2.imshow(p, im0)
                if cv2.waitKey(1) == ord('q'):
                    raise StopIteration

    if save_txt or save_img:
        print('Results saved to %s' % os.getcwd() + os.sep + out)

    print('Done. (%.3fs)' % (time.time() - t0))

    tot = nT + nF + nND
    if tot == 0:
        print("Number of Detected Objects: 0, Accuracy: 0.0 (No objects detected)")
    else:
        accu = nT / tot
        print('Number of Detected Objects: {0}, True: {1}, False: {2}, Not Detected: {3}, Accuracy: {4}'.format(tot, nT, nF, nND, accu))

    with open('./classificaion_result.txt', 'w') as f:
        rslt = [r + '\n' for r in rslt]
        f.writelines(rslt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--cfg', type=str, default='yolov3-spp-403cls.cfg', help='*.cfg path')
    parser.add_argument('--names', type=str, default='403food.names', help='*.names path')
    parser.add_argument('--weights', type=str, default='best_403food_e200b150v2.pt', help='weights path')
    parser.add_argument('--source', type=str, default='../Fooddata/Images', help='source')
    parser.add_argument('--output', type=str, default='../Yolo_output', help='output folder')
    parser.add_argument('--device', default='cpu', help='device id (i.e. 0 or 0,1) or cpu')
    parser.add_argument('--save-xml', action='store_true', default=True, help='save results to *.xml')

    parser.add_argument('--img-size', type=int, default=320, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.15, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec')
    parser.add_argument('--half', action='store_true', help='half precision FP16 inference')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')

    opt = parser.parse_args()

    opt.cfg = check_file(opt.cfg)
    opt.names = check_file(opt.names)

    with torch.no_grad():
        print('Session START :', time.strftime('%Y-%m-%d %Z %H:%M:%S', time.localtime(time.time())))
        print('===============================================================')

        def printOsInfo():
            try:
                print('GPU                  :\t', torch.cuda.get_device_name(0))
            except:
                print('GPU                  :\t None (Using CPU Mode)')
            print('OS                   :\t', pf.system())

        printOsInfo()

        def printSystemInfor():
            print('Process information  :\t', pf.processor())
            print('Process Architecture :\t', pf.machine())
            print('RAM Size             :\t', str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + "(GB)")
            print('===============================================================')

        printSystemInfor()
        detect()