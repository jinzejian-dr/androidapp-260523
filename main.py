# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 Android App
版本: 1.1.1
日期: 2026-05-24
功能: RTSP视频播放、设备发现、设备管理
使用 Kivy 内置 Video 组件
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

# 使用 Kivy 内置视频播放器
try:
    from kivy.uix.video import Video
    KIVY_VIDEO_AVAILABLE = True
except ImportError:
    KIVY_VIDEO_AVAILABLE = False


class VideoWidget(BoxLayout):
    """视频显示组件 - 使用 Kivy Video"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.video = None
        self.is_playing = False
        
    def start_playback(self, url):
        """开始播放视频"""
        if not KIVY_VIDEO_AVAILABLE:
            return False, "Kivy Video 不可用"
            
        try:
            # 停止之前的播放
            self.stop_playback()
            
            # 创建视频播放器
            self.video = Video(
                source=url,
                state='play',
                options={'allow_stretch': True}
            )
            self.add_widget(self.video)
            self.is_playing = True
            return True, "播放开始"
        except Exception as e:
            return False, f"播放失败: {str(e)}"
    
    def stop_playback(self):
        """停止播放"""
        self.is_playing = False
        if self.video:
            self.video.state = 'stop'
            self.remove_widget(self.video)
            self.video = None


class MainLayout(BoxLayout):
    """主界面布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
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
            text='[b]术野摄像头接收端 v1.1[/b]',
            markup=True,
            size_hint_y=None,
            height=40,
            font_size='20sp'
        )
        self.add_widget(title)
        
        # 视频显示区域
        self.video_widget = VideoWidget(size_hint_y=0.5)
        self.add_widget(self.video_widget)
        
        # RTSP地址输入
        url_box = BoxLayout(size_hint_y=None, height=40, spacing=5)
        url_box.add_widget(Label(text='RTSP地址:', size_hint_x=0.2))
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/cam',
            multiline=False,
            size_hint_x=0.8
        )
        url_box.add_widget(self.url_input)
        self.add_widget(url_box)
        
        # 按钮区域
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.play_btn = Button(
            text='▶ 播放',
            font_size='16sp',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.play_btn.bind(on_press=self.on_play)
        btn_box.add_widget(self.play_btn)
        
        self.stop_btn = Button(
            text='⏹ 停止',
            font_size='16sp',
            background_color=(0.7, 0.2, 0.2, 1)
        )
        self.stop_btn.bind(on_press=self.on_stop)
        btn_box.add_widget(self.stop_btn)
        
        self.discover_btn = Button(
            text='🔍 发现设备',
            font_size='16sp',
            background_color=(0.2, 0.5, 0.7, 1)
        )
        self.discover_btn.bind(on_press=self.on_discover)
        btn_box.add_widget(self.discover_btn)
        
        self.add_widget(btn_box)
        
        # 设备列表区域
        self.add_widget(Label(
            text='[b]发现的设备:[/b]',
            markup=True,
            size_hint_y=None,
            height=25,
            font_size='14sp'
        ))
        
        # 设备列表滚动区域
        scroll = ScrollView(size_hint_y=0.2)
        self.devices_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        scroll.add_widget(self.devices_layout)
        self.add_widget(scroll)
        
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
        if not url:
            self.status_label.text = '状态: 请输入RTSP地址'
            return
            
        success, msg = self.video_widget.start_playback(url)
        if success:
            self.status_label.text = f'状态: 正在播放 {url}'
            self.log_label.text = '日志: 播放中...'
            self.play_btn.background_color = (0.5, 0.5, 0.5, 1)
        else:
            self.status_label.text = f'状态: {msg}'
            self.log_label.text = f'日志: {msg}'
        
    def on_stop(self, instance):
        """停止按钮"""
        self.video_widget.stop_playback()
        self.status_label.text = '状态: 已停止'
        self.log_label.text = '日志: 播放停止'
        self.play_btn.background_color = (0.2, 0.7, 0.3, 1)
        
    def on_discover(self, instance):
        """手动触发设备发现"""
        self.status_label.text = '状态: 正在发现设备...'
        threading.Thread(target=self.discover_devices, daemon=True).start()
        
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
            
            # 发送发现请求
            request = json.dumps({'action': 'discover'})
            sock.sendto(request.encode('utf-8'), ('255.255.255.255', 8888))
            
            # 等待响应
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
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'状态: 发现失败 {str(e)}'), 0)
            
    def update_discovery_status(self, count):
        """更新发现状态"""
        self.status_label.text = f'状态: 发现 {count} 个设备'
        
    def add_device(self, device_info):
        """添加设备到列表"""
        Clock.schedule_once(lambda dt: self._add_device_ui(device_info), 0)
        
    def _add_device_ui(self, device_info):
        """在UI中添加设备"""
        device_id = device_info.get('id', 'unknown')
        device_ip = device_info.get('ip', 'unknown')
        device_name = device_info.get('name', f'设备 {device_id[:6]}')
        
        # 检查是否已存在
        for child in self.devices_layout.children:
            if hasattr(child, 'device_id') and child.device_id == device_id:
                return
                
        # 创建设备按钮
        btn = Button(
            text=f'{device_name}\n{device_ip}',
            size_hint_y=None,
            height=50,
            font_size='12sp'
        )
        btn.device_id = device_id
        btn.device_info = device_info
        btn.bind(on_press=lambda x: self.select_device(device_info))
        
        self.devices_layout.add_widget(btn)
        self.devices.append(device_info)
        self.log_label.text = f'日志: 发现设备 {device_name}'
        
    def select_device(self, device_info):
        """选择设备"""
        self.current_device = device_info
        device_ip = device_info.get('ip', '192.168.4.1')
        rtsp_url = f'rtsp://{device_ip}:8554/cam'
        self.url_input.text = rtsp_url
        self.status_label.text = f'状态: 已选择 {device_info.get("name", "设备")}'
        self.log_label.text = f'日志: 选择设备 {device_ip}'


class SimpleSurgeryCamApp(App):
    """Kivy应用类"""
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()


if __name__ == '__main__':
    SimpleSurgeryCamApp().run()
