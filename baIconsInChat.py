# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING, cast

import bascenev1 as bs
import bauiv1 as bui

import base64, os
from bauiv1lib.keyboard.englishkeyboard import EnglishKeyboard
from bauiv1lib import party

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

calls: List[Callable] = []
get_v1_account = None

def set_icons():
    return [(bui.SpecialChar.CROWN),
            (bui.SpecialChar.DRAGON),
            (bui.SpecialChar.SKULL),
            (bui.SpecialChar.HEART),
            (bui.SpecialChar.FEDORA),
            (bui.SpecialChar.HAL),
            (bui.SpecialChar.YIN_YANG),
            (bui.SpecialChar.EYE_BALL),
            (bui.SpecialChar.HELMET),
            (bui.SpecialChar.MUSHROOM),
            (bui.SpecialChar.NINJA_STAR),
            (bui.SpecialChar.VIKING_HELMET),
            (bui.SpecialChar.MOON),
            (bui.SpecialChar.SPIDER),
            (bui.SpecialChar.FIREBALL),
            (bui.SpecialChar.MIKIROG),
            (bui.SpecialChar.LOGO_FLAT),
            (bui.SpecialChar.REWIND_BUTTON),
            (bui.SpecialChar.PLAY_PAUSE_BUTTON),
            (bui.SpecialChar.OUYA_BUTTON_O),
            (bui.SpecialChar.OUYA_BUTTON_U),
            (bui.SpecialChar.OUYA_BUTTON_Y),
            (bui.SpecialChar.OUYA_BUTTON_A),
            (bui.SpecialChar.OUYA_LOGO),
            (bui.SpecialChar.LOGO),
            (bui.SpecialChar.TICKET),
            (bui.SpecialChar.GOOGLE_PLAY_GAMES_LOGO),
            (bui.SpecialChar.TROPHY0A),
            (bui.SpecialChar.TROPHY0B),
            (bui.SpecialChar.TROPHY1),
            (bui.SpecialChar.TROPHY2),
            (bui.SpecialChar.TROPHY3),
            (bui.SpecialChar.TROPHY4),
            (bui.SpecialChar.ALIBABA_LOGO),
            (bui.SpecialChar.TEST_ACCOUNT),
            (bui.SpecialChar.LOCAL_ACCOUNT),
            (bui.SpecialChar.MIKIROG),
            (bui.SpecialChar.OCULUS_LOGO),
            (bui.SpecialChar.STEAM_LOGO),
            (bui.SpecialChar.NVIDIA_LOGO),
            (bui.SpecialChar.PARTY_ICON),
            (bui.SpecialChar.GAME_CIRCLE_LOGO),
            (bui.SpecialChar.V2_LOGO),
            #Flags
            (bui.SpecialChar.FLAG_MEXICO),
            (bui.SpecialChar.FLAG_UNITED_STATES),
            (bui.SpecialChar.FLAG_CANADA),
            (bui.SpecialChar.FLAG_ARGENTINA),
            (bui.SpecialChar.FLAG_CHILE),
            (bui.SpecialChar.FLAG_BRAZIL),
            (bui.SpecialChar.FLAG_RUSSIA),
            (bui.SpecialChar.FLAG_JAPAN),
            (bui.SpecialChar.FLAG_CHINA),
            (bui.SpecialChar.FLAG_SOUTH_KOREA),
            (bui.SpecialChar.FLAG_GERMANY),
            (bui.SpecialChar.FLAG_UNITED_KINGDOM),
            (bui.SpecialChar.FLAG_INDIA),
            (bui.SpecialChar.FLAG_FRANCE),
            (bui.SpecialChar.FLAG_INDONESIA),
            (bui.SpecialChar.FLAG_ITALY),
            (bui.SpecialChar.FLAG_NETHERLANDS),
            (bui.SpecialChar.FLAG_QATAR),
            (bui.SpecialChar.FLAG_ALGERIA),
            (bui.SpecialChar.FLAG_KUWAIT),
            (bui.SpecialChar.FLAG_EGYPT),
            (bui.SpecialChar.FLAG_MALAYSIA),
            (bui.SpecialChar.FLAG_CZECH_REPUBLIC),
            (bui.SpecialChar.FLAG_AUSTRALIA),
            (bui.SpecialChar.FLAG_SINGAPORE),
            (bui.SpecialChar.FLAG_IRAN),
            (bui.SpecialChar.FLAG_POLAND),
            (bui.SpecialChar.FLAG_PHILIPPINES),
            (bui.SpecialChar.FLAG_SAUDI_ARABIA),
            (bui.SpecialChar.FLAG_UNITED_ARAB_EMIRATES)]

def charstr():
    return [bui.charstr(i) for i in set_icons()] + [
           '✾', '✿', '❀', '❁', '❂', '❃','✶', '✷',
           '✸', '✹', '✺','✞', '✟', '✠', '✢', '✣',
           '✤', '✥', '✦', '✧', '✩', '✪', '✫', '✬',
           '✭', '✮', '✯', '✰','❪', '❫']

def change_icon(msg: str):
    key = ['/i', '/']
    icons = charstr()
    
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

def new_chat(msg, *args):
    msg = change_icon(msg)
    return calls[0](msg, *args)

def create_chars_file():
    folder = bs.app.python_directory_user + '/Configs'
    file = folder + '/iconsInfo.txt'
    
    if not os.path.exists(folder):
        os.mkdir(folder)
   
    with open(file, 'w') as x:
        for id, char in enumerate(charstr()):
            try:
                icon = set_icons()[id]
                name_icon = str(icon).split('.')[1].split(':')[0]
            except:
                name_icon = 'ukw_%s' % base64.b64encode(str(id).encode('UTF-8'))
            data = ("id: %s | "
                    "name: %s | "
                    "cmd: %s\n") % (id, name_icon, [char])
            data = data.replace('[', '').replace(']', '').replace('\'', '')
            x.write(data)
            
# ba_meta export plugin
class Icons(bs.Plugin):
    def __init__(self) -> None:
        calls.append(bs.chatmessage)
        party.PartyWindow = PartyWindow
        bs.chatmessage = new_chat
        create_chars_file()