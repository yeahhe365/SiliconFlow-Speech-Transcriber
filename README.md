
---

# SiliconFlow 语音转录工具

![GitHub stars](https://img.shields.io/github/stars/yeahhe365/SiliconFlow-Speech-Transcriber.svg?style=social&label=Stars)
![GitHub forks](https://img.shields.io/github/forks/yeahhe365/SiliconFlow-Speech-Transcriber.svg?style=social&label=Fork)
![License](https://img.shields.io/github/license/yeahhe365/SiliconFlow-Speech-Transcriber)

**SiliconFlow 语音转录工具** 是一款基于 Python 和 PyQt5 开发的桌面应用程序，旨在通过调用 SiliconFlow 的语音转文本 API，将音频文件高效地转换为文本。无论您是内容创作者、研究人员还是需要文字整理的专业人士，本工具都能为您提供便捷、快速的转录体验。

## 目录

- [功能特性](#功能特性)
- [界面预览](#界面预览)
- [前置条件](#前置条件)
- [安装步骤](#安装步骤)
- [使用说明](#使用说明)
  - [启动应用](#启动应用)
  - [转录音频文件](#转录音频文件)
  - [编辑与管理转录结果](#编辑与管理转录结果)
  - [主题切换](#主题切换)
  - [首选项设置](#首选项设置)
- [配置说明](#配置说明)
- [参与贡献](#参与贡献)
- [许可证](#许可证)
- [致谢](#致谢)

## 功能特性

- **直观易用的界面**：用户友好的图形界面，轻松操作。
- **API 集成**：无缝连接 SiliconFlow 语音转文本 API。
- **多线程请求**：后台处理转录请求，不影响界面响应。
- **进度指示**：实时显示转录进度，用户可随时了解状态。
- **取消请求**：支持中途取消正在进行的转录任务。
- **设置持久化**：自动保存用户的 API Token、模型名称和最近使用的文件路径。
- **错误处理**：清晰的错误提示，帮助用户快速定位问题。
- **复制与导出**：一键复制转录文本或导出为文本文件，便于后续使用。
- **可编辑转录文本**：转录结果可直接在应用中编辑和校对。
- **主题切换**：支持深色与浅色主题切换，满足不同用户偏好。
- **响应式设计**：自适应不同屏幕尺寸，提供最佳使用体验。

## 界面预览

![image](https://github.com/user-attachments/assets/66355c39-f7b1-4e1b-893d-faaaeb055c02)

*图示：SiliconFlow 语音转录工具主界面*

## 前置条件

在安装和使用本工具之前，请确保您具备以下条件：

- **Python 3.6 或更高版本**：请从 [Python 官网](https://www.python.org/downloads/) 下载并安装。
- **Pip**：Python 的包管理工具，通常随 Python 一同安装。
- **SiliconFlow API 访问权限**：  
  - 首先在此处注册获得账号：[SiliconFlow 注册链接](https://cloud.siliconflow.cn/i/IymiJgdO)  
  - 然后前往 [SiliconFlow 官网](https://www.siliconflow.cn/) 获取您的 Bearer Token。

## 安装步骤

1. **克隆仓库**

   使用 Git 克隆本仓库到本地：

   ```bash
   git clone https://github.com/yeahhe365/SiliconFlow-Speech-Transcriber.git
   cd SiliconFlow-Speech-Transcriber
   ```

2. **创建虚拟环境（可选但推荐）**

   为了隔离项目依赖，建议创建并激活虚拟环境：

   ```bash
   python -m venv venv
   ```

   激活虚拟环境：

   - **Windows**：

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux**：

     ```bash
     source venv/bin/activate
     ```

3. **安装依赖**

   使用 `pip` 安装所需的 Python 包：

   ```bash
   pip install -r requirements.txt
   ```

   *如果没有提供 `requirements.txt` 文件，可手动安装依赖：*

   ```bash
   pip install PyQt5 requests
   ```

4. **运行应用**

   启动应用程序：

   ```bash
   python test.py
   ```

   *如果脚本名称不同，请将 `test.py` 替换为实际脚本名称。*

## 使用说明

### 启动应用

安装完成后，通过命令行运行以下命令启动应用：

```bash
python test.py
```

主界面将会显示，提供所有功能的入口。

### 转录音频文件

1. **输入 Bearer Token**

   - 点击菜单栏中的 **"设置" > "首选项"**。
   - 在弹出的对话框中输入从 SiliconFlow 获取的 **Bearer Token**。
   - 可选择勾选 **"显示 Token"** 以查看或隐藏 Token。

2. **选择模型**

   - 在主界面上部的 **"API 参数与文件选择"** 区域输入模型名称。
   - 例如：`FunAudioLLM/SenseVoiceSmall`（可根据实际需求更改模型）。

3. **选择音频文件**

   - 点击 **"选择文件"** 按钮，浏览并选择需要转录的音频文件（支持 `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg` 等格式）。

4. **提交转录请求**

   - 点击工具栏的 **"提交转录请求"** 按钮。
   - 应用将显示进度条，指示请求正在进行中。

5. **查看转录结果**

   - 转录完成后，转录文本将显示在 **"转录结果"** 区域。
   - 您可以直接在此区域编辑和校对文本。

### 编辑与管理转录结果

- **复制结果**

  - 点击工具栏的 **"复制"** 按钮，将转录文本复制到剪贴板。

- **导出结果**

  - 点击工具栏的 **"导出结果"** 按钮，将转录文本导出为 `.txt` 文件。

- **清空结果**

  - 点击工具栏的 **"清空结果"** 按钮，清除当前转录文本。

### 主题切换

- 在菜单栏 **"设置" > "切换主题"** 中，点击以在深色和浅色主题之间切换，适应不同的使用环境和个人偏好。

### 首选项设置

- **Bearer Token**：输入您的 SiliconFlow API 访问令牌。
- **Model**：指定用于转录的模型名称。
- 应用程序会自动保存您的配置和最近使用的文件路径，以便下次使用时自动加载。

## 配置说明

### API Token

请确保您已在 [SiliconFlow 注册链接](https://cloud.siliconflow.cn/i/IymiJgdO) 完成注册并获取账号，然后在 [SiliconFlow 官网](https://www.siliconflow.cn/) 获取有效的 **Bearer Token**。在 **"首选项"** 对话框中正确输入此 Token，以确保应用程序能够成功调用 API 进行转录。

### 模型选择

根据您的需求选择合适的转录模型。默认使用 `FunAudioLLM/SenseVoiceSmall`，但您也可以输入其他已在 SiliconFlow 注册的模型名称。

## 参与贡献

非常欢迎社区的贡献！如果您希望为本项目做出贡献，请按照以下步骤进行：

1. **Fork 本仓库**

2. **创建新分支**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **提交更改**

   ```bash
   git commit -m "Add your feature"
   ```

4. **推送到分支**

   ```bash
   git push origin feature/YourFeature
   ```

5. **发起 Pull Request**

   在 GitHub 上提交 Pull Request，并详细描述您的更改内容。我们将尽快审核并合并您的贡献。

## 许可证

本项目采用 [MIT License](LICENSE) 许可协议。详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro/)**：Python 的 Qt 应用程序框架绑定。
- **[SiliconFlow](https://www.siliconflow.cn/)**：提供语音转文本 API。
- **[Requests](https://requests.readthedocs.io/)**：优雅且简单的 Python HTTP 库。
- **[Shields.io](https://shields.io/)**：用于生成徽章。

---

