import torch
import cv2
import os
from PIL import Image
from detect_video import Detector

detector = Detector("param/p_net.pth", "param/r_net.pth", "param/o_net.pth")
video_path = r"detect_video/test01.mp4"

# 读取视频
cap = cv2.VideoCapture(video_path)
# get size and fps of video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 帧播放速率
fps = cap.get(cv2.CAP_PROP_FPS)
# VideoWriter_fourcc为视频编解码器
# cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),该参数是Flash视频，文件名后缀为.flv
#cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'),该参数是MPEG-1编码类型，文件名后缀为.avi
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')

# create VideoWriter for saving
outVideo = cv2.VideoWriter('out_video/save_video.avi', fourcc, fps, (width, height))

c = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        timeF = 1  # 每一帧检测一次
        if c % timeF == 0:
            img = frame[..., ::-1]
            img = Image.fromarray(img)
            onet_boxes = detector.detect(img)
            if onet_boxes is not None:
                for box in onet_boxes:
                    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
                    for i in range(5, 15, 2):
                        cv2.circle(frame, (int(box[i]), int(box[i + 1])), radius=1, color=(255, 255, 0), thickness=-1)
        c += 1
        # 将处理后的图片存入输出视频
        outVideo.write(frame)

        cv2.imshow('video', frame)
        c = cv2.waitKey(1)
        # 27表示Esc键
        if c == 27:
            break
    else:
        print("视频播放结束")
        break
cap.release()
cv2.destroyAllWindows()