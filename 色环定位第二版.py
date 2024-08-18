import cv2
import numpy as np

def detect_color_contours(image, lower_hsv, upper_hsv):
    # 将图像从BGR转换为HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 使用颜色阈值找到指定颜色的区域
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    # 进行形态学操作，去除噪声
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def detect_color(image_path, color_type):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像，请检查路径是否正确")
        return

    # 定义HSV颜色范围（扩展范围）
    if color_type == 'red':
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        contours1 = detect_color_contours(image, lower_red1, upper_red1)
        contours2 = detect_color_contours(image, lower_red2, upper_red2)
        contours = contours1 + contours2
    elif color_type == 'green':
        lower_green = np.array([30, 40, 40])
        upper_green = np.array([90, 255, 255])
        contours = detect_color_contours(image, lower_green, upper_green)
    elif color_type == 'blue':
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        contours = detect_color_contours(image, lower_blue, upper_blue)

    # 将所有轮廓点合并
    all_points = np.vstack(contours)

    # 找到所有轮廓点的最小矩形
    rect = cv2.minAreaRect(all_points)
    box = cv2.boxPoints(rect)
    box = np.int32(box)  # 使用np.int32代替np.int0

    # # 在原图上绘制矩形
    # cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

    # 计算矩形的中心点
    center = (int(rect[0][0]), int(rect[0][1]))

    # 绘制十字标记中心点
    cv2.drawMarker(image, center, (0, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # 显示结果图像
    cv2.imshow("Detected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_path = "image_path"
color_type = 'green'  # 'red', 'green', 或 'blue'

detect_color(image_path, color_type)
