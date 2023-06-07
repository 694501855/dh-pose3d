import cv2
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture('scripts/002.mp4')

detector = PoseDetector()
posList = []
success = True
while success:
    success, img = cap.read()
    if success:
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img)

        if bboxInfo:
            lmString = ''
            for lm in lmList:
                lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
            posList.append(lmString)

        print(len(posList))

        cv2.imshow("Image", img)
    #key = cv2.waitKey(1)
    #if key == ord('s'):
with open("MotionFile.txt", 'w') as f:
    f.writelines(["%s\n" % item for item in posList])




        #cv2.imshow("Image", img)
        #img=Image.fromarray(img0)
        #img.save("D:\\mm.png")

        #img = cv2.imread("D:\\mm.png")

        #img = cv2.cvtColor(img , cv2.COLOR_RGB2RGB)

        #cap = cv2.VideoCapture('./002.mp4')
        #success, img2 = cap.read()



        #Image.fromarray(img).save("D:\\mm2.png")
        #cv2.imshow("Image", img)