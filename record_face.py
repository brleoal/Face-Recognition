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

import cv2
import os

def getDataset():
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')

    # For video capturing from video files, image sequences or camera
    cap = cv2.VideoCapture(0)

    # Create the Haar cascade
    cascpath = 'haarcascade_frontalface_default.xml'
    facecasc = cv2.CascadeClassifier(cascpath)

    for sampleNum in range(20):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(gray)
        # Detect face in the image
        faces = facecasc.detectMultiScale(cl1, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30,30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        for (x,y,w,h) in faces:
            imgfile = os.path.join('dataset', str(w)+str(h)+'_faces.jpg')
            cv2.imwrite(imgfile, cl1[y:y+h, x:x+w])
            # Draw a rectangle around the faces
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.waitKey(100)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.waitKey(1);
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
