# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 Android App
版本: 1.0.0
日期: 2026-05-23
功能: 仅支持 RTSP 视频播放，输入地址即可播放

打包命令:
    buildozer android debug

依赖:
    pip install kivy ffpyplayer
"""

import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.window import Window

import cv2
import threading
import time


class VideoWidget(Image):
    """视频显示组件"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texture = None
        self.allow_stretch = True
        self.keep_ratio = True
        
    def update_frame(self, frame):
        """更新视频帧"""
        # 转换 BGR 到 RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 转换为 Kivy Texture
        buf = frame_rgb.tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='rgb'
        )
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        
        self.texture = texture


class MainLayout(BoxLayout):
    """主界面布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # 状态变量
        self.is_playing = False
        self.cap = None
        self.video_thread = None
        
        # 创建UI
        self.create_ui()
        
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title = Label(
            text='[b]术野摄像头接收端[/b]',
            markup=True,
            size_hint_y=None,
            height=40,
            font_size='20sp'
        )
        self.add_widget(title)
        
        # RTSP地址输入
        url_box = BoxLayout(size_hint_y=None, height=40, spacing=5)
        url_box.add_widget(Label(text='RTSP地址:', size_hint_x=0.2))
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/c',
            multiline=False,
            size_hint_x=0.8
        )
        url_box.add_widget(self.url_input)
        self.add_widget(url_box)
        
        # 按钮区域
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.play_btn = Button(
            text='▶ 播放',
            font_size='16sp'
        )
        self.play_btn.bind(on_press=self.start_playback)
        btn_box.add_widget(self.play_btn)
        
        self.stop_btn = Button(
            text='⏹ 停止',
            font_size='16sp',
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_playback)
        btn_box.add_widget(self.stop_btn)
        
        self.add_widget(btn_box)
        
        # 状态显示
        self.status_label = Label(
            text='状态: 就绪',
            size_hint_y=None,
            height=30,
            font_size='14sp'
        )
        self.add_widget(self.status_label)
        
        # 视频显示区域
        self.video_widget = VideoWidget()
        self.add_widget(self.video_widget)
        
        # 日志区域
        self.log_label = Label(
            text='日志: 等待连接...',
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.add_widget(self.log_label)
        
    def start_playback(self, instance):
        """开始播放"""
        url = self.url_input.text.strip()
        if not url:
            self.update_status('请输入RTSP地址', error=True)
            return
            
        self.update_status('正在连接...')
        self.play_btn.disabled = True
        self.stop_btn.disabled = False
        self.is_playing = True
        
        # 启动视频线程
        self.video_thread = threading.Thread(
            target=self.video_loop,
            args=(url,),
            daemon=True
        )
        self.video_thread.start()
        
    def video_loop(self, url):
        """视频接收循环"""
        try:
            self.cap = cv2.VideoCapture(url)
            
            if not self.cap.isOpened():
                Clock.schedule_once(lambda dt: self.on_error('无法打开视频流'), 0)
                return
            
            # 获取视频信息
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            Clock.schedule_once(
                lambda dt: self.update_status(f'已连接: {width}x{height}@{fps:.1f}fps'), 
                0
            )
            
            while self.is_playing and self.cap.isOpened():
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                # 更新视频帧（在主线程）
                Clock.schedule_once(lambda dt, f=frame: self.update_video_frame(f), 0)
                
                # 控制帧率，避免CPU占用过高
                time.sleep(0.001)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.on_error(f'播放错误: {str(e)}'), 0)
        finally:
            if self.cap:
                self.cap.release()
                self.cap = None
                
    def update_video_frame(self, frame):
        """更新视频帧"""
        try:
            self.video_widget.update_frame(frame)
        except Exception:
            pass
            
    def stop_playback(self, instance):
        """停止播放"""
        self.is_playing = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=2)
            
        self.play_btn.disabled = False
        self.stop_btn.disabled = True
        self.video_widget.texture = None
        self.update_status('已停止')
        
    def update_status(self, message, error=False):
        """更新状态"""
        self.status_label.text = f'状态: {message}'
        self.log_label.text = f'日志: {message}'
        if error:
            self.status_label.color = (1, 0, 0, 1)
        else:
            self.status_label.color = (1, 1, 1, 1)
            
    def on_error(self, message):
        """错误处理"""
        self.update_status(message, error=True)
        self.play_btn.disabled = False
        self.stop_btn.disabled = True
        self.is_playing = False


class SimpleSurgeryCamApp(App):
    """Kivy应用类"""
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()
        
    def on_stop(self):
        """应用停止时清理"""
        if hasattr(self.root, 'is_playing'):
            self.root.is_playing = False
        if hasattr(self.root, 'cap') and self.root.cap:
            self.root.cap.release()


if __name__ == '__main__':
    SimpleSurgeryCamApp().run()
