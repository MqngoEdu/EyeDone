# Eye Tracker
# Magnus Lie
# 11/14/23
# 11/16/23
# Tracks eyes through a camera

import cv2 as cv
import numpy as np
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh

# Locations and points of the eye
LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]


cap = cv.VideoCapture(0) # Video camera capture.
with mp_face_mesh.FaceMesh(
    max_num_faces=3,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[1].landmark])
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv.circle(frame,center_left, int(l_radius), (255,0,255), 1, cv.LINE_AA)
            cv.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv.LINE_AA)


        cv.imshow('img', frame)
        key = cv.waitKey(1)
        if key ==ord('q'):
            break
cap.release()
cv.destroyAllWindows()

