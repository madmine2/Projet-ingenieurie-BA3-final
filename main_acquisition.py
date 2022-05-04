import cv2
# import the opencv library
import numpy as np


from PIL import Image, ImageDraw


refLow = [[165, 80, 150], [55, 30, 50], [90, 80, 2], [10, 40, 105]]
refHigh = [[184, 255, 255], [85, 255, 255], [110, 255, 255], [50, 255, 255]]
ref2Low = [[0, 0, 60], [30, 120, 0], [90, 80, 2], [0, 80, 60]]
ref2High = [[60, 20, 150], [85, 255, 255], [110, 255, 255], [20, 100, 150]]
# refLow = ref2Low
# refHigh = ref2High


def findColor(frame,x,y, I) :
    #take part of the image
    temp_x = x
    x = y
    y = temp_x
    temp_frame = frame[x-10:x+10, y-10:y+10]
    color = ["rouge","vert","bleu","jaune"]
    color_id = ["1","2","3","4"]

    color_dict = {"rouge" : 0, "bleu":0,"jaune": 0,"vert":0}

    #make dict of the colors in the image
    for i in range(20):
        for j in range(20):
            for k in range(4):
                temp = False
                for l in range(3):
                    if temp_frame[i][j][l] < refLow[k][l] or temp_frame[i][j][l] > refHigh[k][l]:
                        temp = True
                # if l == 0:
                #     if temp_frame[i][j][1] < 10  and  temp_frame[i][j][1] >= refLow[k][1] and  temp_frame[i][j][1] <= refHigh[k][1] and temp_frame[i][j][2] >= 70 and  temp_frame[i][j][2] <= refHigh[k][2]:
                #         temp = False
                if temp == False:
                   color_dict[color[k]] +=1

    # Sort them by count number(first element of tuple)
    temppp = 0
    color_dom ="0"
    for i in range(4):
        if color_dict[color[i]] >= temppp:
            temppp = color_dict[color[i]]
            color_dom = color_id[i]

    return color_dom




def capture_video():
    face_colour = []
    # define a video capture object
    vid = cv2.VideoCapture(1)
 
    pos = 0
    temp = 0

    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        frame = Image.fromarray(frame)

        draw = ImageDraw.Draw(frame, "RGBA")

        coordTriangleX = [300,200,300,400,100,200,300,400,500]
        coordTriangleY = [50,250,200,250,400,350,400,350,400]
        for i in range(9):

            x = coordTriangleX[i]
            y = coordTriangleY[i]

            draw.rectangle((x - 10, y - 10, x + 10, y + 10), outline=(0, 0, 0, 125))
        draw.rectangle((300 - 2, 200 - 2, 300 + 2, 200 + 2), outline=(100, 100, 100, 125))
        frame = np.array(frame)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            print(hsv_frame[200,300])

        if cv2.waitKey(1) & 0xFF == ord(' '):
            face_temp = []
            for i in range(9):

                x = coordTriangleX[i]
                y = coordTriangleY[i]
                face_temp.append( int(findColor(hsv_frame, x, y, i)))
                print(face_temp)


            print(face_temp)
            vid.release()
            # Destroy all the windows
            cv2.destroyAllWindows()
            return face_temp

        # Red color
        low_red = np.array(refLow[0])
        low_red2 = np.array([0,80, 70])
        high_red = np.array(refHigh[0])
        high_red2 = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)
        red2 = cv2.bitwise_and(frame, frame, mask=red_mask2)


        # Blue color
        low_blue = np.array(refLow[2])
        high_blue = np.array(refHigh[2])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
        # Green color
        low_green = np.array(refLow[1])
        high_green = np.array(refHigh[1])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)
        # Yellow color
        low_yellow = np.array(refLow[3])
        high_yellow = np.array(refHigh[3])
        yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        cv2.imshow("Frame", frame)
        #cv2.imshow("Hsv_Frame", hsv_frame)

        cv2.imshow("Red", red)
        #cv2.imshow("Red2", red2)
        cv2.imshow("Blue", blue)
        cv2.imshow("Green", green)
        cv2.imshow("Yellow", yellow)
















        #
        # # variables pour les carré de mesure de couleur
        # decalage = 130
        # departx = 100
        # departy = 70
        # largeur = 80
        # finx = departx + largeur
        # finy = departy + largeur
        #
        # # couleurs du rubik's cube
        # rgbCube = [([0, 150, 67], [10, 160, 77]), ([180, 0, 0], [190, 10, 10]), ([0, 64, 168], [10, 74, 178]),
        #            ([245, 84, 0], [255, 94, 10]), ([245, 245, 245], [255, 255, 255]), ([245, 203, 0], [255, 213, 10])]
        # rgbCube2 = [(0, 155, 72),(255, 255, 255),(183, 18, 52),(255, 213, 0),(0, 70, 173),(255, 88, 0)]
        # cube_color = ["vert", "blanc", "rouge", "jaune", "bleu", "orange"]
        #
        #
        # if time.time() >= time_saved + 10000 or (cv2.waitKey(1) & 0xFF == ord(' ')):
        #     time_saved = time.time()
        #     print("COULEURS : ")
        #     #transform frame from bgr (opencv) color to rgb (pillow) and make it an nparray
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     pixels = np.array(frame)
        #     #show whole image
        #     plt.imshow(frame)
        #     plt.show()
        #     for i in range(3):
        #         for j in range(3):
        #             #take part of the image
        #             temp_frame = frame[departy+decalage*j:finy+decalage*j, departx+decalage*i:finx+decalage*i]
        #             #make it a pillow image
        #             temp_frame = Image.fromarray(temp_frame)
        #             #transform it to rgb
        #             temp_frame.convert("RGB")
        #             #make dict of the colors in the image
        #             pixels = temp_frame.getcolors(maxcolors=1000000)
        #             # Sort them by count number(first element of tuple)
        #             sorted_pixels = sorted(pixels, key=lambda t: t[0])
        #             # Get the most frequent color
        #             dominant_color = sorted_pixels[-1][1]
        #             #find closest color
        #             temp_color = 0
        #             temp_distance = float('inf')
        #             counting = 0
        #             for color in  rgbCube2:
        #                 if (abs(dominant_color[0]-color[0])+abs(dominant_color[1]-color[1])+abs(dominant_color[2]-color[2]) < temp_distance):
        #                     temp_distance = abs(dominant_color[0]-color[0])+abs(dominant_color[1]-color[1])+abs(dominant_color[2]-color[2])
        #                     temp_color =counting
        #                 counting +=1
        #             #print the color of the face
        #             print(cube_color[temp_color])
        #
        #
        #
        #
        #
        #
        # frame = Image.fromarray(frame)
        # draw = ImageDraw.Draw(frame, "RGBA")
        #
        # for i in range(3):
        #     for j in range(3) :
        #         draw.rectangle((departx+decalage*i,departy+decalage*j,finx+decalage*i,finy+decalage*j),outline=(255,255,255,127))
        # frame = np.array(frame)
        #
        # cv2.imshow("frame", frame)







        #
        # lower = rgbCube[pos][0]
        # upper = rgbCube[pos][1]
        # for i in range(len(lower)) :
        #     lower[i] -= 50
        #     if lower[i] < 0:
        #         lower[i] = 0
        # for i in range(len(upper)):
        #     upper[i] += 50
        #     if upper[i] > 255:
        #         upper[i] = 255
        # # create NumPy arrays from the boundaries
        # lower = np.array(lower, dtype="uint8")
        # upper = np.array(upper, dtype="uint8")
        #
        # # find the colors within the specified boundaries and apply
        # # the mask
        # mask = cv2.inRange(frame, lower, upper)
        # output = cv2.bitwise_and(frame, frame, mask=mask)
        # #cv2.imshow("frame", output)
        # if temp == 0:
        #     print(frame.shape)
        #     print(output.shape)
        #     temp +=1
        # # show the images
        # cv2.imshow("frame", np.hstack([output, frame]))


        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            pos +=1
            if pos > 5  :
                pos = 0

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
# Press the green button in the gutter to run the script.

def main():
    matrix = []
    for i in range(4):
        matrix.append()

if __name__ == '__main__':
    capture_video()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
