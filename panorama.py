# imorting necessary libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
# taking images for stiching
#importing images from folder
images = []
path = 'C:\\aa\\iv_labs\\image_stiching'
p = os.path.join(path, "images")

for img in os.listdir(p):
    image = cv.imread(os.path.join(p, img))
    #cv.imshow('img',image)
    #cv.waitKey(0)
    images.append(image)
print(len(images))
#reference image
img1 = cv.imread('C:\\aa\\iv_labs\\image_stiching\\images\\img02.jpg')
#stiching image
img2 = cv.imread('C:\\aa\\iv_labs\\image_stiching\\images\\img03.jpg')

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
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
    pts1 = np.float32(pts1)
    pts2 = np.float32(pts2)
    return pts1,pts2,matches


status = 0
pts1, pts2, matches = keypoints(img1, img2)
if len(matches) <= 15:
    print("image pair is not suaitable for stiching")
    status = 1
    M = np.identity(3)
else:
    # find homography matrix between images :
    M , mask = cv.findHomography(pts2, pts1, cv.RANSAC, ransacReprojThreshold = 3)

#final width, height of stiched image
width = img1.shape[1] + img2.shape[1]
height = img1.shape[0] + img2.shape[0]
results = cv.warpPerspective(img2, M, (width,height))
print(results.shape)
#appending images 2 to first
results[0:img1.shape[0],0:img1.shape[1]] = img1
cv.imshow('img',results)
cv.waitKey(0)




'''
results = np.zeros(images[0].shape)

for i in range(len(images)-1):
    print(i)
    status = 0
    pts1, pts2, matches = keypoints(images[i], images[i+1])
    if len(matches) <= 15:
        print("image pair is not suaitable for stiching")
        status = 1
        M = np.identity(3)
    else:
        # find homography matrix between images :
        M , mask = cv.findHomography(pts2, pts1, cv.RANSAC, ransacReprojThreshold = 3)

    #final width, height of stiched image
    width = results.shape[1] + images[i+1].shape[1]
    height = results.shape[0] + images[i+1].shape[0]
    results = cv.warpPerspective(images[i+1], M, (width,height))
    #appending images 2 to first
    results[0:results.shape[0],0:results.shape[1]] = results
    cv.imshow('img',results)
    cv.waitKey(0)
'''
