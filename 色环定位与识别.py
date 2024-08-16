import cv2
import numpy as np

def detect_circles_and_colors(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    output = image.copy()

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用HoughCircles检测圆，参数主要调整param2，越大越精确
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=200, minRadius=0, maxRadius=0)

    if circles is not None:
        # 将圆坐标和半径转换为整数
        circles = np.round(circles[0, :]).astype("int")

        # 初始化存储坐标的列表
        x_coords = []
        y_coords = []

        for (x, y, r) in circles:
            # 将圆心坐标加入列表
            x_coords.append(x)
            y_coords.append(y)

            # 提取色环区域
            mask = np.zeros_like(gray)  # np.zeros_like函数返回与给定数组具有相同形状和类型的新数组，但新数组的所有元素都是0
            cv2.circle(mask, (x, y), r, 255, thickness=-1)
            masked_image = cv2.bitwise_and(image, image, mask=mask)

            # 提取色环区域内的所有像素
            pixels = masked_image[mask == 255]
            pixels = pixels.reshape(-1, 3)

            # 统计红绿蓝三种颜色的像素数量
            red_count = np.sum((pixels[:, 2] > 100) & (pixels[:, 1] < 100) & (pixels[:, 0] < 100))
            green_count = np.sum((pixels[:, 1] > 100) & (pixels[:, 2] < 100) & (pixels[:, 0] < 100))
            blue_count = np.sum((pixels[:, 0] > 100) & (pixels[:, 2] < 100) & (pixels[:, 1] < 100))

            # 判断主要颜色
            if red_count > green_count and red_count > blue_count:
                ring_color = "Red"
            elif green_count > red_count and green_count > blue_count:
                ring_color = "Green"
            elif blue_count > red_count and blue_count > green_count:
                ring_color = "Blue"
            else:
                ring_color = "Unknown"

        # 计算圆心坐标的平均值
        avg_x = int(np.mean(x_coords))
        avg_y = int(np.mean(y_coords))

        # 在输出图像中绘制平均圆心位置的小十字
        cv2.drawMarker(output, (avg_x, avg_y), (0, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # 显示带有标注的图像
    cv2.imshow("Detected Circles", output)
    print(ring_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 调用函数，传入图片路径
detect_circles_and_colors("image_path")


