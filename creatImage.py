import cv2

video=cv2.VideoCapture(0)
findFace=cv2.CascadeClassifier('face_view.xml')
count=0

while True:
	ret,frame=video.read()
	faces=findFace.detectMultiScale(frame,1.3, 5)
	for x,y,w,h in faces:
		count=count+1
		name='./images/face_without_mask/'+ str(count) + '.jpg'
		print("Creating Images........." +name)
		cv2.imwrite(name, frame[y:y+h,x:x+w])
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
	cv2.imshow("WindowFrame", frame)
	cv2.waitKey(1)
	if count>500:
		break
video.release()
cv2.destroyAllWindows()