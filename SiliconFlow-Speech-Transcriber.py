import sys
import time
import requests

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings, QSize
from PyQt5.QtGui import QClipboard, QPalette, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QFileDialog, QAction,
                             QMessageBox, QCheckBox, QGroupBox, QGridLayout, QStatusBar, QProgressBar,
                             QDialog, QDialogButtonBox, QFormLayout, QSplitter, QToolBar, QStyle)


class RequestThread(QThread):
    finished_signal = pyqtSignal(object, float)  # 用于传递响应结果或异常和请求耗时
    running = True

    def __init__(self, token, model_name, file_path, parent=None):
        super().__init__(parent)
        self.token = token
        self.model_name = model_name
        self.file_path = file_path

    def run(self):
        url = "https://api.siliconflow.cn/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        start_time = time.time()
        try:
            with open(self.file_path, 'rb') as f:
                files = {
                    'file': f
                }
                data = {
                    'model': self.model_name
                }

                if not self.running:
                    self.finished_signal.emit(None, 0)
                    return

                response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
                elapsed = time.time() - start_time
                if self.running:
                    self.finished_signal.emit(response, elapsed)
                else:
                    self.finished_signal.emit(None, 0)
        except Exception as e:
            elapsed = time.time() - start_time
            if self.running:
                self.finished_signal.emit(e, elapsed)
            else:
                self.finished_signal.emit(None, 0)

    def cancel(self):
        self.running = False


class PreferencesDialog(QDialog):
    """首选项对话框，用于编辑Token和Model。"""
    def __init__(self, token, model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("首选项")
        self.token = token
        self.model = model
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.token_edit = QLineEdit(self.token)
        self.token_edit.setEchoMode(QLineEdit.Password if not self.token else QLineEdit.Normal)
        self.show_token_cb = QCheckBox("显示 Token")
        self.show_token_cb.setChecked(bool(self.token) and self.token_edit.echoMode() == QLineEdit.Normal)
        self.show_token_cb.toggled.connect(self.toggle_token_visibility)
        token_hlayout = QHBoxLayout()
        token_hlayout.addWidget(self.token_edit)
        token_hlayout.addWidget(self.show_token_cb)

        self.model_edit = QLineEdit(self.model)

        layout.addRow("Bearer Token:", token_hlayout)
        layout.addRow("Model:", self.model_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setContentsMargins(0, 10, 0, 0)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def toggle_token_visibility(self, checked):
        if checked:
            self.token_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.token_edit.setEchoMode(QLineEdit.Password)

    def get_values(self):
        return self.token_edit.text().strip(), self.model_edit.text().strip()


class TranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.request_thread = None
        self.settings = QSettings("MyCompany", "SiliconFlowSpeechTranscriber")

        # 读取上次主题选择，默认为深色主题
        self.dark_theme_enabled = self.settings.value("dark_theme_enabled", True, type=bool)

        self.init_ui()
        self.load_settings()
        self.apply_theme(self.dark_theme_enabled)

    def apply_theme(self, dark: bool):
        """根据dark值切换主题"""
        if dark:
            QApplication.setStyle("Fusion")
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53,53,53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(35,35,35))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53,53,53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42,130,218))
            dark_palette.setColor(QPalette.Highlight, QColor(42,130,218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.setPalette(dark_palette)

            font = QFont("Sans Serif", 12)
            QApplication.setFont(font)

            self.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #444;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-size: 14px;
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 5px;
                }
                QPushButton {
                    padding: 8px 16px;
                    border-radius: 4px;
                    background-color: #444;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QLineEdit {
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 6px;
                    background: #333;
                    selection-background-color: #666;
                    font-size: 13px;
                }
                QTextEdit {
                    border: 1px solid #555;
                    border-radius: 4px;
                    background: #222;
                    selection-background-color: #666;
                    font-size: 16px; 
                }
                QCheckBox, QLabel {
                    font-size: 13px;
                }
            """)
        else:
            # 浅色主题
            QApplication.setStyle("Fusion")
            light_palette = QPalette()
            light_palette.setColor(QPalette.Window, QColor(240,240,240))
            light_palette.setColor(QPalette.WindowText, Qt.black)
            light_palette.setColor(QPalette.Base, QColor(255,255,255))
            light_palette.setColor(QPalette.AlternateBase, QColor(240,240,240))
            light_palette.setColor(QPalette.ToolTipBase, Qt.white)
            light_palette.setColor(QPalette.ToolTipText, Qt.black)
            light_palette.setColor(QPalette.Text, Qt.black)
            light_palette.setColor(QPalette.Button, QColor(240,240,240))
            light_palette.setColor(QPalette.ButtonText, Qt.black)
            light_palette.setColor(QPalette.BrightText, Qt.red)
            light_palette.setColor(QPalette.Link, QColor(42,130,218))
            light_palette.setColor(QPalette.Highlight, QColor(42,130,218))
            light_palette.setColor(QPalette.HighlightedText, Qt.white)
            QApplication.setPalette(light_palette)

            font = QFont("Sans Serif", 12)
            QApplication.setFont(font)

            self.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #aaa;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-size: 14px;
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 5px;
                }
                QPushButton {
                    padding: 8px 16px;
                    border-radius: 4px;
                    background-color: #ddd;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #ccc;
                }
                QLineEdit {
                    border: 1px solid #aaa;
                    border-radius: 3px;
                    padding: 6px;
                    background: #fff;
                    selection-background-color: #3399ff;
                    font-size: 13px;
                }
                QTextEdit {
                    border: 1px solid #aaa;
                    border-radius: 4px;
                    background: #fff;
                    selection-background-color: #3399ff;
                    font-size: 16px; 
                }
                QCheckBox, QLabel {
                    font-size: 13px;
                    color: #000;
                }
            """)

        self.dark_theme_enabled = dark
        self.settings.setValue("dark_theme_enabled", self.dark_theme_enabled)

    def init_ui(self):
        self.setWindowTitle("SiliconFlow Speech Transcriber")
        self.resize(1000, 700)

        # 创建工具栏
        toolbar = QToolBar("操作工具栏")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24,24))
        self.addToolBar(toolbar)

        # 添加工具栏动作
        # 提交请求
        self.submit_action = QAction(self.style().standardIcon(QStyle.SP_DialogApplyButton), "提交转录请求", self)
        self.submit_action.triggered.connect(self.submit_request)
        toolbar.addAction(self.submit_action)

        # 取消请求
        self.cancel_action = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton), "取消请求", self)
        self.cancel_action.setEnabled(False)
        self.cancel_action.triggered.connect(self.cancel_request)
        toolbar.addAction(self.cancel_action)

        toolbar.addSeparator()

        # 清空结果
        self.clear_action = QAction(self.style().standardIcon(QStyle.SP_TrashIcon), "清空结果", self)
        self.clear_action.triggered.connect(self.clear_results)
        toolbar.addAction(self.clear_action)

        # 复制结果 (增加图标)
        self.copy_action = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "复制", self)
        self.copy_action.triggered.connect(self.copy_to_clipboard)
        toolbar.addAction(self.copy_action)

        # 导出结果
        self.export_action = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "导出结果", self)
        self.export_action.triggered.connect(self.export_to_file)
        toolbar.addAction(self.export_action)

        # 中心Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10,10,10,10)

        # 上部参数设置区
        input_group = QGroupBox("API 参数与文件选择")
        input_layout = QGridLayout(input_group)
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(10,10,10,10)

        # Token行
        token_label = QLabel("Bearer Token:")
        self.token_edit = QLineEdit()
        self.token_edit.setEchoMode(QLineEdit.Password)
        self.token_edit.setToolTip("在此输入你的Bearer Token，用于鉴权请求API。")

        self.show_token_cb = QCheckBox("显示")
        self.show_token_cb.toggled.connect(self.toggle_token_visibility)
        input_layout.addWidget(token_label, 0, 0)
        input_layout.addWidget(self.token_edit, 0, 1)
        input_layout.addWidget(self.show_token_cb, 0, 2)

        # 模型行
        model_label = QLabel("Model:")
        self.model_edit = QLineEdit()
        self.model_edit.setToolTip("在此输入或选择要使用的模型名称。")
        input_layout.addWidget(model_label, 1, 0)
        input_layout.addWidget(self.model_edit, 1, 1, 1, 2)

        # 文件行
        file_label = QLabel("音频文件:")
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setToolTip("在此显示选中的音频文件路径。")
        file_button_widget = QPushButton("选择文件")
        file_button_widget.setToolTip("点击选择要转录的音频文件。")
        file_button_widget.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        file_button_widget.clicked.connect(self.select_file)

        input_layout.addWidget(file_label, 2, 0)
        input_layout.addWidget(self.file_path_edit, 2, 1)
        input_layout.addWidget(file_button_widget, 2, 2)

        # 下方结果显示区
        result_group = QGroupBox("转录结果")
        result_group_layout = QVBoxLayout(result_group)
        result_group_layout.setSpacing(10)
        result_group_layout.setContentsMargins(10,10,10,10)
        self.result_text = QTextEdit()
        # 可编辑
        self.result_text.setReadOnly(False)
        self.result_text.setToolTip("此处显示转录结果，你可对结果进行编辑。")
        result_group_layout.addWidget(self.result_text)

        # 使用QSplitter分隔上下区域
        splitter = QSplitter(Qt.Vertical)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.addWidget(input_group)

        splitter.addWidget(top_widget)
        splitter.addWidget(result_group)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # 状态栏与进度条
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度显示
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # 菜单栏
        menubar = self.menuBar()
        setting_menu = menubar.addMenu("设置")
        pref_action = QAction("首选项", self)
        pref_action.triggered.connect(self.open_preferences)
        setting_menu.addAction(pref_action)

        theme_action = QAction("切换主题", self)
        theme_action.triggered.connect(self.toggle_theme)
        setting_menu.addAction(theme_action)

        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def open_preferences(self):
        current_token = self.token_edit.text().strip()
        current_model = self.model_edit.text().strip()

        dialog = PreferencesDialog(current_token, current_model, self)
        if dialog.exec_() == QDialog.Accepted:
            token, model = dialog.get_values()
            self.token_edit.setText(token)
            self.model_edit.setText(model)
            self.save_settings()

    def toggle_token_visibility(self, checked):
        if checked:
            self.token_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.token_edit.setEchoMode(QLineEdit.Password)

    def toggle_theme(self):
        """在深色和浅色主题之间切换"""
        self.apply_theme(not self.dark_theme_enabled)

    def show_about_dialog(self):
        QMessageBox.information(self, "关于",
                                "SiliconFlow Speech Transcriber\n\n"
                                "这是一个示例程序，用于调用SiliconFlow语音转文本API。\n"
                                "功能包括多线程请求、进度指示、取消操作、配置保存、\n"
                                "错误提示、复制导出结果、显示耗时以及首选项对话框。\n"
                                "UI支持深色与浅色主题切换，更加舒适美观。\n\n"
                                "作者：yeahhe（LINUXDO）")

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择音频文件", "",
            "音频文件 (*.wav *.mp3 *.m4a *.flac *.ogg);;所有文件 (*)",
            options=options
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.save_settings()

    def clear_results(self):
        self.result_text.clear()

    def copy_to_clipboard(self):
        text = self.result_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text, QClipboard.Clipboard)
            QMessageBox.information(self, "复制成功", "结果已复制到剪贴板。")
        else:
            QMessageBox.warning(self, "无内容", "当前没有可复制的内容。")

    def export_to_file(self):
        text = self.result_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "无内容", "当前没有可导出的内容。")
            return
        options = QFileDialog.Options()
        export_path, _ = QFileDialog.getSaveFileName(self, "导出转录结果", "", "文本文件 (*.txt);;所有文件 (*)", options=options)
        if export_path:
            try:
                with open(export_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "导出成功", f"结果已导出到 {export_path}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"无法导出文件：{str(e)}")

    def submit_request(self):
        token = self.token_edit.text().strip()
        model_name = self.model_edit.text().strip()
        file_path = self.file_path_edit.text().strip()

        if not token:
            QMessageBox.warning(self, "警告", "请先输入Bearer Token。")
            return
        if not model_name:
            QMessageBox.warning(self, "警告", "请先输入模型名称。")
            return
        if not file_path:
            QMessageBox.warning(self, "警告", "请先选择音频文件。")
            return

        # 显示进度
        self.progress_bar.setVisible(True)
        self.status_bar.showMessage("请求中...")
        self.submit_action.setEnabled(False)
        self.cancel_action.setEnabled(True)

        # 启动线程
        self.request_thread = RequestThread(token, model_name, file_path)
        self.request_thread.finished_signal.connect(self.handle_response)
        self.request_thread.start()

    def cancel_request(self):
        if self.request_thread and self.request_thread.isRunning():
            self.request_thread.cancel()
            self.result_text.setText("请求已取消。请稍候...")
        self.cancel_action.setEnabled(False)

    def handle_response(self, result, elapsed):
        self.progress_bar.setVisible(False)
        self.submit_action.setEnabled(True)
        self.cancel_action.setEnabled(False)

        if result is None:
            # 请求被取消
            self.status_bar.showMessage("就绪")
            self.result_text.append("\n请求已被用户取消。")
            return

        self.status_bar.showMessage(f"就绪 | 耗时: {elapsed:.2f}s")

        if isinstance(result, Exception):
            self.result_text.setText(f"请求异常: {str(result)}")
            return

        response = result
        if response.status_code == 200:
            resp_json = response.json()
            transcription = resp_json.get("text", "")
            if transcription:
                self.result_text.setText(transcription)
            else:
                self.result_text.setText("未获取到转录文本。")
        else:
            self.result_text.setText(f"请求失败，状态码: {response.status_code}\n响应内容: {response.text}")

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self):
        self.settings.setValue("token", self.token_edit.text())
        self.settings.setValue("model", self.model_edit.text())
        self.settings.setValue("file_path", self.file_path_edit.text())

    def load_settings(self):
        saved_token = self.settings.value("token", "")
        saved_model = self.settings.value("model", "FunAudioLLM/SenseVoiceSmall")
        saved_file_path = self.settings.value("file_path", "")

        self.token_edit.setText(saved_token)
        self.model_edit.setText(saved_model)
        self.file_path_edit.setText(saved_file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranscriptionApp()
    window.show()
    sys.exit(app.exec_())