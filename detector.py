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
import manage_database as db

def faceRecognizer(username, password):
    try:
        record = db.getData(username, password)
        if record is not None:
            fname = record[4]
            if not os.path.exists('./recognizer'):
                os.makedirs('./recognizer')    
            recogpath = os.path.join('recognizer','trainingData.yml')
            with open(recogpath, 'wb') as f:
                f.write(fname)
            cascpath = 'haarcascade_frontalface_default.xml'
            facecasc = cv2.CascadeClassifier(cascpath)
            cap = cv2.VideoCapture(0)
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(recogpath)

            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                cl1 = clahe.apply(gray)
                faces = facecasc.detectMultiScale(cl1, scaleFactor=1.1,
                                                  minNeighbors=5, minSize=(30,30),
                                                  flags=cv2.CASCADE_SCALE_IMAGE)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    ids, conf = recognizer.predict(cl1[y:y+h,x:x+w])
                    name = record[1]
                    if conf < 50:
                        cv2.putText(frame, name, (x+2,y+h-5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0), 2)
                    else:
                        cv2.putText(frame, 'No Match', (x+2,y+h-5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow('Face Recognizer. Press [ESC] to quit', frame)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()
            return conf
        else:
            print('Username or password are incorrect')
    except IOError as error:
        print(error)
