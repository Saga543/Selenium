import cv2
import mediapipe as mp
# read Video from webcam
cap = cv2.VideoCapture(0)


class FaceDetector(mp.solutions.face_mesh.FaceMesh):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detect_face(self, img):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.process(img_RGB)
        mp_drawing = mp.solutions.drawing_utils
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(img, face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)


class HandDetector(mp.solutions.hands.Hands):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detect_hands(self, img):
        height, width, channel = img.shape
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.process(img_RGB)
        mp_drawing = mp.solutions.drawing_utils
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)
                # draw a circle on a specified point
                # for id_,lm in enumerate(handLms.landmark):
                #     # cx, cy = int(lm.x * width), int(lm.y*height)
                #     # if id_ == 8:
                #     #     cv2.circle(img,(cx,cy),8,(255,255,0), cv2.FILLED)
        handsD = HandDetector()
        faceD = FaceDetector()
        while cv2.waitKey(1) != ord('q'):
            _, img = cap.read()
            # detect hands
            handsD.detect_hands(img)
            # detect face
            faceD.detect_face(img)
            # show image
            cv2.imshow('cap1', img)
        # turn off the video capture and close all windows
        cap.release()
        cv2.destroyAllWindows()