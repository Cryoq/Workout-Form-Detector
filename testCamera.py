import cv2

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    
    
    if success:
        cv2.imshow("test", image)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
        
