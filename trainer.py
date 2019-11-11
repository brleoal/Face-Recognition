""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import shutil
import cv2
import numpy as np
import manage_database as db

def getImagesWithID(ID, path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = cv2.imread(imagePath)
        gray = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(gray)
        faces.append(cl1)
        IDs.append(ID)
        cv2.imshow('training',cl1)
        cv2.waitKey(10)
    return np.array(IDs), faces

def trainDataset(ID, username, passwd, photo):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataset'
    if not os.path.exists('./recognizer'):
        os.makedirs('./recognizer')    
    Ids, faces = getImagesWithID(ID, path)
    recognizer.train(faces,Ids)
    recogpath = os.path.join('recognizer','trainingData.yml')
    recognizer.save(recogpath)
    db.insertData(ID, username, passwd, photo, recogpath)
    shutil.rmtree('recognizer')
    shutil.rmtree('dataset')
    cv2.destroyAllWindows()
