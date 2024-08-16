import cv2
import numpy as np


def detect_and_mark_color_objects(image_path, color_type):
    # 定义颜色范围（根据你指定的颜色类型）
    color_ranges = {
        "red": ([0, 50, 50], [10, 255, 255]),  # 红色范围（HSV）
        "green": ([40, 50, 50], [80, 255, 255]),  # 绿色范围（HSV）
        "blue": ([100, 50, 50], [140, 255, 255])  # 蓝色范围（HSV）
    }

    # 读取图像
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 根据颜色类型获取颜色范围
    lower_color = np.array(color_ranges[color_type][0])
    upper_color = np.array(color_ranges[color_type][1])

    # 创建颜色掩膜
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # 使用形态学操作去噪点
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # 查找颜色区域的轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # 忽略小的轮廓区域
            # 获取轮廓的边界框
            x, y, w, h = cv2.boundingRect(contour)

            # 在原图上画出白色矩形框
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

            # 计算物体的中心点
            center_x = x + w // 2
            center_y = y + h // 2

            # 在中心点处画白色十字标记
            cv2.drawMarker(image, (center_x, center_y), (255, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=20,
                           thickness=2)

    # 显示标记后的图像
    cv2.imshow("Detected Color Objects", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# 调用函数，传入图片路径和颜色类型
detect_and_mark_color_objects("C:\\Users\\24787\\Desktop\\1723777700678.jpg", "red")  # 颜色类型可以是 "red", "green", "blue"
