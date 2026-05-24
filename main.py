# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 Android App
版本: 1.1.3
日期: 2026-05-24
功能: 设备发现、RTSP地址管理
说明: 暂时移除视频播放功能，使用外部播放器
"""

import threading
import socket
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform


class MainLayout(BoxLayout):
    """主界面布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 5
        
        # 设备列表
        self.devices = []
        self.current_device = None
        
        # 创建UI
        self.create_ui()
        
        # 启动设备发现
        self.start_discovery()
        
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title = Label(
            text='SurgeryCam v1.1',
            size_hint_y=None,
            height=30,
            font_size='16sp'
        )
        self.add_widget(title)
        
        # RTSP地址输入
        url_box = BoxLayout(size_hint_y=None, height=35, spacing=3)
        url_box.add_widget(Label(text='RTSP:', size_hint_x=0.2, font_size='12sp'))
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/cam',
            multiline=False,
            size_hint_x=0.8,
            font_size='11sp'
        )
        url_box.add_widget(self.url_input)
        self.add_widget(url_box)
        
        # 按钮区域
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=5)
        
        self.copy_btn = Button(
            text='COPY',
            font_size='12sp',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.copy_btn.bind(on_press=self.copy_url)
        btn_box.add_widget(self.copy_btn)
        
        self.scan_btn = Button(
            text='SCAN',
            font_size='12sp',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.scan_btn.bind(on_press=self.on_scan)
        btn_box.add_widget(self.scan_btn)
        
        self.play_btn = Button(
            text='PLAY',
            font_size='12sp',
            background_color=(0.8, 0.4, 0.2, 1)
        )
        self.play_btn.bind(on_press=self.open_player)
        btn_box.add_widget(self.play_btn)
        
        self.add_widget(btn_box)
        
        # 设备列表区域
        self.add_widget(Label(
            text='Devices:',
            size_hint_y=None,
            height=20,
            font_size='12sp'
        ))
        
        # 设备列表滚动区域
        scroll = ScrollView(size_hint_y=0.6)
        self.devices_layout = GridLayout(cols=1, spacing=3, size_hint_y=None)
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        scroll.add_widget(self.devices_layout)
        self.add_widget(scroll)
        
        # 状态显示
        self.status_label = Label(
            text='Ready',
            size_hint_y=None,
            height=25,
            font_size='11sp'
        )
        self.add_widget(self.status_label)
        
        # 说明文字
        self.add_widget(Label(
            text='Use external player (VLC/MX)',
            size_hint_y=None,
            height=20,
            font_size='10sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        
    def copy_url(self, instance):
        """复制URL到剪贴板"""
        url = self.url_input.text.strip()
        if platform == 'android':
            try:
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                ClipboardManager = autoclass('android.content.ClipboardManager')
                ClipData = autoclass('android.content.ClipData')
                
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                clipboard = activity.getSystemService(Context.CLIPBOARD_SERVICE)
                clip = ClipData.newPlainText("RTSP URL", url)
                clipboard.setPrimaryClip(clip)
                self.status_label.text = 'URL copied!'
            except:
                self.status_label.text = 'Copy failed'
        else:
            self.status_label.text = 'URL: ' + url[:30] + '...'
        
    def on_scan(self, instance):
        """扫描设备"""
        self.status_label.text = 'Scanning...'
        self.devices_layout.clear_widgets()
        self.devices = []
        threading.Thread(target=self.discover_devices, daemon=True).start()
        
    def open_player(self, instance):
        """打开外部播放器"""
        url = self.url_input.text.strip()
        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(Uri.parse(url), "video/*")
                PythonActivity.mActivity.startActivity(intent)
                self.status_label.text = 'Opening player...'
            except Exception as e:
                self.status_label.text = f'Error: {str(e)[:30]}'
        else:
            self.status_label.text = 'URL: ' + url[:30]
        
    def start_discovery(self):
        """启动设备发现服务"""
        self.discovery_thread = threading.Thread(target=self.discovery_listener, daemon=True)
        self.discovery_thread.start()
        
    def discovery_listener(self):
        """监听设备广播"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', 8888))
            sock.settimeout(1)
            
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    device_info = json.loads(data.decode('utf-8'))
                    device_info['ip'] = addr[0]
                    self.add_device(device_info)
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Discovery error: {e}")
        except Exception as e:
            print(f"Discovery listener error: {e}")
            
    def discover_devices(self):
        """主动发现设备"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(3)
            
            request = json.dumps({'action': 'discover'})
            sock.sendto(request.encode('utf-8'), ('255.255.255.255', 8888))
            
            found = []
            start_time = __import__('time').time()
            while __import__('time').time() - start_time < 3:
                try:
                    data, addr = sock.recvfrom(1024)
                    device_info = json.loads(data.decode('utf-8'))
                    device_info['ip'] = addr[0]
                    if device_info not in found:
                        found.append(device_info)
                        self.add_device(device_info)
                except socket.timeout:
                    break
                except Exception as e:
                    continue
                    
            Clock.schedule_once(lambda dt: self.update_discovery_status(len(found)), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Scan failed'), 0)
            
    def update_discovery_status(self, count):
        """更新发现状态"""
        self.status_label.text = f'Found {count} devices'
        
    def add_device(self, device_info):
        """添加设备到列表"""
        Clock.schedule_once(lambda dt: self._add_device_ui(device_info), 0)
        
    def _add_device_ui(self, device_info):
        """在UI中添加设备"""
        device_id = device_info.get('id', 'unknown')
        device_ip = device_info.get('ip', 'unknown')
        device_name = device_info.get('name', f'Device {device_id[:6]}')
        
        for child in self.devices_layout.children:
            if hasattr(child, 'device_id') and child.device_id == device_id:
                return
                
        btn = Button(
            text=f'{device_name}\n{device_ip}',
            size_hint_y=None,
            height=45,
            font_size='10sp'
        )
        btn.device_id = device_id
        btn.device_info = device_info
        btn.bind(on_press=lambda x: self.select_device(device_info))
        
        self.devices_layout.add_widget(btn)
        self.devices.append(device_info)
        
    def select_device(self, device_info):
        """选择设备"""
        self.current_device = device_info
        device_ip = device_info.get('ip', '192.168.4.1')
        rtsp_url = f'rtsp://{device_ip}:8554/cam'
        self.url_input.text = rtsp_url
        self.status_label.text = f'Selected: {device_info.get("name", "Device")}'


class SimpleSurgeryCamApp(App):
    """Kivy应用类"""
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()


if __name__ == '__main__':
    SimpleSurgeryCamApp().run()
