# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 v1.3.1
最小化版本，确保能成功构建
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class SimpleApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        layout.add_widget(Label(
            text='SurgeryCam v1.3.1',
            size_hint_y=None,
            height=40,
            font_size='18sp'
        ))
        
        # RTSP 输入
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/cam',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.url_input)
        
        # 按钮
        btn = Button(
            text='Copy RTSP URL',
            size_hint_y=None,
            height=50
        )
        btn.bind(on_press=self.copy_url)
        layout.add_widget(btn)
        
        # 状态
        self.status = Label(text='Ready')
        layout.add_widget(self.status)
        
        return layout
    
    def copy_url(self, instance):
        url = self.url_input.text
        self.status.text = f'URL: {url}'


if __name__ == '__main__':
    SimpleApp().run()
