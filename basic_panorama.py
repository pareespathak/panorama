# importing necessary libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
# taking two images for stiching
#importing images from folder
#reference image
#img1 = cv.imread('C:\\aa\\iv_labs\\image_stiching\\images\\img02.jpg')
img1 = cv.imread('panorama\\images\\img02.jpg')
img2 = cv.imread('panorama\\images\\img03.jpg')
#stiching image
#img2 = cv.imread('C:\\aa\\iv_labs\\image_stiching\\images\\img03.jpg')

#detecting key points and finding correspondence
def keypoints(img1,img2):
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # FLANN parameters
    # FINDING INDEX PARAMETERS FOR FLANN OPERATORS
    des1 = np.float32(des1)
    des2 = np.float32(des2)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    pts1 = []
    pts2 = []
    # ratio test as per Lowe's paper for best matches
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
    pts1 = np.float32(pts1)
    pts2 = np.float32(pts2)
    return pts1,pts2,matches

#find correspondence
pts1, pts2, matches = keypoints(img1, img2)
#threshold num of correspondence obtain
if len(matches) <= 15:
    print("image pair is not suaitable for stiching")
    #M = np.identity(3) # no homography generated
else:
    # find homography matrix between images :
    M , mask = cv.findHomography(pts2, pts1, cv.RANSAC, ransacReprojThreshold = 3)
    #final width, height of stiched image
    width = img1.shape[1] + img2.shape[1]
    height = img1.shape[0] + img2.shape[0]
    results = cv.warpPerspective(img2, M, (width,height))
    #print(results.shape)
    #appending images 2 to first
    results[0:img1.shape[0],0:img1.shape[1]] = img1
cv.imshow('img',results)
#cv.imwrite('results1.jpg',results)     #for saving image
cv.waitKey(0)
