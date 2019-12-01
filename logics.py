import random
import cv2
import time
import numpy as np


# Hyper Parameters
speed = 4

"""
    Write you own logic to control the remote Android Device

    For example:
        input text "xxxx"   # send keyboard event
        input tap 50 250    # click event
"""


def get_man_pos(img):
    template = cv2.imread('./template.jpg')
    print(img.shape)
    detect_result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(detect_result)
    max_loc = (max_loc[0] + 25, max_loc[1] + 80)
    return max_loc


def get_end(img, start_pos):
    img_rgb = cv2.GaussianBlur(img, (5, 5), 0)
    canny_img = cv2.Canny(img_rgb, 1, 10)
    H, W = canny_img.shape
    # cv2.imshow('asdf', canny_img)
    # cv2.waitKey(0)

    y_top1 = np.nonzero([max(row[:max(0, start_pos[0]-20)])
                         for row in canny_img[200:]])[0][0] + 200
    print(y_top1)
    y_top2 = np.nonzero([max(row[min(start_pos[0]+20, img.shape[0]):])
                         for row in canny_img[200:]])[0][0] + 200
    print(y_top2)

    y_top = min(y_top1, y_top2)
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    y_bottom = y_top + 80
    for row in range(y_bottom, H):
        if np.mean(canny_img[row, x_top-5:x_top+5]) != 0:
            y_bottom = row
            break

    if y_bottom > y_top + 160:
        y_bottom = y_top + 80

    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return (x_center, y_center)


def get_order(img):
    img = cv2.resize(img, (400, 800))

    print('Detecting the start position.')
    start_pos = get_man_pos(img)
    print('The start position is', start_pos)
    print('Detecting the end position.')
    end_pos = get_end(img, start_pos)
    print('The end position is', end_pos)

    # img = cv2.circle(img, start_pos, 5, (0, 255, 0), -1)
    # img = cv2.circle(img, end_pos, 5, (0, 0, 255), -1)

    # cv2.imshow('name', img)
    # cv2.waitKey(0)

    rand1 = 500+random.randint(1, 300)
    rand2 = 1650+random.randint(1, 100)
    rand3 = rand1
    rand4 = rand2 + random.randint(1, 50)

    dis = ((start_pos[0] - end_pos[0]) ** 2 +
           (start_pos[1] - end_pos[1]) ** 2) ** 0.5
    dis = int(dis * speed)
    print('The time interval is', dis)
    print('Sending to the Android phone...')
    order = f'input swipe {rand1} {rand2} {rand3} {rand4} {dis}'
    return order


def get_commands(token, img_file):
    try:
        """ analyze the screenshot and send
            commands back to android device """
        img_file.save("tmp.png")
        print(token)
        img = cv2.imread('./tmp.png')

        # your adb shell commands
        cmds = [
            get_order(img)
        ]
        print('OK!\n\n')
        return cmds
    except Exception as err:
        print(err)
    finally:
        time.sleep(0.5)
