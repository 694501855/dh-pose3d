import os

from fastapi import FastAPI, Body
from cvzone.PoseModule import PoseDetector
from PIL import  Image
from modules.api.models import *
from modules.api import api
import cv2
import numpy as np

from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
def pose_api(_, app: FastAPI):
    @app.get("/pose3d/version")
    async def version():
        return {"version": "0.0.0.1"}

    @app.post("/pose3d/img_to_pose3d")
    async def img_to_pose3d(input_image: str = Body("", title='input_image'), is_return_image:bool=Body(True, title='is_return_image')):
        temp = os.path.join(os.getenv("TEMP"), "DH")
        img0 =np.array(api.decode_base64_to_image(input_image)).astype('uint8')
        img_cv = cv2.cvtColor(img0, cv2.COLOR_RGB2BGR)
        #cv2.imwrite(os.path.join(temp, "img_cv.png"), img_cv)  # 保存文件

        img_pose = detector.findPose(img_cv)
        #cv2.imwrite(os.path.join(temp, "img_pose.png"), img_pose)  # 保存文件

        lmList, bboxInfo = detector.findPosition(img_pose)
        newList = []
        if bboxInfo:
            for lm in lmList :
                lm[2]=img_pose.shape[0] - lm[2]
                newList.append([lm[1], lm[2], lm[3]])
        if is_return_image :
            img = cv2.cvtColor(img_pose, cv2.COLOR_BGR2RGB)
            rimg=api.encode_pil_to_base64(Image.fromarray(img))
            return {"lmList": newList, "bboxInfo": bboxInfo,"image":rimg}
        return {"lmList": newList, "bboxInfo": bboxInfo}

    @app.post("/pose3d/video_to_pose3d")
    async def video_to_pose3d(input_video: str = Body("", title='123'), type:int=Body(0, title='123')):
        cap = cv2.VideoCapture(input_video)
        detector_video = PoseDetector()
        success = True
        posList = []
        while success:
            success, img = cap.read()
            if success:
                img = detector_video.findPose(img)
                lmList, bboxInfo = detector_video.findPosition(img)
                if bboxInfo:
                    newList=[]
                    for lm in lmList:
                        lm[2] = img.shape[0] - lm[2]
                        newList.append([lm[1], lm[2], lm[3]])
                    posList.append(newList)
        return {"pose_anim_list": posList}

    @app.post("/pose3d/video_to_pose3d_txt")
    async def video_to_pose3d_txt(input_video):
        cap = cv2.VideoCapture(input_video)
        detector_video = PoseDetector()
        success = True
        posListText = []
        while success:
            success, img = cap.read()
            if success:
                img = detector_video.findPose(img)
                lmList, bboxInfo = detector_video.findPosition(img)
                if bboxInfo:
                    newList=[]
                    lmString = ''
                    for lm in lmList:
                        lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
                    posListText.append(lmList)
        temp = os.path.join(os.getenv("TEMP"), "DH")
        fiel=os.path.join(temp, "video_to_pose3d_txt.txt")
        with open(fiel, 'w') as f:
            f.writelines(["%s\n" % item for item in posListText])
        return fiel

import logging
logger = logging.getLogger(__name__)

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(pose_api)
    logger.debug("pose_api API 加载")
except:
    pass

