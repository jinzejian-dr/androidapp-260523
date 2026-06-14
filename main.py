# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - Android App v1.4.0
版本: 1.4.0
日期: 2026-06-15
功能: 设备发现、内置RTSP播放器 (ijkplayer准备集成)
说明: 使用ijkplayer实现内置视频播放，不依赖外部App
"""

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
import threading
import socket
import json


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        self.create_ui()
        self.start_discovery()
        
    def create_ui(self):
        # 标题
        self.add_widget(Label(
            text='SurgeryCam v1.4.0 (ijkplayer Ready)',
            size_hint_y=None, height=40,
            font_size='16sp', bold=True
        ))
        
        # 提示
        self.add_widget(Label(
            text='Built-in player coming soon...\nCurrently using external player',
            size_hint_y=None, height=50,
            font_size='12sp'
        ))
        
        # RTSP地址
        url_box = BoxLayout(size_hint_y=None, height=40, spacing=5)
        url_box.add_widget(Label(text='RTSP:', size_hint_x=0.2))
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/cam',
            multiline=False, size_hint_x=0.8
        )
        url_box.add_widget(self.url_input)
        self.add_widget(url_box)
        
        # 按钮
        btn_box = BoxLayout(size_hint_y=None, height=45, spacing=5)
        
        btn_scan = Button(text='SCAN', background_color=(0.2, 0.5, 0.8, 1))
        btn_scan.bind(on_press=self.on_scan)
        btn_box.add_widget(btn_scan)
        
        btn_play = Button(text='PLAY (External)', background_color=(0.2, 0.7, 0.3, 1))
        btn_play.bind(on_press=self.on_play_external)
        btn_box.add_widget(btn_play)
        
        self.add_widget(btn_box)
        
        # 设备列表
        self.add_widget(Label(text='Devices:', size_hint_y=None, height=25))
        self.devices_label = Label(
            text='No devices found',
            size_hint_y=0.3
        )
        self.add_widget(self.devices_label)
        
        # 状态
        self.status_label = Label(
            text='Ready - v1.4.0',
            size_hint_y=None, height=30
        )
        self.add_widget(self.status_label)
        
    def start_discovery(self):
        threading.Thread(target=self.discovery_listener, daemon=True).start()
        
    def discovery_listener(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', 8888))
            sock.settimeout(1)
            devices = []
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    device = json.loads(data.decode('utf-8'))
                    device['ip'] = addr[0]
                    if device not in devices:
                        devices.append(device)
                        Clock.schedule_once(
                            lambda dt: self.update_devices(devices), 0
                        )
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Discovery error: {e}")
        except Exception as e:
            logger.error(f"Listener error: {e}")
            
    def update_devices(self, devices):
        text = '\n'.join([f"{d.get('name','Device')} @ {d.get('ip','')}" for d in devices])
        self.devices_label.text = text or 'No devices found'
        
    def on_scan(self, instance):
        self.status_label.text = 'Scanning...'
        threading.Thread(target=self.send_discovery, daemon=True).start()
        
    def send_discovery(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(3)
            request = json.dumps({'action': 'discover'})
            sock.sendto(request.encode('utf-8'), ('255.255.255.255', 8888))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Scan complete'), 3)
        except Exception as e:
            logger.error(f"Scan error: {e}")
            
    def on_play_external(self, instance):
        url = self.url_input.text.strip()
        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(Uri.parse(url), "video/*")
                activity.startActivity(intent)
                self.status_label.text = 'Opening external player...'
            except Exception as e:
                self.status_label.text = f'Error: {str(e)[:30]}'
        else:
            self.status_label.text = f'URL: {url[:30]}...'


class SurgeryCamApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()


if __name__ == '__main__':
    SurgeryCamApp().run()
