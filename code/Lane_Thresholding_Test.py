import cv2
import numpy as np


# def nothing(a):
#     pass

# def initializeTrackbars(intialTracbarVals,wT=420,hT=240):
#     cv2.namedWindow("Trackbars")
#     cv2.resizeWindow("Trackbars",420, 240)
#     cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
#     cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
#     cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
#     cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)

# def valTrackbars(wT=640, hT=480):
#     widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
#     heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
#     widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
#     heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
#     points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
#                       (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
#     return points

# intialTracbarVals = [110,208,0,480]
# #intialTracbarVals = [110,208,255,255]
# initializeTrackbars(intialTracbarVals)

# points = valTrackbars()



# def drawPoints(img,points):
#     for x in range(0,4):
#         #drawed = cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
#         drawed = cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(255,255,255),cv2.FILLED)
#         cv2.imshow("points", drawed)
#     return img


def getLaneCurve(img):
    imgThres = thresholding(img)
    cv2.imshow("mask", imgThres)
    return imgThres


def thresholding(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([90, 0, 156])
    upperWhite = np.array([179, 255, 255])
    maskedWhite= cv2.inRange(hsv,lowerWhite,upperWhite)
    return maskedWhite


def getHistogram(img,minPer=0.1,display= True,region=1):
 
    if region ==1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    if display == True:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            middle = cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
            cv2.imshow("middle", middle)
        return basePoint,imgHist
 
    return basePoint


if __name__ == '__main__':
    cap = cv2.VideoCapture(r"C:\Users\HNE2COB\Downloads\20230810_204144.mp4")
    while True:
        _, img = cap.read() # GET THE IMAGE
        img = cv2.resize(img,(640,480)) # RESIZE
        imgThres = getLaneCurve(img)
        getHistogram(imgThres)
        cv2.waitKey(1)