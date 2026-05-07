import os
import cv2

DATA_DIR = 'C:/Users/HP/Desktop/SLR-Project/data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 11
dataset_size = 100

cap = cv2.VideoCapture(0)

try:
    for j in range(number_of_classes):
        class_dir = os.path.join(DATA_DIR, str(j))
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        print('Collecting data for class {}'.format(j))

        while True:
            ret, frame = cap.read()
            cv2.putText(frame, 'Ready? Press "Q" to start, or "ESC" to exit.', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            key = cv2.waitKey(25)
            if key == ord('q'):
                break
            elif key == 27:  # ESC key
                print("Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                exit()

        counter = 0
        while counter < dataset_size:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            key = cv2.waitKey(25)
            if key == 27:  # ESC key
                print("Early exit during data collection.")
                cap.release()
                cv2.destroyAllWindows()
                exit()
            cv2.imwrite(os.path.join(class_dir, '{}.jpg'.format(counter)), frame)
            counter += 1

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
