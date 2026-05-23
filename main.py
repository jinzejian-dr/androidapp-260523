# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 Android App
版本: 1.0.0
日期: 2026-05-23
功能: 基础界面测试
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class MainLayout(BoxLayout):
    """主界面布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
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
        self.play_btn.bind(on_press=self.on_play)
        btn_box.add_widget(self.play_btn)
        
        self.stop_btn = Button(
            text='⏹ 停止',
            font_size='16sp'
        )
        self.stop_btn.bind(on_press=self.on_stop)
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
        
        # 日志区域
        self.log_label = Label(
            text='日志: 等待连接...',
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.add_widget(self.log_label)
        
    def on_play(self, instance):
        """播放按钮"""
        url = self.url_input.text.strip()
        self.status_label.text = f'状态: 准备播放 {url}'
        self.log_label.text = '日志: 点击了播放'
        
    def on_stop(self, instance):
        """停止按钮"""
        self.status_label.text = '状态: 已停止'
        self.log_label.text = '日志: 点击了停止'


class SimpleSurgeryCamApp(App):
    """Kivy应用类"""
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()


if __name__ == '__main__':
    SimpleSurgeryCamApp().run()
