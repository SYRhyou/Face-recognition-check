import cv2, dlib

# load model
detector = dlib.get_frontal_face_detector()

# initialize video source, default 0 (webcam)
video_path = 0
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
  ret, img = cap.read()
  if not ret:
    break
  
  # prepare input
  result_img = img.copy()

  # inference, find faces
  detections = detector(result_img, 1)
  # postprocessing
  for d in detections:
    x1, y1, x2, y2 = d.left(), d.top(), d.right(), d.bottom()

    # draw rects
    cv2.rectangle(result_img, (x1, y1), (x2, y2), (255, 255, 255), 2, cv2.LINE_AA)

  # visualize
  cv2.imshow('result', result_img)
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()