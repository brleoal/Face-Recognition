# Face-Recognition
Facial recognition system for biometric restricted area access.
Based on https://github.com/Aryal007/opencv_face_recognition.git, a GUI was added for access login with username and password and other GUI for manage users database. If access was successful, shows user image from database and opens a door via RS232 circuit.

Requeriments:

- Python 2.7
- OpenCV
- SQLite
- QT5, PyQT5

Usage:

GUI access login with username and password
```sh
$ python face_gui.py 
```
GUI for manage users database.
```sh
$ python datamanager.py
```
