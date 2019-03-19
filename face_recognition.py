import dlib, cv2
import numpy as np

# load models
model_path = 'models/opencv_face_detector_uint8.pb'
config_path = 'models/opencv_face_detector.pbtxt'
detector = cv2.dnn.readNetFromTensorflow(model_path, config_path)

sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')

facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')

conf_threshold = 0.8


# find face and landmarks in image and encode face descriptor
def encode_face(img_path):

  img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

  # find face
  result_img = img_rgb.copy()
  h, w, _ = result_img.shape
  blob = cv2.dnn.blobFromImage(result_img, 1.0, (300, 300), [104, 117, 123], False, False)
  detector.setInput(blob)

  dets = detector.forward()

  # postprocessing
  for i in range(dets.shape[2]):
    confidence = dets[0, 0, i, 2]
    if confidence > conf_threshold:
      x1 = int(dets[0, 0, i, 3] * w)
      y1 = int(dets[0, 0, i, 4] * h)
      x2 = int(dets[0, 0, i, 5] * w)
      y2 = int(dets[0, 0, i, 6] * h)

  if len(dets) == 0 or len(dets) > 1:
    raise Exception('There\'s no faces or more than 1 faces in %s' % img_path)
  else:
    print("face detected")

  for k, d in enumerate(dets):
    d = dlib.rectangle(x1,y1,x2,y2)
    shape = sp(img_rgb, d)
    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)
    return np.array(face_descriptor)

# # make database

descs = dict()
descs['Rhyou'] = encode_face('img/Rhyou.jpg')
descs['Noh'] = encode_face('img/Noh.jpg')
descs['Kim'] = encode_face('img/Kim.jpg')
print("done!")


# 0 -> webcam
video_path = 0
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
  exit()

_, img_bgr = cap.read()
padding_size = 0
resized_width = 640
video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

while cap.isOpened():
  ret, img_bgr = cap.read()
  if not ret:
    break

  # resize for realtime speed
  img_bgr = cv2.resize(img_bgr, video_size)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
  
  # find faces
  result_img = img_bgr.copy()
  h, w, _ = result_img.shape
  blob = cv2.dnn.blobFromImage(result_img, 1.0, (300, 300), [104, 117, 123], False, False)
  detector.setInput(blob)
  dets = detector.forward()
  # postprocessing
  for i in range(dets.shape[2]):
    confidence = dets[0, 0, i, 2]
    if confidence > conf_threshold:
      x1 = int(dets[0, 0, i, 3] * w)
      y1 = int(dets[0, 0, i, 4] * h)
      x2 = int(dets[0, 0, i, 5] * w)
      y2 = int(dets[0, 0, i, 6] * h)

  for k, d in enumerate(dets):
    d = dlib.rectangle(x1,y1,x2,y2)
    shape = sp(img_rgb, d)
    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

    # threshold 0.8
    found = {'name': 'unknown', 'dist': 0.45, 'color': (0,0,255)}

    # compute distance of video image and database images
    for name, saved_desc in descs.items():
      dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)      
      
      if dist < found['dist']:
        found = {'name': name, 'dist': dist, 'color': (255,255,255)}
        if(found['name'] == 'unknown'):
          found = {'name': 'unknown', 'dist': dist, 'color': (0,0,255)}
  # find faces
  result_img = img_bgr.copy()
  h, w, _ = result_img.shape
  blob = cv2.dnn.blobFromImage(result_img, 1.0, (300, 300), [104, 117, 123], False, False)
  detector.setInput(blob)
  dets = detector.forward()
  # postprocessing
  for i in range(dets.shape[2]):
    confidence = dets[0, 0, i, 2]
    if confidence > conf_threshold:
      x1 = int(dets[0, 0, i, 3] * w)
      y1 = int(dets[0, 0, i, 4] * h)
      x2 = int(dets[0, 0, i, 5] * w)
      y2 = int(dets[0, 0, i, 6] * h)

      # visualize
      cv2.rectangle(result_img, (x1, y1), (x2, y2), found['color'] , int(round(h/150)), cv2.LINE_AA)
      cv2.putText(result_img, found['name'], (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1,found['color'] , 2, cv2.LINE_AA)

  cv2.imshow('result', result_img)
  print(found['dist'])
  print(found['name'])
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()


