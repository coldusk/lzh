import cv2
import numpy as np


def detect_color_contours(image, lower_color, upper_color):
    """
    检测图像中指定颜色的轮廓。

    参数:
    - image: 输入的图像。
    - lower_color: HSV格式中颜色的下界。
    - upper_color: HSV格式中颜色的上界。

    返回:
    - 与指定颜色匹配的轮廓列表。
    """
    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 创建指定颜色的掩模
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # 在掩模中找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def mark_enclosing_circle_center(image, contours):
    """
    标记能包围所有指定颜色轮廓的最小包围圆的圆心。

    参数:
    - image: 在其上标记圆心的输入图像。
    - contours: 轮廓列表。

    返回:
    - 标记了圆心的图像。
    """
    if len(contours) == 0:
        return image

    # 将所有轮廓点合并为一个整体
    all_points = np.vstack(contours)

    # 计算最小包围圆
    (x, y), radius = cv2.minEnclosingCircle(all_points)
    center = (int(x), int(y))

    # 在圆心处画一个十字
    cv2.drawMarker(image, center, (0, 0, 0), markerType=cv2.MARKER_CROSS,
                   markerSize=20, thickness=2, line_type=cv2.LINE_AA)

    return image


def process_image(image_path, color_type):
    """
    处理图像，检测指定颜色的轮廓并标记能包围所有轮廓的最小包围圆的圆心。

    参数:
    - image_path: 输入图像的路径。
    - color_type: 颜色类型（'red', 'green', 'blue'）。

    返回:
    - 标记了圆心的图像。
    """
    # 读取图像
    image = cv2.imread(image_path)

    # 定义HSV颜色范围
    if color_type == 'red':
        # 红色可能跨越HSV色相范围的两个部分
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        contours1 = detect_color_contours(image, lower_red1, upper_red1)
        contours2 = detect_color_contours(image, lower_red2, upper_red2)
        contours = contours1 + contours2
    elif color_type == 'green':
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        contours = detect_color_contours(image, lower_green, upper_green)
    elif color_type == 'blue':
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        contours = detect_color_contours(image, lower_blue, upper_blue)

    # 标记最小包围圆的圆心
    output_image = mark_enclosing_circle_center(image, contours)

    return output_image


image_path = "image_path"  # 输入图像路径
color_type = 'red'  # 选择颜色类型（'red', 'green', 'blue'）

# 处理图像并获取输出
output_image = process_image(image_path, color_type)

# 展示结果图像
cv2.imshow('Detected', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
