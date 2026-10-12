import cv2
import mediapipe as mp
import math
import pyautogui
import time
import os
import subprocess
import webbrowser

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands()

camera=cv2.VideoCapture(1)

screen_width,screen_height=pyautogui.size()
print(screen_width,screen_height)

smooth_x=0
smooth_y=0

assistant_on=True
pinch=False
last_ss=0
last_spotify=0
last_on=0


def map_to_screen(x, y, c_width, c_height, s_width, s_height):
    screen_x = (x / c_width) * s_width
    screen_y = (y / c_height) * s_height
    return screen_x, screen_y
    
def finger(number):
    fin_tip=hand_landmarks.landmark[int(number)]
    fin_x=int(fin_tip.x*width)
    fin_y=int(fin_tip.y*height)
    fin=(fin_x,fin_y)
    return fin

#main loop starts     
while True:
    success,frame=camera.read()
    frame = cv2.flip(frame, 1)
    height,width,_=frame.shape

    
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

#Landmark identify
            index_fin=finger(8)
            thumb_fin=finger(4)

            lan3=finger(3)
            lan1=finger(1)
            lan5=finger(5)

            index_up  = finger(8)[1]  < finger(6)[1]
            middle_up = finger(12)[1] < finger(10)[1]
            ring_up   = finger(16)[1] < finger(14)[1]
            pinky_up  = finger(20)[1] < finger(18)[1]
            ring_down = finger(16)[1] > finger(14)[1]
            pinky_down= finger(20)[1] > finger(18)[1]
            index_down  = finger(8)[1]  > finger(6)[1]
            middle_down = finger(12)[1] > finger(10)[1]


            cv2.circle(frame,(index_fin[0],index_fin[1]),10,(200,240,255),-1)

            if assistant_on:
    #Mouse move
                screen_x,screen_y=map_to_screen(index_fin[0],index_fin[1],width, height, screen_width, screen_height)
                smooth_x += (screen_x-smooth_x)/3
                smooth_y += (screen_y-smooth_y)/3
                pyautogui.moveTo(smooth_x, smooth_y)

    #Mouse click
                dist1=math.dist(index_fin,thumb_fin)
                if dist1<100:
                    if not pinch:
                        pyautogui.mouseDown()
                        pyautogui.moveTo(smooth_x, smooth_y)
                        pinch=True 

                else:
                        pyautogui.mouseUp()
                        pinch=False

    #Volume up/down
    #read about os and subprocesses more-
                if lan3[1]<lan1[1] and lan3[1]<lan5[1] and lan3[1]<index_fin[1]:
                    volume = subprocess.check_output("osascript -e 'output volume of (get volume settings)'",shell=True)
                    volume = int(volume)
                    volume = min(volume + 5, 100)
                    os.system(f"osascript -e 'set volume output volume {volume}'")
                    cv2.putText(frame,str(volume),(60,height//2),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),3)
                    time.sleep(0.3)
                elif lan3[1]>lan1[1] and lan3[1]>lan5[1] and lan3[1]>index_fin[1]:
                    volume = subprocess.check_output("osascript -e 'output volume of (get volume settings)'",shell=True)
                    volume = int(volume)
                    volume = max(volume - 5, 0)
                    os.system(f"osascript -e 'set volume output volume {volume}'")
                    cv2.putText(frame,str(volume),(60,height//2),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),3)
                    time.sleep(0.3)


    #spotifyyy

                if index_up and middle_up and ring_down and pinky_down:
                    if time.time()-last_spotify>3:
                        webbrowser.open("https://open.spotify.com/")
                        last_spotify=time.time()

    #screenshot
                elif index_up and middle_up and ring_up and pinky_up:
                    if time.time()-last_ss>3:
                        img=pyautogui.screenshot()
                        img.save(f"screenshot_{time.ctime()}.png")
                        print("ss")
                        last_ss=time.time()     

    #toggle
            if index_down and middle_down and ring_down and pinky_down:
                if time.time()-last_on>2:
                    assistant_on=not assistant_on
                    last_on=time.time()

    if assistant_on:
            cv2.putText(frame,"ASSISTANT ON",(width//2-200,80),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,20),5)
    else:
            cv2.putText(frame,"ASSISTANT OFF",(width//2-200,80),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,20),5)

#Camera show/break
    cv2.imshow("Camera",frame)
    if cv2.waitKey(1)==ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

