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

class face_reg_integration:

    # Init 
    def __init__(self):

        print('Initializing...')
        
        self.bridge = CvBridge()

        self.addr = 'http://localhost:5000'
        self.test_url =  self.addr + '/face_register'
        self.content_type = 'application/json'
        self.headers = {'content-type': self.content_type}     
    
        self.frame_dict = {'frontal': 0, 'top': 0, 'bottom': 0, 'left': 0, 'right': 0, 'top_right': 0, 'top_left': 0,
                  'bottom_left': 0, 'bottom_right': 0}

        self.cv_image = None
        self.username = "Anon. User"
        self.saved_count = 0

        #ROS Subscriber related 
        rospy.init_node('face_regist_ros', anonymous=True)
        rospy.Subscriber("k4a/rgb/image_rect_color", Image, self.image_callback)
        rospy.Subscriber("k4a/points2", PointCloud2, self.point_cloud_callback)
        self.feedback_pub = rospy.Publisher('/registration_feedback', String, queue_size=10)



    # Callback for getting image from Azure Kinect ROS-Topic
    def image_callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    # Callback for getting Pointcloud from Azure Kinect ROS-Topic
    def point_cloud_callback(self, pc2_msg):
        # print("Inside pointcloud callback")
        point_cloud = "true"
        
    def run_main(self):
        while  not rospy.is_shutdown():
            if self.cv_image is not None:
                self.cv_image = cv2.resize(self.cv_image, (640,480) , interpolation = cv2.INTER_AREA)
                string_img = base64.binascii.b2a_base64(self.cv_image).decode("ascii")
                data = {'img': string_img, 'frame_dict': self.frame_dict, 'saved_count': self.saved_count, 'username': self.username}

                t0 = time.time()
                response = requests.post(self.test_url, json=data, headers=self.headers)
                # print("Inference time: " + str(time.time() - t0))

                response = json.loads(response.text)
                status_msg = response['messege']
                print (status_msg)
                saved_count = response['saved_count']
                print(saved_count)
                
                self.feedback_pub.publish(status_msg)
                
                if(saved_count == 9):
                    rospy.signal_shutdown("Killing node")
               
            
# -----------------------------------------
if __name__ == '__main__':
    try:
        inter = face_reg_integration()
        inter.run_main()

    except rospy.ROSInterruptException:
        pass

