import numpy as np
import cv2 as cv2
import os
import pickle

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_3d_to_2d(model_pts, params):
    extrinsic_camera_matrix =  pt2render.ex_camera_matrix(params[0], params[1], params[2], params[3])
    camera_matrix = pt2render.get_camera_matrix(variables.INTRINSIC_CAMERA_MATRIX,extrinsic_camera_matrix,
                                      variables.WORLD_MATRIX)
    #render
    pt_array = pt2render.get_render_location(model_pts,camera_matrix)
    
    return pt_array


with open('2.pickle', 'rb') as file:
    [templateKeyPoints3d ,templateKeyPoints2d, templateMeanShiftedPoints,templateBins,templateNormDists] = pickle.load(file)
    file.close()

with open('image.pickle', 'rb') as file:
    [imageKeyPoints2d, imageMeanShiftedPoints,imageBins,imageNormDists] = pickle.load(file)
    file.close()

def binnify(k3d,k2d,steps=10):
    print("inside binnify")
    keyPoints3d =k3d
    keyPoints2d = np.array(k2d)
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
    keyPoints3d =keyPoints3d[sortOrder ]
    keyPoints2d =keyPoints2d[sortOrder ]
    meanShiftedPoints =meanShiftedPoints[sortOrder ]
    theta =theta[sortOrder ]
    bins =bins[sortOrder ]
    dists =dists[sortOrder ]
    normDists =normDists[sortOrder ]
    dumpList = [keyPoints3d ,keyPoints2d, meanShiftedPoints,bins,normDists]
    return dumpList

keypoints2d =[]
keypoints3d =[]
uniqueBins = np.unique(imageBins)
count = 0
templateImagePath =os.path.join("images6" ,"2.png")
imagePath ='real.png'
templateImage = cv2.imread(templateImagePath)
image = cv2.imread(imagePath)
image1 = image.copy()
image2 = image.copy()
templateImage1 = templateImage.copy()
for imageKeyPoint in imageKeyPoints2d:
    imageBin = imageBins[count]
    imageDist = imageNormDists[count]
    possibeIndices = np.where(templateBins == imageBin)
    if(len(possibeIndices[0]) >0):
        possibeTargetKeypoints2d = templateKeyPoints2d[possibeIndices]
        possibeTargetKeypoints3d = templateKeyPoints3d[possibeIndices]
        possibeTargetNormDistances = templateNormDists[possibeIndices]
        closestIndex = find_nearest(possibeTargetNormDistances,imageDist)
        keypoints2d.append(imageKeyPoint)
        keypoints3d.append(possibeTargetKeypoints3d[closestIndex])
        cv2.circle(image, (imageKeyPoint[0],imageKeyPoint[1]), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.circle(templateImage, (int((960/300)*float(possibeTargetKeypoints2d[closestIndex][0])), int((540/160)*float(possibeTargetKeypoints2d[closestIndex][1])) ), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.imshow("image",image)
        cv2.imshow("templateImage",templateImage)
        cv2.waitKey(0)
        print(imageDist ,possibeTargetNormDistances[closestIndex])
    count = count + 1

points_3D = np.array(keypoints3d).astype(np.double)
points_2D = np.array(keypoints2d).astype(np.double)
dist_coeffs = np.zeros((4,1),dtype="double")
INTRINSIC_CAMERA_MATRIX = np.array([ [328.1250,    0,  150],
                                      [ 0, 326.67,  84],
                                      [0,    0,    1] ],dtype="double")
success, rotation_vector, translation_vector,inliers = cv2.solvePnPRansac(points_3D, points_2D, INTRINSIC_CAMERA_MATRIX, dist_coeffs, flags=0)
projectedPoints, jacobian = cv2.projectPoints(points_3D, rotation_vector, translation_vector, INTRINSIC_CAMERA_MATRIX, dist_coeffs)
#projectedPoints = np.reshape(1,-1,2)
projectedPoints = np.squeeze(projectedPoints)
projectedPoints = projectedPoints.astype(int)
#    extra
projectedPointsActual, jacobian = cv2.projectPoints(templateKeyPoints3d, rotation_vector, translation_vector, INTRINSIC_CAMERA_MATRIX, dist_coeffs)
projectedPointsActual = np.squeeze(projectedPointsActual)
projectedPointsActual = projectedPointsActual.astype(int)
steps = 10
dumpList = binnify(templateKeyPoints3d,projectedPointsActual,steps)
dumpList.append(rotation_vector)
dumpList.append(translation_vector)
with open('iter1'+'.pickle', 'wb') as b:
    pickle.dump(dumpList,b)
#    extra

for projectPoint in projectedPoints:
    cv2.circle(image1, (projectPoint[0],projectPoint[1]), radius=3, color=(0, 0, 255), thickness=-1)
cv2.imshow("image1",image1)
cv2.waitKey(0)
print(projectedPoints.shape)
print(success)
noProjectedPoints = projectedPoints.shape[0]
projectedPoints = projectedPoints.astype(np.double)
projectionError = np.sum(np.linalg.norm(points_2D -projectedPoints,axis=1))
print(projectionError/noProjectedPoints)
print(np.squeeze(inliers))
print(inliers.shape)
inliers = np.squeeze(inliers)
projectionErrorInliers = np.sum(np.linalg.norm(points_2D[inliers] -projectedPoints[inliers],axis=1))
print('projectionErrorInliers',projectionErrorInliers/inliers.shape)

with open('keypoints.pickle', 'rb') as file:
    keypoints = pickle.load(file)
    projectedPoints, jacobian = cv2.projectPoints(keypoints, rotation_vector, translation_vector, INTRINSIC_CAMERA_MATRIX, dist_coeffs)
    projectedPoints = np.squeeze(projectedPoints)
    projectedPoints = projectedPoints.astype(int)
    for projectPoint in projectedPoints:
        cv2.circle(image2, (projectPoint[0],projectPoint[1]), radius=3, color=(0, 0, 255), thickness=-1)
    cv2.imshow("ransac",image2)
    cv2.waitKey(0)
    cv2.imwrite("ransac.png",image2)
    file.close()


