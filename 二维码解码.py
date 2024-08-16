import cv2
from pyzbar import pyzbar


def decode_qr_code(image_path):
    # 读取图像，保持原尺寸
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # cv2.imshow("import",image)
    # 使用pyzbar解码二维码
    decoded_objects = pyzbar.decode(image)

    for obj in decoded_objects:
        # 输出二维码中的数据
        print("Data:", obj.data.decode("utf-8"))
        # 输出二维码类型
        # print("Type:", obj.type)
        # # 获取二维码的位置
        # (x, y, w, h) = obj.rect
        # # 在图像中绘制矩形框
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示带框的图像
    # cv2.imshow("QR Code", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 调用函数，传入图片路径
decode_qr_code("C:\\Users\\24787\\Documents\\Tencent Files\\2478723753\\FileRecv\\MobileFile\\1723772857934.jpg")

#"C:/Users/24787/Documents/Tencent Files/2478723753/FileRecv/MobileFile/IMG20240816093852.jpg"