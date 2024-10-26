#include <iostream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <cmath>

using namespace std;
using namespace cv;

// 计算两个点之间的距离
double calculateDistance(Point p1, Point p2) {
    return sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2));
}

// 计算直线与水平方向的夹角
double calculateAngle(Point pt1, Point pt2) {
    // 计算直线的斜率
    double deltaY = pt2.y - pt1.y;
    double deltaX = pt2.x - pt1.x;

    if (deltaX == 0) {
        return (deltaY > 0) ? 90.0 : -90.0;
    }

    // 计算夹角（以度为单位）
    double angle = atan2(deltaY, deltaX) * 180.0 / CV_PI;
    return angle;
}

int main() {

    Mat image = imread("input.jpg"); //图片路径
    if (image.empty()) {
        cout << "无法读取图片!" << endl;
        return -1;
    }

    // 转换为灰度图像
    Mat gray;
    cvtColor(image, gray, COLOR_BGR2GRAY);

    // 使用Canny算法检测边缘
    Mat edges;
    Canny(gray, edges, 50, 150);

    // 使用霍夫变换检测直线
    vector<Vec2f> lines;
    HoughLines(edges, lines, 1, CV_PI / 180, 100);

    // 找到最长的直线
    double maxLength = 0;
    Vec2f longestLine;
    for (const auto& line : lines) {
        float rho = line[0];
        float theta = line[1];

        // 计算直线的两个端点
        Point pt1(rho * cos(theta) + 1000 * (-sin(theta)), rho * sin(theta) + 1000 * (cos(theta)));
        Point pt2(rho * cos(theta) - 1000 * (-sin(theta)), rho * sin(theta) - 1000 * (cos(theta)));

        // 计算这条直线的长度
        double length = calculateDistance(pt1, pt2);
        if (length > maxLength) {
            maxLength = length;
            longestLine = line;
        }
    }


    if (maxLength > 0) {
        float rho = longestLine[0];
        float theta = longestLine[1];
        Point pt1(rho * cos(theta) + 1000 * (-sin(theta)), rho * sin(theta) + 1000 * (cos(theta)));
        Point pt2(rho * cos(theta) - 1000 * (-sin(theta)), rho * sin(theta) - 1000 * (cos(theta)));

        // 计算夹角
        double angle = calculateAngle(pt1, pt2);
        cout << "最长直线与水平方向的夹角: " << angle << " 度" << endl;

        // 在图像上绘制该直线
        line(image, pt1, pt2, Scalar(0, 0, 255), 2);
        imshow("Detected Line", image);
        waitKey(0);
    }
    else {
        cout << "未检测到直线!" << endl;
    }

    return 0;
}
