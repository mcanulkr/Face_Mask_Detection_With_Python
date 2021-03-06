import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cv2
from keras.models import load_model
import arduino


findFace = cv2.CascadeClassifier('face_view.xml')
threshold=0.90
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
font=cv2.FONT_HERSHEY_COMPLEX
model = load_model('MyTrainingModel.h5')

def setImage(img):
    img=img.astype("uint8")
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=cv2.equalizeHist(img)
    img = img/255
    return img

def result(classNo):
	if classNo==0:
		return "Maske Takılı"
	elif classNo==1:
		return "Maske Yok"


while True:
	sucess, imgOrignal=cap.read()
	faces = findFace.detectMultiScale(imgOrignal,1.3,5)
	for x,y,w,h in faces:
		crop_img=imgOrignal[y:y+h,x:x+h]
		img=cv2.resize(crop_img, (32,32))
		img=setImage(img)
		img=img.reshape(1, 32, 32, 1)
		prediction=model.predict(img)
		classIndex=np.argmax(prediction,axis=1)
		probabilityValue=np.amax(prediction)
		if probabilityValue>threshold:
			if classIndex==0:
				arduino.door1(0)
				arduino.door2(0)
				cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(0,255,0),2)
				cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (0,255,0),-2)
				cv2.putText(imgOrignal, str(result(classIndex)),(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)
			elif classIndex==1:
				arduino.door1(1)
				arduino.door2(1)
				cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(50,50,255),2)
				cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (50,50,255),-2)
				cv2.putText(imgOrignal, str(result(classIndex)),(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)
	cv2.imshow("Result",imgOrignal)
	k=cv2.waitKey(1)
	if k==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()