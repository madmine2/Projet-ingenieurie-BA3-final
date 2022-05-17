import cv2
# import the opencv library
import numpy as np
from gpiozero import Button
from signal import pause

from PIL import Image, ImageDraw

refLow = [[120, 40, 80], [45, 30, 50], [90, 40, 2], [10, 30, 105]]
refHigh = [[255, 255, 255], [90, 180, 255], [130, 255, 255], [45, 120, 255]]
ref2Low = [[0, 0, 60], [30, 120, 0], [90, 80, 2], [0, 80, 60]]
ref2High = [[60, 20, 150], [85, 255, 255], [110, 255, 255], [20, 100, 150]]


# refLow = ref2Low
# refHigh = ref2High


def findColor(frame, x, y, I):
    # take part of the image
    temp_x = x
    x = y
    y = temp_x
    temp_frame = frame[x - 10:x + 10, y - 10:y + 10]
    color = ["rouge", "vert", "bleu", "jaune"]
    color_id = ["1", "2", "3", "4"]

    color_dict = {"rouge": 0, "bleu": 0, "jaune": 0, "vert": 0}

    # make dict of the colors in the image
    for i in range(20):
        for j in range(20):
            for k in range(4):
                temp = False
                for l in range(3):
                    if temp_frame[i][j][l] < refLow[k][l] or temp_frame[i][j][l] > refHigh[k][l]:
                        temp = True
                if l == 0:
                    if temp_frame[i][j][1] < 10 and temp_frame[i][j][1] >= refLow[k][1] and temp_frame[i][j][1] <= \
                            refHigh[k][1] and temp_frame[i][j][2] >= 70 and temp_frame[i][j][2] <= refHigh[k][2]:
                        temp = False
                if temp == False:
                    color_dict[color[k]] += 1

    # Sort them by count number(first element of tuple)
    temppp = 0
    color_dom = "0"
    for i in range(4):
        if color_dict[color[i]] >= temppp:
            temppp = color_dict[color[i]]
            color_dom = color_id[i]

    return color_dom


def capture_video(last, button):
    face_colour = []
    # define a video capture object
    vid = cv2.VideoCapture(0)
    if vid.isOpened() == False:
        print("changement")
        vid = cv2.VideoCapture(1)
    else:
        print("good")
    if vid.isOpened() == False:
        vid = cv2.VideoCapture("/dev/video1")

    pos = 0
    temp = 0
    ret, frame = vid.read()
    # cv2.imwrite('/home/pi/Desktop/test.png', frame)
    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        frame = Image.fromarray(frame)

        draw = ImageDraw.Draw(frame, "RGBA")
        if last:
            coordTriangleX = [300, 400, 300, 200, 500, 400, 300, 200, 100]
        else:
            coordTriangleX = [300, 200, 300, 400, 100, 200, 300, 400, 500]
        coordTriangleY = [50, 250, 200, 250, 400, 350, 400, 350, 400]
        for i in range(9):
            x = coordTriangleX[i]
            y = coordTriangleY[i]

            draw.rectangle((x - 10, y - 10, x + 10, y + 10), outline=(0, 0, 0, 125))
        draw.rectangle((300 - 2, 200 - 2, 300 + 2, 200 + 2), outline=(100, 100, 100, 125))
        frame = np.array(frame)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #         if cv2.waitKey(1) & 0xFF == ord('p'):
        #             print(hsv_frame[50,300])

        if button.is_pressed:
            face_temp = []
            for i in range(9):
                x = coordTriangleX[i]
                y = coordTriangleY[i]

                face_temp.append(int(findColor(hsv_frame, x, y, i)))

            print(face_temp)
            #             vid.release()
            # Destroy all the windows
            #             cv2.destroyAllWindows()
            return face_temp


#-----------------------------------
#Décommenter le code qui suit pour afficher les vues de la caméra
#-----------------------------------

#         # Red color
#         low_red = np.array(refLow[0])
#         low_red2 = np.array([0,0, 0])
#         high_red = np.array(refHigh[0])
#         high_red2 = np.array([10 , 255, 255])
#         red_mask = cv2.inRange(hsv_frame, low_red, high_red)
#         red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
#         red = cv2.bitwise_and(frame, frame, mask=red_mask)
#         red2 = cv2.bitwise_and(frame, frame, mask=red_mask2)
#         # Blue color
#         low_blue = np.array(refLow[2])
#         high_blue = np.array(refHigh[2])
#         blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
#         blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
#         # Green color
#         low_green = np.array(refLow[1])
#         high_green = np.array(refHigh[1])
#         green_mask = cv2.inRange(hsv_frame, low_green, high_green)
#         green = cv2.bitwise_and(frame, frame, mask=green_mask)
#         # Yellow color
#         low_yellow = np.array(refLow[3])
#         high_yellow = np.array(refHigh[3])
#         yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
#         yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
#         cv2.imshow("Frame", frame)
#         #cv2.imshow("Hsv_Frame", hsv_frame)
#
#         cv2.imshow("Red", red)
#         cv2.imshow("Red2", red2)
#         cv2.imshow("Blue", blue)
#         cv2.imshow("Green", green)
#         cv2.imshow("Yellow", yellow)
#
# the 'q' button is set as the
# quitting button you may use any
# desired button of your choice
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         if cv2.waitKey(1) & 0xFF == ord('s'):
#             pos +=1
#             if pos > 5  :
#                 pos = 0

# After the loop release the cap object
#     vid.release()
# Destroy all the windows
#     cv2.destroyAllWindows()
# Press the green button in the gutter to run the script.

def main():
    matrix = []
    for i in range(4):
        matrix.append()


if __name__ == '__main__':
    capture_video()

