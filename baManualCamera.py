# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING, cast

import _babase as _ba
import bascenev1 as bs
import bauiv1 as bui

from bauiv1lib.popup import PopupWindow
from bauiv1lib.confirm import ConfirmWindow

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable

calls: dict = {}
command = '.cam'

class FreeCameraWindow(PopupWindow):
    def __init__(self, transition= 'in_scale'):
        columns = 2
        self._width = width = 1200
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.buttons = []

        app = bs.app.ui_v1
        uiscale = app.uiscale

        self._root_widget = bui.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5, background=False,
                           stack_offset=(0,-30) if uiscale is bui.UIScale.SMALL else  (0,0))
        
        self._back_button = b = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(200,self._height-90),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=bui.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=bui.Call(self._back))
        bui.buttonwidget(edit=self._back_button, button_type='backSmall',size=(60, 60),label=bui.charstr(bui.SpecialChar.BACK))
        bui.containerwidget(edit=self._root_widget,cancel_button=b)
        
        _x = 0.0
        
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-170),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=bui.Call(self._move, 'u')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-300),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=bui.Call(self._move, 'd')))
        
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(210.5+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.LEFT_ARROW),
                   button_type='square', on_activate_call=bui.Call(self._move, 'l')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(352.55+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.RIGHT_ARROW),
                   button_type='square', on_activate_call=bui.Call(self._move, 'r')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*4.75+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=bui.Call(self._move, 'z+')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*4.75+_x, self._height-235*1.3),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'z-')))

        _x += 650
        
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-170),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'ar')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-300),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'ab')))
        
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(210.5+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.LEFT_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'iz')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(352.55+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.RIGHT_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'de')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*7.5+(_x-_x), self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'w+')))
                   
        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*7.5+(_x-_x), self._height-235*1.3),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=bui.charstr(bui.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=bs.Call(self._move, 'w-')))

        self.buttons.append(
            bui.buttonwidget(parent=self._root_widget,autoselect=True,
                   position=(352.55*2.9, self._height-235*0.45),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label='*', enable_sound=False,
                   button_type='square', on_activate_call=bs.Call(self._move, '*')))

    def _move(self, val: str = 'none'):
        pos = [0.0, 0.0, 0.0]
        max = 1.0
        if val == 'u':
            pos[2] = -max
        elif val == 'd':
            pos[2] = max
        elif val == 'l':
            pos[0] = -max
        elif val == 'r':
            pos[0] = max
        elif val == 'z-':
            pos[1] = -max
        elif val == 'z+':
            pos[1] = max

        pos2 = [0.0, 0.0, 0.0]
        if val == 'ar':
            pos2[2] = -max
        elif val == 'ab':
            pos2[2] = max
        elif val == 'iz':
            pos2[0] = -max
        elif val == 'de':
            pos2[0] = max
        elif val == 'w-':
            pos2[1] = -max
        elif val == 'w+':
            pos2[1] = max

        if val == '*':
            _ba.set_camera_manual(False)
        else:
            _ba.set_camera_manual(True)
            p = list(_ba.get_camera_position())
            _ba.set_camera_position(
                p[0]+pos[0], p[1]+pos[1], p[2]+pos[2])
            
            p = list(_ba.get_camera_target())
            _ba.set_camera_target(
                p[0]+pos2[0], p[1]+pos2[1], p[2]+pos2[2])

def _back(self):
    bui.containerwidget(edit=self._root_widget,transition='out_scale')
    #MapMakerWindow()

def party_icon(value: bool):
    calls['btn_party'](True)

def new_message(msg, **kwargs):
    if msg.lower() == command:
        if bs.app.classic.party_window is not None and bs.app.classic.party_window() is not None:
            bs.app.classic.party_window().close()
        
        camera_window = FreeCameraWindow
        camera_window._back = _back
        
        with bs.ContextRef.empty():
            camera_window()
        #ut.open_bs17_window()
    else:
        calls['chat'](msg, **kwargs)
        
def add_plugin():
    try: from baBearModz import BearPlugin
    except: return

    BearPlugin(icon='achievementDualWielding',
               creator='@PatrónModz',
               button_color=(0.25, 1.05, 0.05),
               plugin=ManualCamera,
               window=FreeCameraWindow)
        
# ba_meta export plugin
class ManualCamera(bs.Plugin):
    def __init__(self):
        add_plugin()
        
        calls['chat'] = bs.chatmessage
        calls['btn_party'] = bui.set_party_icon_always_visible
        
        bs.chatmessage = new_message
        bui.set_party_icon_always_visible = party_icon
        bui.set_party_icon_always_visible(True)
        