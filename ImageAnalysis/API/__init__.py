from API.Pages import HTML_pages
from flask import Flask,request,redirect,session,Response
import numpy as np
import cv2
from PIL import Image
from Analysis import Representations
from Analysis.Representations import ImageRepresentations
import json
import picamera

app = Flask(__name__)
vc = cv2.VideoCapture(0) 

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

class Session(object):
    
    def __init__(self):
        self.img_rep = None

@app.route('/')
def get_redirect_home():
    return get_home()

@app.route('/home')
def get_home():
    return HTML_pages.img_upload

def gen(): 
    """Video streaming generator function.""" 
    while True: 
        rval, frame = vc.read() 
        cv2.imwrite('pic.jpg', frame) 
        yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n') 
@app.route('/video_feed') 
def video_feed(): 
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

@app.route('/input', methods = ['GET', 'POST'])
def post_upload_image():
    if request.method == 'POST':
        npimg = np.fromfile(request.files['img2'], np.uint8)
        img_array_BGR = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img_array_RGB = cv2.cvtColor(img_array_BGR , cv2.COLOR_BGR2RGB)
        Session.img_rep = ImageRepresentations(array=img_array_RGB, image=Image.fromarray(img_array_RGB, "RGB"))
        Session.img_rep.populate_filtered_images()
        Session.img_rep.sobel_edge_detection()
        Session.img_rep.erosion()
        Session.img_rep.dilation()
        Session.img_rep.histogram()
        Session.img_rep.canny_edge_detection(min_threshold=100,max_threshold=200)
        Session.img_rep.hough_line_transform()
        Session.img_rep.hough_circle_transform()
        Session.img_rep.face_detection()
    return redirect("/view")

@app.route("/view")
def get_view_images():
    return HTML_pages.img_break_down

@app.route('/original_image')
def get_original_image():
    return Representations.serve_pil_image(Session.img_rep.original)

@app.route('/filtered-1')
def get_filtered1():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[0])

@app.route('/filtered-2')
def get_filtered2():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[1])

@app.route('/filtered-3')
def get_filtered3():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[2])

@app.route('/filtered-4')
def get_filtered4():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[3])

@app.route('/filtered-5')
def get_filtered5():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[4])

@app.route('/filtered-6')
def get_filtered6():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[5])

@app.route('/filtered-7')
def get_filtered7():
    return Representations.serve_pil_image(Session.img_rep.filtered_images[6])

@app.route('/edged-1')
def get_edged1():
    return Representations.serve_pil_image(Session.img_rep.edged_images[0])

@app.route('/edged-2')
def get_edged2():
    return Representations.serve_pil_image(Session.img_rep.edged_images[1])

@app.route('/lined-1')
def get_lined2():
    return Representations.serve_pil_image(Session.img_rep.lined_image)

@app.route('/circled-1')
def get_circled1():
    return Representations.serve_pil_image(Session.img_rep.circled_image)

@app.route('/eroded-1')
def get_eroded1():
    return Representations.serve_pil_image(Session.img_rep.eroded_image)

@app.route('/dilated-1')
def get_dilated1():
    return Representations.serve_pil_image(Session.img_rep.dilated_image)

@app.route('/histogram-1')
def get_histogram():
    return Representations.serve_pil_image(Session.img_rep.image_histogram)

@app.route('/faces-1')
def get_faces():
    return Representations.serve_pil_image(Session.img_rep.detected_faces)


if __name__ == '__main__':
    app.run(debug=True)