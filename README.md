# AI Face Tracker
## 简介
AI Face Tracker 是一个使用 Python 和 OpenCV、Dlib、face_recognition 库实现的人脸跟踪和识别程序。该程序可以实时跟踪人脸，计算人脸在画面中的位置并给出移动指令，同时进行人脸识别并记录人员的进出时间。
## 功能特点
1. 人脸跟踪：使用 Dlib 人脸检测器和特征点预测器实时跟踪人脸。
2. 人脸识别：可以识别已知人脸，并记录人员的进出时间到日志文件。
3. 科技感界面：使用科技感配色绘制中心十字线、面部轮廓、指引线等。
4. 移动指令：根据人脸位置给出移动指令，如向左、向右、向上、向下移动。
## 安装依赖
在运行此程序之前，需要安装以下 Python 库：
```bash
pip install -r requirements.txt
```
同时，需要下载`shape_predictor_68_face_landmarks.dat`文件，并将其放在程序同一目录下。可以从[Dlib 官方网站](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)下载。
## 使用方法
1. 将已知人脸图片放入`face`文件夹中，文件名即为人员姓名。
2. 运行`face_track.py`文件：
```bash
python face_track.py
```
3. 程序将打开摄像头并开始实时跟踪和识别。
4. 按 ESC 键退出程序。
## 日志记录
程序会将人员的进出时间记录到`face_log.txt`文件中，格式如下：
```plaintext
{name} entered at {enter_time} on {computer_name} ({computer_ip})
{name} left at {leave_time} on {computer_name} ({computer_ip})
```
## 代码结构
1. `face_track.py`：主程序文件，包含人脸跟踪、识别和日志记录的主要逻辑。 
2. `face_track2.0.py`：主程序2.0文件，包含人脸跟踪、识别和日志记录的主要逻辑。 
3. `face`文件夹：存放已知人脸图片。
4. `shape_predictor_68_face_landmarks.dat`：Dlib 人脸特征点预测器模型文件。
5. `face_log.txt`：日志文件，记录人员的进出时间。
## 注意事项
1. 请确保摄像头正常工作，程序才能正常运行。
2. 已知人脸图片的文件名应为人员姓名，文件格式应为 `.jpg`、`.jpeg` 或 `.png`。
3. 人脸识别的准确性可能受到光照、角度等因素的影响。
## 贡献
如果你有任何建议或发现了问题，请在 GitHub 上提交 [issue](https://github.com/Jessssssseea/AI-Face-Tracker/issues) 或 [pull request](https://github.com/Jessssssseea/AI-Face-Tracker/pulls)。
## 许可证
本项目采用[MIT 许可证](https://opensource.org/license/MIT)。
