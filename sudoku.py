import cv2
import numpy as np
import argparse
import pytesseract
from subprocess import run, PIPE
import time
start = time.time()
from threading import Thread
import math





#sort the corners to remap the image
def getOuterPoints(rcCorners):
    ar = [];
    ar.append(rcCorners[0,0,:])
    ar.append(rcCorners[1,0,:])
    ar.append(rcCorners[2,0,:])
    ar.append(rcCorners[3,0,:])
    
    x_sum = sum(rcCorners[x, 0, 0] for x in range(len(rcCorners)) ) / len(rcCorners)
    y_sum = sum(rcCorners[x, 0, 1] for x in range(len(rcCorners)) ) / len(rcCorners)
    
    def algo(v):
        return (math.atan2(v[0] - x_sum, v[1] - y_sum)
                + 2 * math.pi) % 2*math.pi
        ar.sort(key=algo)
    return (  ar[3], ar[0], ar[1], ar[2])
#################Threading###################################
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
def worker(lst):
    list = []
    for val in (lst):
        if is_sorta_black(val):
            text = tesseractIt(val)
            if text == '':
                list.append(0)
            else:
                list.append(int(text))
        else:
            list.append(0)
    return list
########################OCR####################################
def tesseractIt(img):
    config = ("-l digits --oem 1 --psm 6 -c tessedit_char_whitelist=0123456789")
    text = pytesseract.image_to_string(img, config=config)
    return text
#########################Largest rectangle###########################
def findLargestRect(img):
    image_sudoku_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(image_sudoku_gray,255,1,1,11,15)
    erode = cv2.erode(thresh,(np.ones((5,5),np.uint8)),iterations = 1)
    contours,hierarchy = cv2.findContours( thresh,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
    size_rectangle_max = 0; 
    for i in range(len(contours)):
        approximation = cv2.approxPolyDP(contours[i], 4, True)
        if(not (len (approximation)==4)):
            continue;
        if(not cv2.isContourConvex(approximation) ):
            continue; 
        size_rectangle = cv2.contourArea(approximation)
        if size_rectangle> size_rectangle_max:
            size_rectangle_max = size_rectangle 
            big_rectangle = approximation
    approximation = big_rectangle
    x,y,w,h = cv2.boundingRect(approximation)
    crop_img = img[y:y+h,x:x+w]
    return crop_img,approximation
#######################Check if black or white###################
def is_sorta_black(arr):
    if np.mean(arr)  > 240:
       return False
    else:
       return True
######################CROP Image
def cropImg(img):
    w = 0
    z = 55
    img_lst = []
    for i in range(1,10):
        x = 0
        y = 55
        for j in range(1,10):
            crop_img = img[w+4:z-4,x+10:y-10]
            x +=55
            y +=55
            img_lst.append(crop_img)
        w +=55
        z +=55
    return img_lst
##################Variables########################
dim = (495, 495)
img_lst = []
lst = []
##################Argument parser#################
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	help="path to input image")
args = vars(ap.parse_args())
##################Image Read#######################
img = cv2.imread(args['image'])
if img is None:
    print('Could not open or find the image:',args['image'])
    exit(0)
##################Image processing ###################
resized = cv2.resize(img, dim, interpolation = cv2.INTER_LANCZOS4)
largestRect,approximation = findLargestRect(resized)
resLargRect = cv2.resize(largestRect, dim, interpolation = cv2.INTER_LANCZOS4)
gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
rgb = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
lst = cropImg(resLargRect)
points1 = np.array([
                    np.array([0.0,0.0] ,np.float32) + np.array([496,0], np.float32),
                    np.array([0.0,0.0] ,np.float32),
                    np.array([0.0,0.0] ,np.float32) + np.array([0.0,496], np.float32),
                    np.array([0.0,0.0] ,np.float32) + np.array([496,496], np.float32),
                    ],np.float32) 
outerPoints = getOuterPoints(approximation)
points2 = np.array(outerPoints,np.float32)
pers = cv2.getPerspectiveTransform(points2,  points1 )
warp = cv2.warpPerspective(resized, pers, (496, 496))
warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
ret,thresh =  cv2.threshold(warp_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# cv2.imshow('thr',thresh)
# cv2.imshow('warp_gray',warp_gray)
lst = cropImg(thresh)
Half1 = ThreadWithReturnValue(target=worker, args=(lst[0:9],))
Half2 = ThreadWithReturnValue(target=worker, args=(lst[9:18],))
Half3 = ThreadWithReturnValue(target=worker, args=(lst[18:27],))
Half4 = ThreadWithReturnValue(target=worker, args=(lst[27:36],))
Half5 = ThreadWithReturnValue(target=worker, args=(lst[36:45],))
Half6 = ThreadWithReturnValue(target=worker, args=(lst[45:54],))
Half7 = ThreadWithReturnValue(target=worker, args=(lst[54:63],))
Half8 = ThreadWithReturnValue(target=worker, args=(lst[63:72],))
Half9 = ThreadWithReturnValue(target=worker, args=(lst[72:81],))
Listes = []
Half1.start()
Half2.start()
Half3.start()
Half4.start()
Half5.start()
Half6.start()
Half7.start()
Half8.start()
Half9.start()
Listes += Half1.join()
Listes += Half2.join()
Listes += Half3.join()
Listes += Half4.join()
Listes += Half5.join()
Listes += Half6.join()
Listes += Half7.join()
Listes += Half8.join()
Listes += Half9.join()
a = " ".join(str(x) for x in Listes)
p = run(['Sudoku.exe'], stdout=PIPE,input=a, encoding='ascii')  
print(p.stdout)
# cv2.imshow("rgb",rgb)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
end = time.time()
print(end - start)
