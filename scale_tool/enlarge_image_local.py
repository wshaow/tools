# -*- coding:utf-8 -*-
"""
A local image scale tool
Licensed under The MIT License
Writen by Shaowu Wu, 20190926
"""
import cv2.cv2 as cv
import numpy as np
import os

LINE_COLOR = (0, 255, 0)  # 获取在原图上画的线的颜色
LINE_WIDTH = 2  # 在原图上线的宽度
SCALE = 2  # 对选取区域的放大倍数
ADD_BBOX = True  # 是否对要保存的图像增加边框
BBOX_WIDTH = 4   # 增加的边框的宽度
BBOX_COLOR = (255, 255, 255)  # 默认为白色
INTER_METHOD = cv.INTER_LINEAR  # 默认使用最近邻, 双三次INTER_CUBIC, INTER_LANCZOS4, INTER_LINEAR


point1 = (-1, -1)
point2 = (-1, -1)
G_RECT = []
global img, g_rect  # g_rect是选择的感兴趣的区域[min_x, min_y, width, height]


def read_image(path):
    img = cv.imread(path)
    return img


def draw_circle(event, x, y, flags, param):
    global point1, img, G_RECT
    img2 = img.copy()  # 这里必须要拷贝一个新的
    if event == cv.EVENT_LBUTTONDOWN:  # 获取左上角的坐标
        point1 = x, y
        print("point1: ",point1)
        # 画图的时候是先在img2数据上进行处理，之后再将其显示出来
        cv.circle(img2, point1, 10, LINE_COLOR, LINE_WIDTH)
        cv.imshow("ori_image", img2)
    elif event == cv.EVENT_MOUSEMOVE and (flags & cv.EVENT_FLAG_LBUTTON):
        cv.rectangle(img2, point1, (x, y), LINE_COLOR, LINE_WIDTH)
        cv.imshow("ori_image", img2)

    elif event == cv.EVENT_LBUTTONUP:  # 鼠标左键按钮松开的时候画图
        point2 = x, y
        print("point2", point2)
        if point1 != point2:
            min_x = min(point1[0], point2[0])
            min_y = min(point1[1], point2[1])
            width = abs(point1[0] - point2[0])
            height = abs(point1[1] - point2[1])
            G_RECT = [min_x, min_y, width, height]
            print("g_rect: ", G_RECT)
            cv.rectangle(img2, point1, point2, LINE_COLOR, LINE_WIDTH)

        cv.imshow('ori_image', img2)


def get_ROI():
    global img
    scaled_image = []
    while True:
        cv.namedWindow('ori_image')
        cv.setMouseCallback('ori_image', draw_circle)
        cv.imshow('ori_image', img)
        k = cv.waitKey(0)
        if k == 32:  # 空格键化出对比图
            scaled_image = get_compair_imgs(imgs)
            plot_compair_imgs(scaled_image, img_names)
        if k == 13:  # 回车键退出
            break

    return scaled_image


def scale_image(img, scale, inter_mathod):
    width, height, chl = img.shape
    dst = cv.resize(img, (height*scale, width*scale), interpolation=inter_mathod)
    return dst


def add_borders(img):
    borderType = cv.BORDER_CONSTANT
    dst = cv.copyMakeBorder(img, BBOX_WIDTH, BBOX_WIDTH, BBOX_WIDTH, BBOX_WIDTH, borderType, value=BBOX_COLOR)
    return dst


def get_scale_image(img):
    roi_img = img[G_RECT[1]:G_RECT[1] + G_RECT[3], G_RECT[0]:G_RECT[0] + G_RECT[2]]  # 提取选择的区域
    scaled_image = scale_image(roi_img, SCALE, INTER_METHOD)  # 对选择的区域放大
    add_borders_img = add_borders(scaled_image)  # 增加边框
    return add_borders_img


def read_imgs(path):
    global img
    g = os.walk(path)
    imgs = []
    img_names = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if "_ROI" in file_name:
                img = read_image(os.path.join(path, file_name))
            else:
                imgs.append(read_image(os.path.join(path, file_name)))
                img_names.append(file_name.split(".")[0])
    return imgs, img_names


def get_compair_imgs(imgs):
    compair_imgs = []
    for img in imgs:
        if ADD_BBOX:
            compair_imgs.append(get_scale_image(img))
        else:
            compair_imgs.append(img)
    return compair_imgs


def plot_compair_imgs(compair_imgs, imgs_name):
    n = len(compair_imgs)
    ori_img = get_scale_image(img)
    h1 = compair_imgs[0]
    h2 = ori_img
    for i in range(1, n):
        h1 = np.hstack((h1, compair_imgs[i]))
        h2 = np.hstack((h2, ori_img))
    h1 = np.vstack((h1, h2))
    cv.imshow("C", h1)
    print(imgs_name)


def save_scale_image(imgs, img_names):
    if not os.path.exists(".\\result\\scale_image\\"):
        os.makedirs(".\\result\\scale_image\\")
    for i in range(len(imgs)):
        cv.imwrite(".\\result\\scale_image\\" + img_names[i] + ".bmp", imgs[i])
    cv.imwrite(".\\result\\scale_image\\"  + "ori_image.bmp", get_scale_image(img))


def save_big_image(images, image_names):
    if not os.path.exists(".\\result\\big_image\\"):
        os.makedirs(".\\result\\big_image\\")
    for i in range(len(images)):
        cv.rectangle(images[i], (G_RECT[0], G_RECT[1]), (G_RECT[0] + G_RECT[2], G_RECT[1] + G_RECT[3]), LINE_COLOR, LINE_WIDTH)
        cv.imwrite(".\\result\\big_image\\" + image_names[i] + ".bmp", imgs[i])

    cv.rectangle(img, (G_RECT[0], G_RECT[1]), (G_RECT[0] + G_RECT[2], G_RECT[1] + G_RECT[3]), LINE_COLOR,
                 LINE_WIDTH)
    cv.imwrite(".\\result\\big_image\\" + "ori.bmp", img)


if __name__ == '__main__':

    # 单幅图像的放大
    # global img
    # path = "j20.PNG"
    # img = read_image(path)
    # img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    # get_ROI()
    # add_borders_img = get_scale_image(img)
    # cv.imshow("roi", add_borders_img)

    # 多幅图像的放大的比对
    path = ".\\imgs"
    imgs, img_names = read_imgs(path)

    scaled_image = get_ROI()

    save_scale_image(scaled_image, img_names)
    save_big_image(imgs, img_names)
    cv.destroyAllWindows()
