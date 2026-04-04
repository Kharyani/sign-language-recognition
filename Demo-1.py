import pickle

import cv2
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('C:/Users/ritee/OneDrive/Desktop/SLR-Project/model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'I', 1: 'Need', 2: 'Help', 3: 'Pain', 4: 'Call', 5: 'Feel', 6: 'Police', 7: 'Fire', 8: 'Emergency', 9: 'Accident', 10: 'Saw'}
while True:

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        prediction = model.predict([np.asarray(data_aux)])

        predicted_character = labels_dict[int(prediction[0])]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ESC key
        break


cap.release()
cv2.destroyAllWindows()













'''
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
import pickle
import threading
import time

#Load Pre-trained Model 
model_dict = pickle.load(open('C:/Users/ritee/OneDrive/Desktop/SLR-Project/model.p', 'rb'))
model = model_dict['model']

#Sign Detection Function 
def start_sign_detection():
    cap = cv2.VideoCapture(0)
    
    #Initialize Mediapipe Hands module
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    # Mapping of model output indices to sign labels
    labels_dict = {0: 'I', 1: 'Need', 2: 'Help', 3: 'Pain', 4: 'Call', 5: 'Feel',
                   6: 'Police', 7: 'Fire', 8: 'Emergency', 9: 'Accident', 10: 'Saw'}

    # Main loop to process webcam frames
    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()
        if not ret:
            break

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
            # Extract coordinates for prediction
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)
                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

            # Get bounding box for display
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            # Predict the sign
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            # Display predicted sign on frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

        cv2.imshow('Sign Detection', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

#Digital Clock Update Function
def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    root.after(1000, update_clock) # Repeat every second

#Exit Confirmation
def confirm_exit():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

#Splash Screen Function
def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("650x650+400+100")
    splash.configure(bg="#FDF7E4")

    try:
        splash_image = Image.open("C:/Users/ritee/OneDrive/Desktop/SLR-Project/splash-screen.png")
        splash_photo = ImageTk.PhotoImage(splash_image)
        splash_label = tk.Label(splash, image=splash_photo, bg="#FDF7E4")
        splash_label.image = splash_photo  # keep a reference
        splash_label.pack()
    except Exception as e:
        print("Error loading splash image:", e)
        tk.Label(splash, text="ASLR Loading...", font=("Helvetica", 24), bg="#FDF7E4").pack(expand=True)

    # After 3 seconds, destroy splash and show main GUI
    splash.after(3000, lambda: (splash.destroy(), start_main_gui()))
    splash.mainloop()

#Main GUI Setup
def start_main_gui():
    global root, clock_label  # global for update_clock

    root = tk.Tk()
    root.title("ASL Emergency Alert")
    root.geometry("650x650")
    root.configure(bg="#FDF7E4")

    #Function for Logo Image
    logo_img = Image.open("C:/Users/ritee/OneDrive/Desktop/SLR-Project/logo.png")
    logo_img = logo_img.resize((70, 70))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo, bg="#FDF7E4")
    logo_label.image = logo_photo
    logo_label.place(x=10, y=10)

    #Title Label 
    title_label = tk.Label(root, text="ASLR for Emergency Alerts", font=("Helvetica", 16, "bold"), bg="#FDF7E4", fg="#333333")
    title_label.place(relx=0.5, rely=0.05, anchor="center")

    #Digital Clock (on Top-right)
    clock_label = tk.Label(root, font=("Courier", 16, "bold"), bg="#FDF7E4", fg="#92ff06")
    clock_label.place(relx=1.0, y=10, anchor="ne")
    update_clock()

    #Button Frame
    frame = tk.Frame(root, bg="#FDF7E4")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    #Button Hover Effect
    def on_enter(button, color):
        button.config(bg=color)

    def on_leave(button, color):
        button.config(bg=color)

    #Style for Buttons
    btn_style = {"font": ("Times New Roman", 12, "bold"), "width": 20, "height": 2,
                 "cursor": "hand2", "fg": "white", "relief": "raised", "bd": 4,
                 "bg": "#ff5959"}

    btn1 = tk.Button(frame, text="Perform Sign", command=lambda: threading.Thread(target=start_sign_detection).start(), **btn_style)
    btn1.pack(pady=10)
    btn1.bind("<Enter>", lambda e: on_enter(btn1, "#ff3333"))
    btn1.bind("<Leave>", lambda e: on_leave(btn1, "#ff5959"))

    btn2 = tk.Button(frame, text="Video Tutorial", **btn_style)
    btn2.pack(pady=10)
    btn2.bind("<Enter>", lambda e: on_enter(btn2, "#ff3333"))
    btn2.bind("<Leave>", lambda e: on_leave(btn2, "#ff5959"))

    btn3 = tk.Button(frame, text="Software Manual", **btn_style)
    btn3.pack(pady=10)
    btn3.bind("<Enter>", lambda e: on_enter(btn3, "#ff3333"))
    btn3.bind("<Leave>", lambda e: on_leave(btn3, "#ff5959"))

    btn4 = tk.Button(frame, text="Exit", command=confirm_exit, **btn_style)
    btn4.pack(pady=10)
    btn4.bind("<Enter>", lambda e: on_enter(btn4, "#ff3333"))
    btn4.bind("<Leave>", lambda e: on_leave(btn4, "#ff5959"))

    #Footer Label
    footer_text = ("Final Year Project by: Kashish Haryani & Ritika Rani\n"
                   "from Department of BS Computer Science under the Supervision of Mr. Muhammad Bux Soomro\n"
                   "SZABIST University, Larkana Campus")
    footer_label = tk.Label(root, text=footer_text, font=("Times New Roman", 10, "italic", "bold"),
                            bg="#FDF7E4", justify="center", fg='#000000')
    footer_label.place(relx=0.5, rely=0.9, anchor="center")

    root.mainloop()


#Show splash screen
show_splash()
'''


