# -*- coding: utf-8 -*-
"""
术野摄像头接收端 - 简化版 Android App
版本: 1.2.0
日期: 2026-05-31
功能: 设备发现、RTSP地址管理、视频播放
说明: 使用 ffpyplayer 进行视频播放
"""

import threading
import socket
import json
import os
import sys
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

# 日志记录
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 尝试导入 ffpyplayer
try:
    from ffpyplayer.player import MediaPlayer
    FFPYPLAYER_AVAILABLE = True
    logger.info("ffpyplayer imported successfully")
except ImportError as e:
    FFPYPLAYER_AVAILABLE = False
    logger.error(f"ffpyplayer import failed: {e}")


class VideoWidget(BoxLayout):
    """视频显示组件"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.player = None
        self.is_playing = False
        self.texture = None
        
        # 视频显示区域
        from kivy.uix.image import Image
        self.video_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.video_image)
        
        # 状态标签
        self.status_label = Label(
            text='Video Ready',
            size_hint_y=None,
            height=20,
            font_size='10sp'
        )
        self.add_widget(self.status_label)
        
    def start_playback(self, url):
        """开始播放视频"""
        if not FFPYPLAYER_AVAILABLE:
            self.status_label.text = 'Error: ffpyplayer not available'
            logger.error("ffpyplayer not available, cannot start playback")
            return False
            
        try:
            # 停止之前的播放
            self.stop_playback()
            
            logger.info(f"Starting playback: {url}")
            self.status_label.text = 'Connecting...'
            
            # 配置 ffpyplayer - 低延迟模式
            ffopts = {
                'rtsp_transport': 'tcp',
                'fflags': 'nobuffer',
                'flags': 'low_delay',
                'probesize': '32',
                'analyzeduration': '0',
                'sync': 'video',
            }
            
            self.player = MediaPlayer(url, ffopts=ffopts)
            self.is_playing = True
            
            # 开始更新视频帧
            Clock.schedule_interval(self.update_frame, 1.0/30.0)  # 30fps
            
            self.status_label.text = 'Playing'
            logger.info("Playback started successfully")
            return True
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)[:30]}'
            logger.error(f"Failed to start playback: {e}")
            return False
    
    def stop_playback(self):
        """停止播放"""
        logger.info("Stopping playback")
        self.is_playing = False
        Clock.unschedule(self.update_frame)
        
        if self.player:
            try:
                self.player.close_player()
            except Exception as e:
                logger.error(f"Error closing player: {e}")
            self.player = None
            
        self.status_label.text = 'Stopped'
        self.video_image.texture = None
        
    def update_frame(self, dt):
        """更新视频帧"""
        if not self.is_playing or not self.player:
            return False
            
        try:
            frame, val = self.player.get_frame()
            if frame is not None:
                # 获取帧数据
                img, t = frame
                if img is not None:
                    # 更新纹理
                    self.video_image.texture = img
                    self.video_image.canvas.ask_update()
        except Exception as e:
            logger.error(f"Frame update error: {e}")
            
        return self.is_playing


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
        
        logger.info("Initializing MainLayout")
        
        # 创建UI
        self.create_ui()
        
        # 启动设备发现
        self.start_discovery()
        
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title = Label(
            text=f'SurgeryCam v1.1.4 (ffpyplayer: {"OK" if FFPYPLAYER_AVAILABLE else "N/A"})',
            size_hint_y=None,
            height=30,
            font_size='14sp'
        )
        self.add_widget(title)
        
        # 视频播放区域 (如果 ffpyplayer 可用)
        if FFPYPLAYER_AVAILABLE:
            self.video_widget = VideoWidget(size_hint_y=0.4)
            self.add_widget(self.video_widget)
        else:
            # 显示警告
            warning = Label(
                text='WARNING: Video playback not available\nUsing external player',
                size_hint_y=0.4,
                color=(1, 0.5, 0, 1),
                font_size='12sp'
            )
            self.add_widget(warning)
            self.video_widget = None
        
        # RTSP地址输入
        url_box = BoxLayout(size_hint_y=None, height=35, spacing=3)
        url_box.add_widget(Label(text='RTSP:', size_hint_x=0.15, font_size='11sp'))
        self.url_input = TextInput(
            text='rtsp://192.168.4.1:8554/cam',
            multiline=False,
            size_hint_x=0.85,
            font_size='11sp'
        )
        url_box.add_widget(self.url_input)
        self.add_widget(url_box)
        
        # 按钮区域
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=5)
        
        self.copy_btn = Button(
            text='COPY',
            font_size='11sp',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.copy_btn.bind(on_press=self.copy_url)
        btn_box.add_widget(self.copy_btn)
        
        self.scan_btn = Button(
            text='SCAN',
            font_size='11sp',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.scan_btn.bind(on_press=self.on_scan)
        btn_box.add_widget(self.scan_btn)
        
        # 播放按钮 - 根据 ffpyplayer 可用性显示不同功能
        if FFPYPLAYER_AVAILABLE:
            self.play_btn = Button(
                text='PLAY',
                font_size='11sp',
                background_color=(0.8, 0.4, 0.2, 1)
            )
            self.play_btn.bind(on_press=self.toggle_playback)
        else:
            self.play_btn = Button(
                text='OPEN',
                font_size='11sp',
                background_color=(0.8, 0.6, 0.2, 1)
            )
            self.play_btn.bind(on_press=self.open_external_player)
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
        scroll = ScrollView(size_hint_y=0.25)
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
        
        logger.info("UI created successfully")
        
    def toggle_playback(self, instance):
        """切换播放/停止"""
        if not self.video_widget:
            self.open_external_player(instance)
            return
            
        if self.video_widget.is_playing:
            self.video_widget.stop_playback()
            self.play_btn.text = 'PLAY'
            self.play_btn.background_color = (0.8, 0.4, 0.2, 1)
        else:
            url = self.url_input.text.strip()
            if self.video_widget.start_playback(url):
                self.play_btn.text = 'STOP'
                self.play_btn.background_color = (0.6, 0.2, 0.2, 1)
        
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
                logger.info("URL copied to clipboard")
            except Exception as e:
                logger.error(f"Copy failed: {e}")
                self.status_label.text = 'Copy failed'
        else:
            self.status_label.text = 'URL: ' + url[:30] + '...'
        
    def on_scan(self, instance):
        """扫描设备"""
        logger.info("Starting device scan")
        self.status_label.text = 'Scanning...'
        self.devices_layout.clear_widgets()
        self.devices = []
        threading.Thread(target=self.discover_devices, daemon=True).start()
        
    def open_external_player(self, instance):
        """打开外部播放器"""
        url = self.url_input.text.strip()
        logger.info(f"Opening external player: {url}")
        
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
                logger.error(f"Open player failed: {e}")
                self.status_label.text = f'Error: {str(e)[:30]}'
        else:
            self.status_label.text = 'URL: ' + url[:30]
        
    def start_discovery(self):
        """启动设备发现服务"""
        logger.info("Starting discovery service")
        self.discovery_thread = threading.Thread(target=self.discovery_listener, daemon=True)
        self.discovery_thread.start()
        
    def discovery_listener(self):
        """监听设备广播"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', 8888))
            sock.settimeout(1)
            
            logger.info("Discovery listener started on port 8888")
            
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    device_info = json.loads(data.decode('utf-8'))
                    device_info['ip'] = addr[0]
                    logger.info(f"Discovered device: {device_info}")
                    self.add_device(device_info)
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Discovery error: {e}")
        except Exception as e:
            logger.error(f"Discovery listener error: {e}")
            
    def discover_devices(self):
        """主动发现设备"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(3)
            
            request = json.dumps({'action': 'discover'})
            sock.sendto(request.encode('utf-8'), ('255.255.255.255', 8888))
            
            logger.info("Discovery broadcast sent")
            
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
                    
            logger.info(f"Discovery complete, found {len(found)} devices")
            Clock.schedule_once(lambda dt: self.update_discovery_status(len(found)), 0)
        except Exception as e:
            logger.error(f"Discovery failed: {e}")
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
        logger.info(f"Added device to UI: {device_name}")
        
    def select_device(self, device_info):
        """选择设备"""
        self.current_device = device_info
        device_ip = device_info.get('ip', '192.168.4.1')
        rtsp_url = f'rtsp://{device_ip}:8554/cam'
        self.url_input.text = rtsp_url
        self.status_label.text = f'Selected: {device_info.get("name", "Device")}'
        logger.info(f"Device selected: {device_info.get('name', 'Device')}")


class SimpleSurgeryCamApp(App):
    """Kivy应用类"""
    def build(self):
        logger.info("Building app...")
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()


if __name__ == '__main__':
    logger.info("Starting SurgeryCam App v1.2.0")
    SimpleSurgeryCamApp().run()
