class HTML_pages(object):
    
    video_stream = '''
    <html> 
    <head> 
        <title>Video Streaming </title> 
    </head> 
    <body>
        <div>
            <h1> Live Video Streaming </h1> 
            <img src="http://localhost:5000/video_feed">
        </div>
        <div>
            <h1>Face Detection</h1>
            <img src="http://localhost:5000/faces-2">
        </div>
        <br>
        <br>
        <br>
        <div>
            <h1>Pixel Histogram</h1>
            <img src="http://localhost:5000/histogram-2">
        </div>
        </body> 
    </html> 
    '''
    
    favicon = '''
    <link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon"> 
    '''
    
    img_upload = '''
    <html>
        <head>
            <title>Upload Image</title>
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
            <meta http-equiv="Pragma" content="no-cache" />
            <meta http-equiv="Expires" content="0" />
        </head>
        <body>
            <h1>Image upload</h1>
            <form action="http://localhost:5000/input" method="post" enctype = "multipart/form-data">
                <input id="img2" type="file" name="img2" accept=".jpg,.png,.ppm">
                <input type="submit">
            </form>
        </body>
    </html>
    '''
    
    img_break_down = '''
    <html>
        <head>
            <title>Image analysis</title>
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
            <meta http-equiv="Pragma" content="no-cache" />
            <meta http-equiv="Expires" content="0" />
        </head>
        <body>
            <div>
                <h1>Original Image</h1>
                <img src="http://localhost:5000/original_image">
            </div>
            <div>
                <h1>Only Red Channel</h1>
                <img src="http://localhost:5000/filtered-1">
            </div>
            <div>
                <h1>Only Green Channel</h1>
                <img src="http://localhost:5000/filtered-2">
            </div>
            <div>
                <h1>Only Blue Channel</h1>
                <img src="http://localhost:5000/filtered-3">
            </div>
            <div>
                <h1>No Red Channel</h1>
                <img src="http://localhost:5000/filtered-4">
            </div>
            <div>
                <h1>No Green Channel</h1>
                <img src="http://localhost:5000/filtered-5">
            </div>
            <div>
                <h1>No Blue Channel</h1>
                <img src="http://localhost:5000/filtered-6">
            </div>
            <div>
                <h1>Gray Scale</h1>
                <img src="http://localhost:5000/filtered-7">
            </div>
            <div>
                <h1>Sobel Edge Detection</h1>
                <img src="http://localhost:5000/edged-1">
            </div>
            <div>
                <h1>Canny Edge Detection</h1>
                <img src="http://localhost:5000/edged-2">
            </div>
            <div>
                <h1>Hough Line Detection using Canny Edge</h1>
                <img src="http://localhost:5000/lined-1">
            </div>
            <div>
                <h1>Hough circle Detection</h1>
                <img src="http://localhost:5000/circled-1">
            </div>
            <div>
                <h1>Erosion</h1>
                <img src="http://localhost:5000/eroded-1">
            </div>
            <div>
                <h1>Dilation</h1>
                <img src="http://localhost:5000/dilated-1">
            </div>
            <br>
            <br>
            <br>
            <div>
                <h1>Pixel Histogram</h1>
                <img src="http://localhost:5000/histogram-1">
            </div>
            <div>
                <h1>Face Detection</h1>
                <img src="http://localhost:5000/faces-1">
            </div>
        </body>
    </html>
    '''