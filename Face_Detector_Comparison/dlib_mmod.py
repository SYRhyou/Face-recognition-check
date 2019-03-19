import cv2, time, dlib

# load model
detector = dlib.cnn_face_detection_model_v1('models/mmod_human_face_detector.dat')

# initialize video source, default 0 (webcam)
video_path = 0
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
  ret, img = cap.read()
  if not ret:
    break


  # prepare input
  result_img = img.copy()
  rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

  # inference, find faces
  detections = detector(rgb_img, 0)

  # postprocessing
  for d in detections:
    x1, y1, x2, y2 = d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()

    # draw rects
    cv2.rectangle(result_img, (x1, y1), (x2, y2), (255, 255, 255), 2, cv2.LINE_AA)


  # visualize
  cv2.imshow('result', result_img)
  if cv2.waitKey(1) == ord('q'):
    break


cap.release()
