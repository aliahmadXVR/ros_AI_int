#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import PointCloud2
import ros_numpy
import base64
import time
import requests
import json
import numpy as np
import cv2
import subprocess

class face_recog_integration:

    # Init 
    def __init__(self):

        print("Inside Init")
        self.bridge = CvBridge()

        self.addr = 'http://localhost:5000'
        self.test_url =  self.addr + '/face_recognition'
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}     
        self.image_acquired = False
        self.cv_image = None
        #ROS Subscriber related 
        rospy.init_node('face_regist_ros', anonymous=True)
        rospy.Subscriber("k4a/rgb/image_rect_color", Image, self.image_callback)
        self.reg_feedback_pub = rospy.Publisher('/registration_feedback', String, queue_size=10)
        print("Init Done")

    # Callback for getting image from Azure Kinect ROS-Topic
    def image_callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
    def run_main(self):
        print("Inside main")
        while  not rospy.is_shutdown():
            if self.cv_image is not None:
                # self.cv_image = cv2.resize(self.cv_image, (640,480) , interpolation = cv2.INTER_AREA)
                print ("encoding image")
                _, img_encoded = cv2.imencode('.jpg', self.cv_image)
                # string_img = base64.binascii.b2a_base64(self.cv_image).decode("ascii")
                print("image encoded")
                
                t0 = time.time()
                response = requests.post(self.test_url, data=img_encoded.tostring(), headers=self.headers)
                print("Inference time: " + str(time.time() - t0))

                response = json.loads(response.text)
                print(response)
                
                # if(saved_count == 9):
                #     rospy.signal_shutdown("All images saved")
            
# -----------------------------------------
if __name__ == '__main__':
    try:
        inter = face_recog_integration()
        # inter.run_registration_server()
        inter.run_main()

    except rospy.ROSInterruptException:
        pass

