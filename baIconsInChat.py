# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING, cast

import bascenev1 as bs
import bauiv1 as bui

import base64, os, math
from bauiv1lib.keyboard.englishkeyboard import EnglishKeyboard
from bauiv1lib.popup import PopupWindow
from bauiv1lib import party

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

calls: List[Callable] = []
get_v1_account = None

def get_icons():
    return list(bui.SpecialChar)

def all_icons():
    return [bui.charstr(i) for i in get_icons()] + [
           '✾', '✿', '❀', '❁', '❂', '❃','✶', '✷',
           '✸', '✹', '✺','✞', '✟', '✠', '✢', '✣',
           '✤', '✥', '✦', '✧', '✩', '✪', '✫', '✬',
           '✭', '✮', '✯', '✰','❪', '❫','卐','࿗','☭']

def change_icon(msg: str):
    key = ['/i', '/']
    icons = all_icons()
    
    if key[0] in msg or key[0].upper() in msg:
        for n, icon in enumerate(icons):
            cmd = key[0] + str(n) + key[1]
            cmd2 = cmd.upper()
            if cmd in msg:
                msg = msg.replace(cmd, icon)
            if cmd2 in msg:
                msg = msg.replace(cmd2, icon)
    return msg

class PartyWindow(party.PartyWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._timer = bs.AppTimer(0.1, self._refresh, repeat=True)
        
    def _refresh(self) -> None:
        """Constantly updated."""
        if not self._text_field:
            self._timer = None
            return
        
        text = bui.textwidget(query=self._text_field)
        update_text = change_icon(text)
        bui.textwidget(edit=self._text_field, text=update_text)

def create_chars_file():
    folder = bs.app.python_directory_user + '/Configs'
    file = folder + '/iconsInfo.txt'
    
    if not os.path.exists(folder):
        os.mkdir(folder)
   
    with open(file, 'w') as x:
        for id, char in enumerate(all_icons()):
            try:
                icon = get_icons()[id]
                name_icon = str(icon).split('.')[1].split(':')[0]
            except:
                name_icon = 'ukw_%s' % base64.b64encode(str(id).encode('UTF-8'))
            data = ("id: %s | "
                    "name: %s | "
                    "cmd: %s\n") % (id, name_icon, [char])
            data = data.replace('[', '').replace(']', '').replace('\'', '')
            x.write(data)
            
class IconsWindow(PopupWindow):
    def __init__(self,
                 position: tuple[float, float] = (0.0, 0.0)
                 ) -> None:

        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        scale = 2 if uiscale is bui.UIScale.SMALL else 1.3
        ipos = 0
        self._width = 380 * 1.46
        self._height = 300
        sub_width = self._width - 90
        sub_height = 100*6
        v = sub_height - 30
        bg_color = (0.5, 0.4, 0.6)

        self.collect = {}

        self.root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition='in_scale',
            scale=scale)
            
        self._cancel_button = bui.buttonwidget(parent=self.root_widget,
            position=(50, self._height - 30), size=(50, 50),
            scale=0.5, label=bui.charstr(bui.SpecialChar.BACK),button_type='backSmall',
            color=(1,0,0),on_activate_call=self.on_popup_cancel,autoselect=True)
        bui.containerwidget(edit=self.root_widget,cancel_button=self._cancel_button)

        self._make_sw  = lambda: bui.scrollwidget(parent=self.root_widget, position=(30, 30),
                                     size=(self._width - 60, self._height - 70))
            
        self._scrollwidget = self._make_sw()

        self.buttontab = bui.buttonwidget(parent=self.root_widget,size=(150*1.3, 60),
            scale=0.5,position=(60*3.6, self._height - 45),label="All Icons | ID",
            color=(0.3, 0.8, 0.8),button_type='tab',autoselect=True)
            
        self._subcontainer = None
        self._plus()
        
    def _plus(self) -> None:
        large = 8
        util = all_icons
        len_icons = len(util())
        count = math.ceil(len_icons / large)
        
        sub_height = (300/5) * count
        v = sub_height - 50
        u = 10
        self._subcontainer = c = bui.containerwidget(parent=self._scrollwidget,
                                 size=(self._width, sub_height),
                                 background=False)

        s = {'y': 0, 'id': 0}
        for n in range(len_icons):
            s['x'] = 0
            
            for icon in range(large):
                
                id = s['id']
                
                if id >= len_icons:
                    break
                
                bui.buttonwidget(parent=c,position=(u+s['x'],v-(60*s['y'])),size=(40,40),button_type='square',
                    label=util()[id],color=(0.8,0.8,0.8),autoselect=True,
                    on_activate_call=bs.Call(bs.screenmessage, "/i" + str(id) + "/"))
                    
                s['x'] += 60
                s['id'] += 1
                
            s['y'] += 1
        
    def on_popup_cancel(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        from baBearModz import ModzWindow
        
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')
            bs.apptimer(0.1, bs.Call(ModzWindow, transition='in_scale'))
        
def add_plugin() -> None:
    try: from baBearModz import BearPlugin
    except Exception as e:
        return bs.timer(2.5, lambda e=e:
               bs.screenmessage('Error plugin: ' + str(e), (1,0,0)))

    BearPlugin(icon='logo',
               button_color=(0.8, 1.3, 0.8),
               creator='@PatrónModz',
               plugin=Icons,
               window=IconsWindow)
            
# ba_meta export plugin
class Icons(bs.Plugin):
    def __init__(self) -> None:
        calls.append(bs.chatmessage)
        party.PartyWindow = PartyWindow
        create_chars_file()
        add_plugin()