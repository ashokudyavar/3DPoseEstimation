import numpy as np
import cv2
import pickle
img = cv2.imread('real.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
cv2.imshow("before",img)
cv2.waitKey(0)
features = np.zeros(img.shape)
dst = cv2.cornerHarris(img,2,3,0.04)
features[dst>0.01*dst.max()]=255
featurePoints =np.transpose(np.nonzero(features))
featurePoints = np.array(featurePoints)
cv2.imshow("features",features)
cv2.waitKey(0)
from sklearn.cluster import MeanShift, estimate_bandwidth
bandwidth = estimate_bandwidth(featurePoints, quantile=0.2, n_samples=featurePoints.shape[0])
ms = MeanShift(bandwidth=4, bin_seeding=True)
ms.fit(featurePoints)
labels = ms.labels_
cluster_centers = ms.cluster_centers_
cluster_centers = cluster_centers.astype(int)
features = np.zeros(img.shape)
for i in range(cluster_centers.shape[0]):
    features[cluster_centers[i,0],cluster_centers[i,1]] = 1
    cv2.circle(img, (cluster_centers[i,1],cluster_centers[i,0]), radius=3, color=(0, 0, 255), thickness=-1)
cv2.imshow("img",img)
cv2.waitKey(0)
print(cluster_centers.shape)
temp =[]
for i in range(cluster_centers.shape[0]):
    temp.append((cluster_centers[i,1],cluster_centers[i,0]))


steps =10
keyPoints2d = np.array(temp)
mean2dPoints = keyPoints2d.mean(axis=0)
meanShiftedPoints = keyPoints2d - mean2dPoints
ys = meanShiftedPoints[:,0]
xs = meanShiftedPoints[:,1]
theta = np.arctan2(ys,xs)
bins = (theta/np.pi) *(steps/2) +(steps/2)
bins = np.rint(bins).astype(int)
dists = np.linalg.norm(meanShiftedPoints,axis=1)
normDists = dists/np.max(dists)
# sort --------------------
sortOrder = np.argsort(theta[np.argsort(dists)])
keyPoints2d =keyPoints2d[sortOrder ]
meanShiftedPoints =meanShiftedPoints[sortOrder ]
theta =theta[sortOrder ]
bins =bins[sortOrder ]
dists =dists[sortOrder ]
normDists =normDists[sortOrder ]
dumpList = [keyPoints2d, meanShiftedPoints,bins,normDists]

with open('image.pickle', 'wb') as b:
    pickle.dump(dumpList,b)