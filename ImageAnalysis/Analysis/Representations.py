from io import BytesIO
from flask import send_file
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
'''
Created on Apr 23, 2019

@author: shangbao.huang
'''

class ImageRepresentations(object):
    '''
    classdocs
    '''


    def __init__(self, image=None, array=None):
        '''
        Constructor
        Parameters:
        original: pillow (PIL) Image
        image_array: numpy array
        '''
        self.image_array = array
        if (image):
            self.original = image
        else:
            Image.fromarray(self.image_array, "RGB")
        self.filtered_images = []
        self.edged_images = []
        self.face_in_frame = None
        self.image_histogram = None
        self.figure = None
        self.histograms = []
        
    def process_image(self):
        self.populate_filtered_images()
        self.sobel_edge_detection()
        self.erosion()
        self.dilation()
        self.histogram()
        self.canny_edge_detection(min_threshold=100,max_threshold=200)
        self.hough_line_transform()
        self.hough_circle_transform()
        self.face_detection()
        
    def process_faces(self, frame_queue):
        while True:
            frame = frame_queue.get()
            self.face_in_frame = detect_face(frame)
            with frame_queue.mutex:
                frame_queue.queue.clear()
    
    def process_histogram(self, frame_queue):
        while True:
            frame = frame_queue.get()
            self.image_histogram = self.histogram_of(frame)
            with frame_queue.mutex:
                frame_queue.queue.clear()
        
    def populate_filtered_images(self):
#         red, green, and blue channel only, respectively
        temp_array = np.copy(self.image_array)
        temp_array[:,:,1:3] = 0
        self.filtered_images.append(Image.fromarray(temp_array, "RGB"))
        temp_array = np.copy(self.image_array)
        temp_array[:,:,0:3:2] = 0
        self.filtered_images.append(Image.fromarray(temp_array, "RGB"))
        temp_array = np.copy(self.image_array)
        temp_array[:,:,0:2] = 0
        self.filtered_images.append(Image.fromarray(temp_array, "RGB"))
#         red, green, and blue channel filtered, respectively
        temp_array = np.copy(self.image_array)
        temp_array[:,:,0] = 0
        self.filtered_images.append(Image.fromarray(temp_array,"RGB"))
        temp_array = np.copy(self.image_array)
        temp_array[:,:,1] = 0
        self.filtered_images.append(Image.fromarray(temp_array,"RGB"))
        temp_array = np.copy(self.image_array)
        temp_array[:,:,2] = 0
        self.filtered_images.append(Image.fromarray(temp_array,"RGB"))
        self.filtered_images.append(Image.fromarray(cv2.cvtColor(self.image_array,cv2.COLOR_RGB2GRAY)))
        
    def sobel_edge_detection(self):
#         vert_sobel = [[-1, 0, 1],
#                       [-2, 0, 2],
#                       [-1, 0, 1]]
#         horz_sobel = [[-1, -2, -1],
#                       [0, 0, 0],
#                       [1, 2, 1]]
#         grey = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
#         vert_edge = convolve2d(grey,vert_sobel)
#         horz_edge = convolve2d(grey,horz_sobel)
#         edges = np.sqrt(np.add(np.square(vert_edge),np.square(horz_edge)))
        edges = ndimage.sobel(cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY))
        self.edged_images.append(Image.fromarray(edges,"L"))
        
    def canny_edge_detection(self,min_threshold=100,max_threshold=200):
        self.canny_edges = cv2.Canny(self.image_array,min_threshold,max_threshold)
        self.edged_images.append(Image.fromarray(self.canny_edges, "L"))
        
    def hough_line_transform(self):
        lined_image_array = np.copy(self.image_array)
        lines = cv2.HoughLines(self.canny_edges,1,np.pi/180,200)
        if (lines is not None):
            for line in lines:
                for rho,theta in line:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a*rho
                    y0 = b*rho
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))
                
                    cv2.line(lined_image_array,(x1,y1),(x2,y2),(0,0,255),2)
        self.lined_image = Image.fromarray(lined_image_array)
        
    def hough_circle_transform(self):
        circled_image_array = cv2.cvtColor(np.copy(self.image_array),cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(circled_image_array,cv2.HOUGH_GRADIENT,1,10,
                            param1=100,param2=90,minRadius=0,maxRadius=0)
        if (circles is not None):
            circles = np.uint16(np.around(circles))
            for circle in circles:
                for i in circle[:]:
                    # draw the outer circle
                    cv2.circle(circled_image_array,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(circled_image_array,(i[0],i[1]),2,(0,0,255),3)
        self.circled_image = Image.fromarray(circled_image_array)
        
    def erosion(self):
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(self.image_array,kernel,iterations = 1)
        self.eroded_image = Image.fromarray(erosion, "RGB")
    
    def dilation(self):
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(self.image_array,kernel,iterations = 1)
        self.dilated_image = Image.fromarray(dilation, "RGB")
        
    def histogram(self):
        self.image_histogram = Image.fromarray(self.histogram_of(self.image_array))
        
    def face_detection(self):
        img = np.copy(self.image_array)
        detect_face(img)
        self.detected_faces_array = img
        self.detected_faces = Image.fromarray(img,"RGB")
        
    def histogram_of(self,img):
        # img: numpy image array
        fig, sub = plt.subplots(4, 1)
        self.figure, self.histograms = fig, sub
        sub[0].hist(img.ravel(),256,[10,256])
        sub[0].set(title="RGB Pixel Breakdown")
        sub[1].hist(img[:,:,0].ravel(),256,[10,256])
        sub[1].set(title="Red Pixel Breakdown")
        sub[2].hist(img[:,:,1].ravel(),256,[10,256])
        sub[2].set(title="Green Pixel Breakdown")
        sub[3].hist(img[:,:,2].ravel(),256,[10,256])
        sub[3].set(title="Blue Pixel Breakdown")
        fig.text(0.5, 0.01, 'Pixel Intensity', ha='center')
        fig.text(0, 0.5, 'Number of Pixels', va='center', rotation='vertical')
        fig.tight_layout()
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return data
        
def detect_face(img):
    face_cascade = cv2.CascadeClassifier('C:\\Python37\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\\Python37\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if (faces is not None):
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    return img
    
def stream_to_image(stream):
    npimg = np.fromfile(stream, np.uint8)
    img_array_BGR = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img_array_RGB = cv2.cvtColor(img_array_BGR , cv2.COLOR_BGR2RGB)
    return serve_pil_image(Image.fromarray(img_array_RGB, "RGB"))
        
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def serve_pil_images(pil_imgs):
    file_array = []
    for pil_img in pil_imgs:
        file_array.append(serve_pil_image(pil_img))
    return file_array