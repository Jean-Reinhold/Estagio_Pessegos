import os
import cv2
import numpy as np
import random as rng
from src.utils.rectangle import Rectangle
rng.seed(12345)

MAJOR_THRESH = 50
SUB_THRESH = 15
FIRST_PROPORTION = 10
SECOND_PROPORTION = 5
LOW_H = 0
LOW_S = 50
LOW_V = 50
HIGH_H = 39
HIGH_S = 200
HIGH_V = 150

class Segmentation:
    def __init__(self, image_path, path = '', filter_num=3):
        self.image = cv2.imread(image_path)
        self.path = path
        self.filter_num = filter_num

    def get_contours(self, image, thresh):
        canny_output = cv2.Canny(image, thresh, 2*thresh)
        _, self.contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def process_big(self):
        src = cv2.resize(self.image, None, fx=(FIRST_PROPORTION**-1), fy=(FIRST_PROPORTION**-1))
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        for i in range(self.filter_num):
            src_gray = cv2.blur(src_gray, (3, 3))
        for i in range(3):
            src_gray = cv2.medianBlur(src_gray, 5)
        self.framed = self.big_thresh_callback(src_gray)

    def process_sub(self):
        src = cv2.resize(self.framed, None, fx=(SECOND_PROPORTION**-1), fy=(SECOND_PROPORTION**-1))
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src_gray = cv2.blur(src_gray, (3, 3))
        self.sub_thresh_callback(src_gray)

    def _rect(self, contour):
         self.rect = Rectangle(np.array(np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))))

    def sub_thresh_callback(self, src_gray):
        counter = 0
        self.get_contours(src_gray, SUB_THRESH)
        for index, contour in enumerate(self.contours):
            self._rect(contour)
            if self.rect.dimension_limits():
                if counter == 0:
                    if abs(self.rect.sin) < 0.2:
                        counter += 1
                        old = self.def_olds(index)
                elif self.rect.dist_box(old) > 4 and abs(self.rect.sin) < 0.2:
                    old = self.def_olds(index)

    def def_olds(self, iterator):
        path = '{}/{}.jpg'.format(self.path, len(os.listdir(self.path)))
        self.save_sub(path, self.rect.points)
        return self.rect.points

    def max_area(self):
        max_area = 0
        minRect = [None] * len(self.contours)
        points = np.zeros((4,2))
        self.rect = Rectangle(np.array(np.intp(points)))        
        for index, contour in enumerate(self.contours):
            minRect[index] = cv2.minAreaRect(contour)
            box = cv2.boxPoints(minRect[index])
            area = cv2.contourArea(box)
            if area > max_area:
                max_area = area
                self.rect = Rectangle(np.array(np.intp(box)))
                points = self.rect.points
        return points

    def big_thresh_callback(self, img):
        self.get_contours(img, MAJOR_THRESH)
        points = self.max_area()
        pts1 = np.float32([points[0], points[1], points[3], points[2]])
        pts1 = FIRST_PROPORTION * pts1
        pts2 = np.float32([[0, 0], [1680, 0], [0, 3300], [1680, 3300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(self.image, M, (1680, 3300))
        return dst

    def save_sub(self, path, points):
        pts1 = np.float32([points[0], points[1], points[3], points[2]])
        pts1 = SECOND_PROPORTION * pts1
        pts2 = np.float32([[0, 0], [150, 0], [0, 300], [150, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(self.framed, M, (150, 300))
        cv2.imwrite(path, dst)

    def mask_filter(self):
        src_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        HSV_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        low_limit = np.array([LOW_H, LOW_S, LOW_V], np.uint8)
        high_limit = np.array([HIGH_H, HIGH_S, HIGH_V], np.uint8)
        mask = cv2.inRange(HSV_img, low_limit, high_limit)
        return mask

    def measuring(self):
        mask = self.mask_filter()
        for i in range(10):
            mask = cv2.medianBlur(mask, 5)
        mask = cv2.copyMakeBorder(mask, 5, 5, 5, 5, cv2.BORDER_CONSTANT, (0, 0, 0))
        self.get_contours(mask, MAJOR_THRESH)
        _ = self.max_area()

def remove_files(path):
    for filename in os.listdir(path):
        os.remove('{0}/{1}'.format(path, filename))

def segmentation(image_path, path, filter_num):
    seg = Segmentation(image_path, path, filter_num)
    filtered = seg.process_big()
    seg.process_sub()

def full_process(image_path, processed_path, identification):
    filter_num = 3
    while(len(os.listdir(processed_path))<95*identification and filter_num<10):
        segmentation(image_path, processed_path, filter_num)
        filter_num += 1
    return True if filter_num == 10 else False

def remove_emptyness(path):
    empty=0
    for filename in os.listdir(path.image_processed):
        width, height = measure(Segmentation('{0}/{1}'.format(path.image_processed, filename)))
        if width<1.5 and height<1.5:
            empty+=1
            os.remove('{0}/{1}'.format(path.image_processed, filename))
    return empty
def measure(seg):
    seg.measuring()
    return (7.9/150)*seg.rect.width, (7.9/150)*seg.rect.height

def size_analysis(x, y, z):
    if x < 3.0 or y < 3 or z < 3:
        return 0
    else:
        if x >= 4.75 and y >= 4.75 and z >= 4.75:
            return 12
        else:
            if x >= 4.5 and y >= 4.5 and z >= 4.5:
                return 11
            else:
                if x >= 4.25 and y >= 4.25 and z >= 4.25:
                    return 10
                else:
                    return 9


