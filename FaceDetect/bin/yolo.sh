echo Testing model with image: 
read image
./darknet detector test yolo-face.names yolo-face-test.cfg yolo-face.weights -thresh 0.24 $image.jpg crop



