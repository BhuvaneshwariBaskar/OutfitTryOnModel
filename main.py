import cvzone
import os
import cv2
from cvzone.PoseModule import PoseDetector

cap=cv2.VideoCapture("resources/Videos/1.mp4")
# cap=cv2.VideoCapture(0)

detector = PoseDetector()

shirtfolderpath="resources/Shirts"
listofshirts=os.listdir(shirtfolderpath)
fixedRatio=262/190  #shirtwidth/pointswidth
shirtRatioHeight=581/440


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img=cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)
    if lmList:
        # center = bboxInfo["center"]
        # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
        lm11 =lmList[11][0:2]
        lm12=lmList[12][0:2]
        # print(lmList)
        widthOfShirt=int((lm11[0]-lm12[0])*fixedRatio)
        print(widthOfShirt)
        imgShirt=cv2.imread(os.path.join(shirtfolderpath,listofshirts[0]),cv2.IMREAD_UNCHANGED)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeight)))
        try:
            img=cvzone.overlayPNG(img,imgShirt,lm12)
        except:
            pass
    cv2.imshow("Image",img)
    cv2.waitKey(1)

