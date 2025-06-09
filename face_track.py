import cv2
import numpy as np
import dlib
import os
import face_recognition
import time
import socket

# 获取电脑名称和IP地址
computer_name = socket.gethostname()
computer_ip = socket.gethostbyname(computer_name)

# 初始化Dlib的人脸检测器和特征点预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 初始化摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera!")
    exit()

# 设置摄像头分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 获取画面尺寸
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame!")
    exit()
height, width = frame.shape[:2]
center = (width // 2, height // 2)

# 创建窗口
cv2.namedWindow('AI Face Tracker', cv2.WINDOW_NORMAL)

# 科技感配色
COLOR_CENTER = (0, 255, 0)  # 中心点 - 绿色
COLOR_FACE = (0, 255, 255)  # 面部轮廓 - 黄色
COLOR_LINE = (255, 0, 255)  # 指引线 - 品红
COLOR_TEXT = (255, 255, 255)  # 文字 - 白色
COLOR_BG = (20, 20, 40)  # 背景色 - 深蓝

# 面部特征点连接规则（基于68点模型）
FACE_CONNECTIONS = [
    # 下巴轮廓
    list(range(0, 17)) + [0],
    # 左眉毛
    list(range(17, 22)),
    # 右眉毛
    list(range(22, 27)),
    # 鼻梁
    list(range(27, 31)),
    # 鼻子底部
    list(range(31, 36)),
    # 左眼
    list(range(36, 42)) + [36],
    # 右眼
    list(range(42, 48)) + [42],
    # 外嘴唇
    list(range(48, 60)) + [48],
    # 内嘴唇
    list(range(60, 68)) + [60]
]

# 加载已知人脸
known_face_encodings = []
known_face_names = []

# 从文件夹 'face' 中加载人脸图片
face_folder = 'face'
for filename in os.listdir(face_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(os.path.join(face_folder, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

# 日志记录
log_file = "face_log.txt"
current_name = None
last_seen_time = None

# 人脸识别线程
def recognize_face(face_image, face_location):
    face_encoding = face_recognition.face_encodings(face_image, [face_location])[0]
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
    return name

# 主循环
last_recognition_time = time.time()
recognition_interval = 1.0  # 每秒进行一次人脸识别
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 水平反转（镜像效果）
    frame = cv2.flip(frame, 1)  # 1 表示水平翻转

    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用Dlib检测人脸（更精确）
    faces = detector(gray, 0)

    # 绘制科技感中心十字线
    cv2.line(frame, (center[0] - 20, center[1]), (center[0] + 20, center[1]), COLOR_CENTER, 2)
    cv2.line(frame, (center[0], center[1] - 20), (center[0], center[1] + 20), COLOR_CENTER, 2)

    # 处理检测到的人脸
    if len(faces) > 0:
        # 获取最大的人脸
        face = max(faces, key=lambda f: f.width() * f.height())

        # 计算人脸面积
        face_area = face.width() * face.height()
        frame_area = width * height
        face_ratio = face_area / frame_area

        # 只有当人脸面积达到画面的1/4时才捕捉
        if face_ratio >= 0.07 and face_ratio <= 0.30:
            # 获取68个面部特征点
            landmarks = predictor(gray, face)
            points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]

            # 计算人脸中心（使用鼻子底部点作为参考）
            face_center = (points[30][0], points[30][1])  # 鼻尖点

            # 绘制面部轮廓（科技感线条）
            for connection in FACE_CONNECTIONS:
                for i in range(len(connection) - 1):
                    pt1 = points[connection[i]]
                    pt2 = points[connection[i + 1]]
                    cv2.line(frame, pt1, pt2, COLOR_FACE, 1, cv2.LINE_AA)

            # 绘制动态指引线（带箭头）
            cv2.arrowedLine(frame, center, face_center, COLOR_LINE, 2, tipLength=0.3)

            # 计算移动指令（非反转逻辑）
            move_x = ""
            move_y = ""

            # X轴方向判断
            if abs(face_center[0] - center[0]) > width * 0.1:
                if face_center[0] < center[0]:
                    move_x = "Move LEFT"
                else:
                    move_x = "Move RIGHT"

            # Y轴方向判断（非反转）
            if abs(face_center[1] - center[1]) > height * 0.1:
                if face_center[1] < center[1]:
                    move_y = "Move UP"
                else:
                    move_y = "Move DOWN"

            # 组合移动指令
            move_cmd = " & ".join(filter(None, [move_x, move_y])) or "Centered!"
            print(move_cmd)

            # 人脸识别
            current_time = time.time()
            if current_time - last_recognition_time > recognition_interval:
                face_location = (face.top(), face.right(), face.bottom(), face.left())  # (top, right, bottom, left)
                name = "Unknown"
                try:
                    name = recognize_face(frame, face_location)
                except Exception as e:
                    print(f"Recognition error: {e}")
                last_recognition_time = current_time

                # 如果识别到的人脸与之前不同，记录到日志
                if name != current_name:
                    if current_name is not None:
                        # 记录离开时间
                        leave_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        with open(log_file, "a") as f:
                            f.write(f"{current_name} left at {leave_time} on {computer_name} ({computer_ip})\n")
                    # 记录进入时间
                    enter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    with open(log_file, "a") as f:
                        f.write(f"{name} entered at {enter_time} on {computer_name} ({computer_ip})\n")
                    current_name = name

            # 在界面上显示识别出的人的姓名
            cv2.putText(frame, name, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_TEXT, 2)

            # 添加状态信息
            info_text = f"Face: ({face_center[0]}, {face_center[1]})"
            cv2.putText(frame, info_text, (20, 30),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, COLOR_TEXT, 1)

            # 添加科技感指令面板
            if name == "Unknown":
                cv2.rectangle(frame, (10, height - 50), (width - 10, height - 10), (0, 0, 255), -1)
            else:
                cv2.rectangle(frame, (10, height - 50), (width - 10, height - 10), (0, 255, 0), -1)
            cv2.putText(frame, f"NAME: {name}", (20, height - 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

    # 显示画面
    cv2.imshow('AI Face Tracker', frame)

    # 按ESC退出
    if cv2.waitKey(1) == 27:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

# 如果程序结束时还有人未离开，记录离开时间
if current_name is not None:
    leave_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, "a") as f:
        f.write(f"{current_name} left at {leave_time} on {computer_name} ({computer_ip})\n")