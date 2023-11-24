import cvzone
import os
import cv2
from cvzone.PoseModule import PoseDetector

# cap=cv2.VideoCapture("resources/Videos/1.mp4")
cap=cv2.VideoCapture(0)

detector = PoseDetector()

shirtfolderpath="resources/Shirts"
listofshirts=os.listdir(shirtfolderpath)
fixedRatio=262/190
shirtRatioHeight=581/440
imageNumber=0
imgButtonRight=cv2.imread("resources/button.png",cv2.IMREAD_UNCHANGED)
imgButtonLeft=cv2.flip(imgButtonRight,1)
counterRight=0
counterLeft=0
selectionSpeed=10


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
        imgShirt=cv2.imread(os.path.join(shirtfolderpath,listofshirts[imageNumber]),cv2.IMREAD_UNCHANGED)

        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeight)))
        currentScale=(lm11[0]-lm12[0])/190
        offset=int(44*currentScale),int(48*currentScale)
        try:
            img=cvzone.overlayPNG(img,imgShirt,(lm12[0]-offset[0],lm12[1]-offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img,imgButtonLeft,(72,293))

        if lmList[16][1]<300:
            counterRight+=1
            cv2.ellipse(img,(139,360),(66,66),0,0,counterRight*selectionSpeed,(0,255,0),28)

            if counterRight*selectionSpeed>360:
                counterRight=0
                if imageNumber<len(listofshirts)-1:
                    imageNumber+=1

        elif lmList[15][1]>900:
            counterRight-=1
            cv2.ellipse(img,(1138,360),(66,66),0,0,counterRight*selectionSpeed,(0,255,0),28)

            if counterRight*selectionSpeed>360:
                counterLeft=0
                if imageNumber>0:
                    imageNumber-=1

        else:
            counterRight=0
            counterLeft=0
    cv2.imshow('Try On', img)
    cv2.waitKey(1)

