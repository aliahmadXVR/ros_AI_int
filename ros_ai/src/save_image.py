from __future__ import print_function
import requests
import json
import time
import cv2
import base64
import os


cam = cv2.VideoCapture(0)
_, img = cam.read()
cv2.imwrite('camera_screenschot'+'.jpg', img)
# img = cv2.flip(img, 1)
# img = cv2.resize(img, (640,480) , interpolation = cv2.INTER_AREA)
