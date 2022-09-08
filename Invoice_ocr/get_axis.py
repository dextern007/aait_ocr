import cv2
import numpy as np
import pytesseract
import translators as ts


def remove_border_lines(image):
    result = image.copy()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)[1]

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255,255,255), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255,255,255), 5)
    # cv2.waitKey()
    cv2.imwrite("result.jpg",result)
    return result

remove_border_lines(cv2.imread("0.jpg"))

flag = False
ix = -1
iy = -1
l = []

def crop(event,x,y,flags,params):
    global  flag ,ix,iy , l
    if event == 1:
        flag =2
        ix = x
        iy = y

    elif event == 0:
        if flag == True:
            cv2.rectangle(img,pt1=(ix,iy),pt2=(x,y),thickness=1,color=(0,0,0))

    elif event == 4:
        fx = x
        fy = y
        flag = False
        cv2.rectangle(img,pt1=(ix,iy),pt2=(x,y),thickness=1,color=(0,0,0))

        cropped = img[iy:fy,ix:fx]
        print([iy,fy,ix,fx])
        cv2.imwrite("cropped.png",cropped)
        extraction = pytesseract.image_to_string(cropped,lang="chi_sim+eng")
        print(extraction)
        txt  = ts.bing(extraction,to_language='en')
        print(txt)
        # print(l)


img = cv2.imread("result.jpg")

cv2.namedWindow("windows", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("windows",crop)

while True:
    cv2.imshow("windows",img)

    if cv2.waitKey(1) & 0xFF == ord("x"):
        break

cv2.destroyAllWindows()

positions = [
[219, 333, 10, 1027],
[341, 447, 10, 1026],
[438, 519, 17, 2254],
[319, 421, 1034, 1820],
[105, 433, 1812, 2250],
[74, 194, 614, 1777],
[576, 674, 1558, 2023],
[1021, 1115, 1269, 1525],
[1128, 1209, 1302, 1551],
[1229, 1317, 1317, 1545],
[1342, 1436, 37, 267],
[1334, 1440, 279, 1579],
[1448, 1598, 34, 2260],
[289, 439, 84, 382],
[291, 430, 642, 1130],
[54, 212, 788, 1125],
[530, 672, 71, 399],
[528, 640, 786, 1112],
[1546, 1712, 66, 733],
[1548, 1693, 724, 1181],
[20, 93, 149, 426],
[100, 187, 141, 347],
[182, 210, 144, 286],
[211, 244, 145, 391],
[73, 249, 496, 720],
[86, 241, 803, 1134],
[16, 79, 748, 976],
[384, 484, 49, 319],
[375, 491, 652, 1022],
[56, 124, 125, 405],
[25, 172, 458, 809],
[76, 155, 1046, 1198],
[132, 298, 23, 465],
[347, 413, 1048, 1207],
[643, 698, 759, 876],
[704, 739, 760, 871],
[752, 803, 757, 869],
[640, 701, 878, 1169],
[691, 760, 879, 1166],
[752, 782, 879, 1103],
[790, 848, 881, 1182],
[41, 144, 424, 793],
[144, 293, 424, 850],
[278, 364, 383, 853],
[362, 407, 323, 552],
[410, 495, 332, 880],
[956, 1163, 331, 913],
[1181, 1322, 316, 795],
[1341, 1499, 305, 902],
[1522, 1717, 303, 879],
[23, 181, 438, 823],
[144, 208, 21, 331],
[201, 256, 31, 451],
[243, 293, 30, 288],
[293, 338, 29, 1170],
[198, 251, 844, 1050],
[1494, 1544, 844, 924],
[1554, 1591, 861, 917],
[1596, 1633, 851, 919],
[1631, 1670, 665, 922],
[1490, 1713, 910, 1214],

#bottom

[1241, 1445, 582, 1223],
[1372, 1574, 909, 1251],
[1392, 1549, 30, 777],
]