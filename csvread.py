import csv
import cv2
import math
import os
import numpy as np
import variables
import numpy as np
import csv
import pt2render
import pickle

paramsArray = [ [0.0,0.0,0.0,2] ,[90,0,0,2] , [180,0,0,2] , [270,0,0,2] ]

lines_count = len(open("keypoints4.csv").readlines())
noPoses = 4 
noElements, noPoses =  lines_count ,4
visibleMatrix = [[0 for x in range( noPoses )] for y in range(noElements)] 
keypoints = [[0 for x in range( 3 )] for y in range(noElements)] 
with open('keypoints3.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lenCount =0
    for row in csv_reader:
        if len(row) == 0 :
            continue
        else:
            keypoints[ lenCount ][0] = float(row[0])
            keypoints[ lenCount ][1] = float(row[1])
            keypoints[ lenCount ][2] = float(row[2])
            lenCount = lenCount + 1
    csv_file.close()
keypoints = np.array(keypoints)
with open('keypoints.pickle', 'wb') as b:
    pickle.dump(keypoints,b)


steps = 10
lenCount =0
for pose in range(0,noPoses):
    image = cv2.imread(os.path.join("images6" ,str(pose)+".png"))
    centerX = 0
    centerY = 0
    k3d =[]
    k2d = []
    with open(str(pose) + '.csv') as csv_file:
        csv_reader1 = csv.reader(csv_file, delimiter=',')
        lenCount = 0
        for row in csv_reader1:
            if len(row) == 0 :
                continue
            visible = int(row[6])
            temp3d =[]
            temp2d=[]
            if visible == 1 :
                temp3d =[float(row[1]) , float(row[2]), float(row[3]) ]
                temp2d =[int( (300/960)*float(row[4])) , int( (160/540)*float(row[5]))  ]
                k3d.append(temp3d)
                k2d.append(temp2d)
        keyPoints3d = np.array(k3d)
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
        #------------------------------
        #verify
        for i in range(0,steps):
            binIndices = np.where( bins == i)
            for binIndex in binIndices[0]:
                #print(keyPoints2d[thetaIndex,0],keyPoints2d[thetaIndex,1])
                cv2.circle(image, (keyPoints2d[binIndex,0],keyPoints2d[binIndex,1]), radius=3, color=(0, 0, 255), thickness=-1)
            #cv2.imshow("image",image)
            #cv2.waitKey(0)
        csv_file.close()
        with open(str(pose)+'.pickle', 'wb') as b:
            pickle.dump(dumpList,b)

with open('0.pickle', 'rb') as file:
    [a,b,c,d,e] = pickle.load(file)
    print(type(d))
    print(b.shape)

    #cv2.imshow("image",image)
    #cv2.imwrite(str(pose)+'.png',image)
    #cv2.waitKey(0)
###############################################

####################################################
#print(thetaMatrix)
# finalMatrix = [ ]
# index =0
# image = cv2.imread("images6/0.png")
# for poses in visibleMatrix :
    # if sum(poses) !=0 :
        # finalMatrix.append( [ keypoints[index][0] , keypoints[index][1] , keypoints[index][2] ] + visibleMatrix[index] + thetaMatrix [index] )
        # if (visibleMatrix[index][1] == 1):
            # key_3d1 = np.array([ [ keypoints[index][0] , keypoints[index][1] , keypoints[index][2]  ]]) # backdoorbottomleft
            # params = paramsArray[0]
            # key_2d = get_3d_to_2d(key_3d1, params).astype(int)
            # cv2.circle(image, (int(key_2d[0]),int(key_2d[1])), radius=3, color=(0, 0, 255), thickness=-1)
    # index = index + 1
# cv2.imshow("image",image)
# cv2.waitKey(0)

#verify

# image = cv2.imread("images6/0.png")

# for all in finalMatrix:
    # key_3d1 = np.array([ [ all[0] , all[1] , all[2] ]]) # backdoorbottomleft
    # params = paramsArray[0]
    # if (all[3] == 1):
        # params = paramsArray[0]
        # key_2d = get_3d_to_2d(key_3d1, params).astype(int)
        # cv2.circle(image, (int(key_2d[0]),int(key_2d[1])), radius=3, color=(0, 0, 255), thickness=-1)
# cv2.imshow("image",image)
# cv2.waitKey(0)



