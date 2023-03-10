#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import PointCloud2
import ros_numpy
import requests
# from display import parameters
# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont


# from memory_profiler import profile

# import k4a
# import docker
import base64
import time
import requests
import json
import numpy as np
import cv2


#For Deleting Images
import os
import glob

#done for testing some ros msgs
# from ros_ai.msg import gait_parameters

class integration:
    # @profile
    def __init__(self):

        print('inside init')
        print('Deleting previous Images')
        # Deleting Images Stored @ /home/xavor/SiamRPN_Tracking_API/Data/Input/Image/

        print('inside init')
        print('Deleting previous Images')
        # Deleting Images Stored @ /home/xavor/SiamRPN_Tracking_API/Data/Input/Image/

        home_path = os.path.expanduser('~')
        # rospy.loginfo(home_path)
        working_dir_image = '/home/orin2/Input/Image/*'
        working_dir_pc = '/home/orin2/Input/Point_Cloud/*'
        #print working_dir
        files = glob.glob(working_dir_image)

        for f in files:
            os.remove(f)

        files = glob.glob(working_dir_pc)

        for f in files:
            os.remove(f)

        print('Deleted all files')


        self.bridge = CvBridge()

        self.addr = 'http://10.21.8.22:5000'
        self.test_url =  self.addr + '/track_person'

        # prepare headers for http request
        self.content_type = 'application/json'
        self.headers = {'content-type': self.content_type}
        
        self.data = ''

        self.xyz_image = None
        self.cv_image = None
        self.url = 'http://0.0.0.0:24/upload'

        # self.point = PointStamped()

        # self.gait_param_msg = gait_parameters()


       
        '''
        Setting up docker clinet and running the container
        '''
        # self.client = docker.from_env()
        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True, 
        # volumes=['/home/zeeshan/xavor/int_ws/src/ros_ai/scripts:/app'])

        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True)
        
        rospy.init_node('integration', anonymous=True)
    

        # self.pub = rospy.Publisher('/person_loc', PointStamped, queue_size=10)
        rospy.Subscriber("/camera/color/image_rect_color", Image, self.img_callback)
        rospy.Subscriber("/camera/depth_registered/points", PointCloud2, self.pc_callback)
    #@profile
    def pc_callback(self, pc2_msg):
        # rospy.loginfo(pc2_msg.height)
        # rospy.loginfo(pc2_msg.width)
        try:
            pc = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(pc2_msg, remove_nans=False)
        except CvBridgeError as e:
            print(e)
            
        if pc is not None:
            # print('PC shape:', pc.shape)
            # pc_x = pc[:,0].reshape((480, 640))
            # pc_y = pc[:,1].reshape((480, 640))
            # pc_z = pc[:,2].reshape((480, 640))
            # rospy.loginfo("priniting length")
            # rospy.loginfo(len(pc[0,:]))
            # print('PC center point raw:', np.stack([pc_x,pc_y, pc_z], axis=2)[360,640,:])
            xyz_image = np.stack([pc[:,:,0],pc[:,:,1],pc[:,:,2]], axis=2)
            # print(pc.shape)
            #self.xyz_image = (xyz_image*1000).astype(np.int16)
            self.xyz_image = np.array(xyz_image*1000)
            #print(self.xyz_image.shape)
            # print('PC center point float16:', self.xyz_image[360,640,:])

            # print(self.xyz_image.shape)

    #@profile
    def img_callback(self, data):

        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # print(self.cv_image)
        except CvBridgeError as e:
            print(e)

    # @profile
    def run(self):

        # rate = rospy.Rate(4)
        count = 0
        while  not rospy.is_shutdown():
            # print("Before If")
            if self.cv_image is not None and self.xyz_image is not None:
                # file = [self.cv_image, self.xyz_image]
                # response = requests.post(url=self.url, files=file)
                # Uncomment below two lines if using serialization/deserialization 
                # string_img = base64.binascii.b2a_base64(self.cv_image).decode("ascii")
                # str_point_cloud = base64.binascii.b2a_base64(self.xyz_image).decode("ascii") 

            ########## Sending Data via Read/Write Operations ##################
                request_time_str = time.asctime(time.localtime(time.time()))
                image_path_write = "/home/orin2/Input/Image/{0}_{1}.jpg".format(request_time_str, count)
                point_cloud_path_write = "/home/orin2/Input/Point_Cloud/{0}_{1}.npy".format(request_time_str, count)
                image_path = "/app/Data/Input/Image/{0}_{1}.jpg".format(request_time_str, count)
                point_cloud_path = "/app/Data/Input/Point_Cloud/{0}_{1}.npy".format(request_time_str, count)
                # rospy.loginfo("here, writing images")

                # # image_path_write = "/home/xavor/SiamRPN_Tracking_API/Data/Input/Image/{0}_{1}.jpg".format(request_time_str, count)
                # # point_cloud_path_write = "/home/xavor/SiamRPN_Tracking_API/Data/Input/Point_Cloud/{0}_{1}.npy".format(request_time_str, count)


                cv2.imwrite(image_path_write, self.cv_image)
                with open(point_cloud_path_write, 'wb') as f:
                    np.save(f, self.xyz_image)

                demo = True
                
                self.data = {'image': image_path, 'point_cloud': point_cloud_path, 're_initialize': False, 'demo': demo} 
                if not count: 
                    self.data = {'image': image_path, 'point_cloud': point_cloud_path, 're_initialize': True, 'demo': demo}
                count += 1
            ####################################################################
                # path1= '/home/orin2/Refactored_API/data_for_AI_new/image/'+str1+'.jpg'
                # path2= '/home/orin2/Refactored_API/data_for_AI_new/testingfile.npy'
                file = [('files', open(image_path_write, 'rb')), ('files', open(point_cloud_path_write, 'rb'))]
                response = requests.post(url=self.url, files=file)
                print(response.json())
                # Uncomment this line if using serialization/deserialization 
                # self.data = {'image': string_img, "image_shape": self.cv_image.shape, 'point_cloud': str_point_cloud, 'point_cloud_shape': self.xyz_image.shape}

                # t0 = time.time()
                
                # response = requests.post(self.test_url, json=self.data, headers=self.headers)
                # print("Inference time: " + str(time.time() - t0))
                

                # response = json.loads(response.text)
                # response_decoded = jsonpickle.decode(response['point'])
                # point = response['point']
                # print("Response: {0}".format(response))

                # self.point.header.stamp = rospy.Time.now()
                # self.point.header.frame_id = 'azure_link'

                # if point is None or (point[0] == 0 and point[1] == 0 and point[2] == 0):
                #     self.point.point.x = -9999
                #     self.point.point.y = -9999-
                #     self.point.point.z = -9999
                # else:
                #     self.point.point.x = point[0]
                #     self.point.point.y = point[1]
                #     self.point.point.z = point[2]

                    # self.gait_param_msg.custom_str = "test custom msg"

                # rospy.loginfo(self.point)

                # self.pub.publish(self.point)

                # window_name = 'image'
                # cv2.imshow(window_name, self.xyz_image.astype('uint16'))
                # cv2.waitKey(0) 
                # cv2.destroyAllWindows() 

            # rate.sleep()



if __name__ == '__main__':
    try:
        inter = integration()
        inter.run()

    except rospy.ROSInterruptException:
        pass