# import sys
# from API.Pages import HTML_pages
# from flask import Flask,request,redirect,session,Response
# import numpy as np
# from PIL import Image
# from Analysis import Representations
# from Analysis.Representations import ImageRepresentations
# import json
# import io
# from threading import Condition,Thread
# import queue
from flask import Flask, Response
import cv2



app = Flask(__name__)

vc = cv2.VideoCapture(0) 

def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        # Session.video_frame.put(frame)
        buf_array = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf_array + b'\r\n')

@app.route('/video_feed') 
def video_feed(): 
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
    
# @app.route('/analyze_video')
# def get_video():
#     rval, frame = vc.read()
#     Session.video_frame.put(frame)
#
#     vid_array = cv2.cvtColor(Session.video_frame.get(), cv2.COLOR_BGR2RGB)
#     Session.vid_rep = ImageRepresentations(array=vid_array, image=Image.fromarray(vid_array, "RGB"))
#     Session.facial_process_thread = Thread(target = Session.vid_rep.process_faces, args = (Session.video_frame,))
#     Session.facial_process_thread.start()
#     Session.histogram_process_thread = Thread(target = Session.vid_rep.process_histogram, args = (Session.video_frame,))
#     Session.histogram_process_thread.start()
#
#     return HTML_pages.video_stream
#
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
# #     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response
#
# class Session(object):
#
#     video_frame = queue.Queue()
#
#     def __init__(self):
#         self.img_rep = None
#         self.img_process_thread = None
#         self.vid_rep = None
#         self.facial_process_thread = None
#         self.histogram_process_thread = None
#
# @app.route('/')
# def get_redirect_home():
#     return get_home()
#
# @app.route('/home')
# def get_home():
#     return HTML_pages.img_upload
#
# @app.route('/input', methods = ['GET', 'POST'])
# def post_upload_image():
#     if request.method == 'POST':
#         npimg = np.fromfile(request.files['img2'], np.uint8)
#         img_array_BGR = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#         img_array_RGB = cv2.cvtColor(img_array_BGR , cv2.COLOR_BGR2RGB)
#         Session.img_rep = ImageRepresentations(array=img_array_RGB, image=Image.fromarray(img_array_RGB, "RGB"))
#         Session.img_process_thread = Thread(target = Session.img_rep.process_image(), args = ((),))
#         Session.img_process_thread.start()
#     return redirect("/view")
#
# @app.route("/view")
# def get_view_images():
#     return HTML_pages.img_break_down
#
# @app.route('/original_image')
# def get_original_image():
#     return Representations.serve_pil_image(Session.img_rep.original)
#
# @app.route('/filtered-1')
# def get_filtered1():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[0])
#
# @app.route('/filtered-2')
# def get_filtered2():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[1])
#
# @app.route('/filtered-3')
# def get_filtered3():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[2])
#
# @app.route('/filtered-4')
# def get_filtered4():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[3])
#
# @app.route('/filtered-5')
# def get_filtered5():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[4])
#
# @app.route('/filtered-6')
# def get_filtered6():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[5])
#
# @app.route('/filtered-7')
# def get_filtered7():
#     return Representations.serve_pil_image(Session.img_rep.filtered_images[6])
#
# @app.route('/edged-1')
# def get_edged1():
#     return Representations.serve_pil_image(Session.img_rep.edged_images[0])
#
# @app.route('/edged-2')
# def get_edged2():
#     return Representations.serve_pil_image(Session.img_rep.edged_images[1])
#
# @app.route('/lined-1')
# def get_lined2():
#     return Representations.serve_pil_image(Session.img_rep.lined_image)
#
# @app.route('/circled-1')
# def get_circled1():
#     return Representations.serve_pil_image(Session.img_rep.circled_image)
#
# @app.route('/eroded-1')
# def get_eroded1():
#     return Representations.serve_pil_image(Session.img_rep.eroded_image)
#
# @app.route('/dilated-1')
# def get_dilated1():
#     return Representations.serve_pil_image(Session.img_rep.dilated_image)
#
# @app.route('/histogram-1')
# def get_histogram1():
#     return Representations.serve_pil_image(Session.img_rep.image_histogram)
#
# def generate_histogram():
#     """Video streaming generator function."""
#     while True:
#         processed = Session.vid_rep.image_histogram
#         if processed is not None:
#             buf_array = cv2.imencode('.jpg', processed)[1].tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buf_array + b'\r\n')
#
# @app.route('/histogram-2')
# def get_histogram2():
#     return Response(generate_histogram(),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/faces-1')
# def get_faces1():
#     return Representations.serve_pil_image(Session.img_rep.detected_faces)
#
# def generate_faces():
#     """Video streaming generator function."""
#     while True:
#         processed = Session.vid_rep.face_in_frame
#         if processed is not None:
#             buf_array = cv2.imencode('.jpg', processed)[1].tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buf_array + b'\r\n')
#
# @app.route('/faces-2')
# def get_faces2():
#     return Response(generate_faces(),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)