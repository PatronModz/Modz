# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui

import random,time,datetime,weakref,json,os
from bauiv1lib.profile.edit import EditProfileWindow as Epw
from bauiv1lib.popup import PopupWindow
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bauiv1lib.profile.browser import ProfileBrowserWindow
from bascenev1._profile import PLAYER_COLORS

if TYPE_CHECKING:
    pass

_sp_ = "\n"

# Lang
def getlanguage(text, subs: str = '', almacen: list = []):
    if not any(almacen):
        almacen = [a for a in range(1000)]
        lang = bs.app.lang.language
        
    translate = {"Action 1":
                      {"Spanish": "Coloración",
                       "English": "Coloration",
                       "Portuguese": "Coloração"},
                 "Creator":
                      {"Spanish": "Mod creado por @PatrónModz",
                       "English": "Mod created by @PatrónModz",
                       "Portuguese": "Mod creado by @PatrónModz"},
                 "Mod Info":
                      {"Spanish": f"Con este mod podrás disfrutar{_sp_} de colores brillantes",
                       "English": f"With this mod you will be able{_sp_} to enjoy bright colors",
                       "Portuguese": f"Com este mod você pode desfrutar{_sp_} de cores brilhantes"}}
    
    languages = ['Spanish','Portuguese','English']
    if lang not in languages: lang = 'English'

    if text not in translate:
        return text
    return translate[text][lang]

def settings_distribution():
    return {"Fluo": {},
           }

# Useful
class Sys:
    data: dict[str, Any] = {}
    dir = bs.app.python_directory_user
    folder = dir + '/Configs'
    file = folder + '/FCSettings.json'
    
    @classmethod
    def make_scripts(cls) -> None:
        if not os.path.exists(cls.folder):
            os.mkdir(cls.folder)
            
        if not os.path.exists(cls.file):
            with open(cls.file, 'w') as f1:
                f1.write('{}')
                
        with open(cls.file) as f1: 
            r = f1.read()
            cls.data = json.loads(r)
            
        cls.new()

    @classmethod
    def save(cls) -> None:
        if os.path.exists(cls.file):
            with open(cls.file, 'w') as f1:
                w = json.dumps(cls.data, indent=4)
                f1.write(w)
          
    @classmethod
    def new(cls) -> None:
        if len(cls.data) == 0:
            cls.data = settings_distribution()
            cls.save()

# Material
def calculate(a,b,c=2):
    try: value = round(a*b/100,c)
    except: value = 0
    return value
    
def petage(a,b,c=2):
    try: value = round(100*a/b,c)
    except: value = 0
    return value

def new_fluo_color():
    fluocolors = []
    for val in Sys.data['Fluo'].values():
        f = val[0]
        c = val[1]
        fluo = (c[0]+calculate(f[0],c[0]),
                c[1]+calculate(f[1],c[1]),
                c[2]+calculate(f[2],c[2]))
        fluocolors.append(fluo)
    return fluocolors
        
GLOBAL = {"Tab": 'Action 1'}

PlayerSpaz.fcspsi = PlayerSpaz.__init__
def new_ps_init(self, *args, **kwargs):
    self.fcspsi(*args, **kwargs)
    playercolor = kwargs['color']
    playerhighlight = kwargs['highlight']
    confluo = Sys.data['Fluo']
    for val in confluo.values():
        f = val[0]
        c = val[1]
        fluo = (c[0]+calculate(f[0],c[0]),
                c[1]+calculate(f[1],c[1]),
                c[2]+calculate(f[2],c[2]))
                
        if val[1] == playercolor:
            self.node.color = fluo
        if val[1] == playerhighlight:
            self.node.highlight = fluo

class FluoColorsWindow(PopupWindow):
    def __init__(self, transition= 'in_right'):
        columns = 2
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.tab_buttons = {}
        self.pys_data = []

        self.tabdefs = {"Action 1": ['buttonSquare',(1,1,1)],
                        "Action 2": ['heart',(1,0,0.5)]}
                        
        self.listdef = list(self.tabdefs)
        
        self.count = len(self.tabdefs) - 1
                        
        self._current_tab = GLOBAL['Tab']

        app = bui.app.ui_v1
        uiscale = app.uiscale

        self._root_widget = bui.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5 if uiscale is bui.UIScale.SMALL else 1.0,
                           stack_offset=(0,-30) if uiscale is bui.UIScale.SMALL else  (0,0))
        
        self._backButton = b = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(60,self._height-15),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=bui.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=bui.Call(self._back))
        bui.buttonwidget(edit=self._backButton, button_type='backSmall',size=(60, 60),label=bui.charstr(bui.SpecialChar.BACK))
        bui.containerwidget(edit=self._root_widget,cancel_button=b)
        
        self.titletext = bui.textwidget(parent=self._root_widget,position=(0, height-15),size=(width,50),
                          h_align="center",color=bui.app.ui_v1.title_color, text='titletext', v_align="center",maxwidth=width*1.3)
        
        index = 0
        for tab in range(self.count):
            for tab2 in range(columns):
                
                tag = self.listdef[index]
                
                position = (620+(tab2*120),self._height-50*2.5-(tab*120))
                
                text = bui.Lstr(resource='gatherWindow.aboutText')
                label = getlanguage(tag)
                
                if tag == 'Action 2':
                    label = text
                
                self.tab_buttons[tag] = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                        position=position,size=(110,110),
                                        scale=1,label='',enable_sound=False,
                                        button_type='square',on_activate_call=bui.Call(self._set_tab,tag,sound=True))
                                       
                self.text = bui.textwidget(parent=self._root_widget,
                            position=(position[0]+55,position[1]+30),
                            size=(0, 0),scale=1,color=bui.app.ui_v1.title_color,
                            draw_controller=self.tab_buttons[tag],maxwidth=100,
                            text=label,h_align='center',v_align='center')
                                       
                self.image = bui.imagewidget(parent=self._root_widget,
                             size=(60,60),color=self.tabdefs[tag][1],
                             draw_controller=self.tab_buttons[tag],
                             position=(position[0]+25,position[1]+40),
                             texture=bui.gettexture(self.tabdefs[tag][0]))

                index += 1
        
                if index > self.count:
                    break
       
            if index > self.count:
                break
        
        self._scrollwidget = None
        self._tab_container = None
        self._set_tab(self._current_tab)

    def __del__(self) -> None:
        Sys.save()

    def _set_tab(self, tab, sound: bool = False, rescrollwidget = True):
        self.sound = sound
        GLOBAL['Tab'] = tab

        bui.textwidget(edit=self.titletext,text=getlanguage(tab))
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()

        if self.sound:
            bui.getsound('click01').play()

        if rescrollwidget:
            if self._scrollwidget:
                self._scrollwidget.delete()
    
            self._scrollwidget = bui.scrollwidget(parent=self._root_widget,
                position=(self._width*0.08,51*1.8),size=(self._sub_width -140,self._scroll_height +60*1.2))

        if tab == 'Action 1':
            colors = Sys.data['Fluo']
            sub_height = len(colors)*140.5
            v = sub_height - 55
            width = 300
            dpos = 0
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
                
            for x,i in colors.items():
                size = 90
                position = (10, v-40-dpos)
                color = (1.2, 0.8, 0.9)
                b = Sys.data['Fluo'][x][0]
                fluo = (i[1][0]+calculate(b[0],i[1][0]),
                        i[1][1]+calculate(b[1],i[1][1]),
                        i[1][2]+calculate(b[2],i[1][2]))
            
                previmg = bui.imagewidget(parent=c,
                          size=(size,size),color=i[1],
                          position=position,
                          texture=bui.gettexture('buttonSquare'))
                          
                text = bui.textwidget(parent=c,position=(position[0]+22,position[1]+30),size=(width,50),
                       h_align="center",color=(1,1,1),text=bui.charstr(bui.SpecialChar.RIGHT_ARROW),
                       v_align="center",maxwidth=width*1.3,scale=2.8)
                          
                previmg2 = bui.imagewidget(parent=c,
                          size=(size,size),color=fluo,
                          position=(position[0]+260,position[1]),
                          texture=bui.gettexture('buttonSquare'))
                    
                npsi = (position[0]+390,position[1]+5)
                buton = bui.buttonwidget(parent=c,autoselect=True,
                        position=npsi,
                        color=(0.5,1.0,0.5),size=(50,50),scale=1.6,label='',
                        texture=bui.gettexture('settingsIcon'),
                            on_activate_call=bui.Call(self._window_fluo,x))
                dpos += calculate(160,90)
                
        elif tab == 'Action 2':
            sub_height = 0
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            t = bui.textwidget(parent=c,position=(110, v-20),size=(width,50),
                      scale=1.4,color=(0.2,1.2,0.2),h_align="center",v_align="center",
                      text=("FluoColors-Mod v1.0.0"),maxwidth=width*30)

            t = bui.textwidget(parent=c,position=(110, v-90),size=(width,50),
                      scale=1,color=(1.3,0.5,1.0),h_align="center",v_align="center",
                      text=getlanguage('Creator'),maxwidth=width*30)

            t = bui.textwidget(parent=c,position=(110, v-220),size=(width,50),
                      scale=1,color=(1.0,1.2,0.3),h_align="center",v_align="center",
                      text=getlanguage('Mod Info'),maxwidth=width*30)
        
        for select_tab,button_tab in self.tab_buttons.items():
            if select_tab == tab:
                bui.buttonwidget(edit=button_tab,color=(0.5,0.4,1.5))
            else: bui.buttonwidget(edit=button_tab,color=(0.52,0.48,0.63))

    def _window_fluo(self, ID):
        CustomFluoColor(idcolor=ID,
                        callback=bui.Call(
                            self._set_tab,'Action 1',rescrollwidget=False))

class CustomFluoColor(PopupWindow):
    def __init__(self, idcolor: int, position=(0,0), callback = None):
        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        scale = 2 if uiscale is bui.UIScale.SMALL else 1.3
        self._width = 560
        self._height = 360
        sub_width = self._width - 90
        sub_height = 100*6
        v = self._height - 30
        bg_color = (0.5, 0.4, 0.6)
        self.max_brightness = 400
        self.index  = idcolor
        self.callback = callback
        self.intensity_board = {}
        self.rgb_texts = []

        super().__init__(position=position,
                         size=(self._width, self._height),
                         scale=scale,bg_color=bg_color)

        self._cancel_button = bui.buttonwidget(parent=self.root_widget,
            position=(50, self._height - 30), size=(50, 50),
            scale=0.5, label=bui.charstr(bui.SpecialChar.BACK),button_type='backSmall',
            color=(1,0,0),on_activate_call=self.on_popup_cancel,autoselect=True)
        bui.containerwidget(edit=self.root_widget,cancel_button=self._cancel_button)

        fluo = Sys.data['Fluo'][idcolor][0]
        rgb_index = 0
        
        rgb_pos = 0
        for rgb in fluo:
            posi = (40+rgb_pos, v-290)
            
            b = bui.buttonwidget(parent=self.root_widget,autoselect=True,
                    position=posi,size=(50,50),scale=0.8,label='-',repeat=True,
                    on_activate_call=bui.Call(self._coloration,rgb_index,'-'))
                    
            b = bui.buttonwidget(parent=self.root_widget,autoselect=True,
                    position=(posi[0]+60,posi[1]),size=(50,50),scale=0.8,label='+',
                    repeat=True,on_activate_call=bui.Call(self._coloration,rgb_index,'+'))
                    
            color = (1,0,0) if rgb_index == 0 else (0,1,0) if rgb_index == 1 else (0,0.7,1)
            rgbtext = bui.textwidget(parent=self.root_widget,position=(posi[0]+30,posi[1]+40),size=(50,50),
                      h_align="center",color=color, text=str(rgb)+'%', v_align="center",maxwidth=280)
            self.rgb_texts.append(rgbtext)
        
            rgb_index += 1
            rgb_pos += 150
            
        dpos = 0
        for inten in range(9):
            size = 40
            pos = (440*1.1, v-270+dpos)
            intensity = bui.imagewidget(parent=self.root_widget,
                        size=(size,size),
                        position=pos,color=PLAYER_COLORS[14],
                        texture=bui.gettexture('buttonSquare'))
            self.intensity_board[inten+1] = intensity
            dpos += 30
        
            intensity = self.update_intensity(fluo)
            self._intensity_color(intensity)
        
        self.expct_txt = bui.textwidget(parent=self.root_widget,position=(410, v-135),size=(50,50),
                         h_align="center",color=(1,1,1), text=str(self.expct)+'%', v_align="center",maxwidth=280)
        
        up = bui.buttonwidget(parent=self.root_widget,autoselect=True,
                    position=(418, v-80),size=(50,50),scale=0.65,button_type='square',
                    label=bui.charstr(bui.SpecialChar.UP_ARROW),repeat=True,
                    on_activate_call=bui.Call(self.percentage,'+'))
                    
        down = bui.buttonwidget(parent=self.root_widget,autoselect=True,
                    position=(418, v-170),size=(50,50),scale=0.65,repeat=True,
                    label=bui.charstr(bui.SpecialChar.DOWN_ARROW),button_type='square',
                    on_activate_call=bui.Call(self.percentage,'-'))

        size = 120
        color = Sys.data['Fluo'][idcolor]
        c = color[1]
        f = color[0]
        fluov = (c[0]+calculate(f[0],c[0]),
                 c[1]+calculate(f[1],c[1]),
                 c[2]+calculate(f[2],c[2]))
        
        self.previmg = bui.imagewidget(parent=self.root_widget,
                       size=(size,size),color=fluov,
                       position=(200, v-170),
                       texture=bui.gettexture('buttonSquare'))
        
        tx = (f"r: {fluov[0]:.2f}" + _sp_ +
              f"g: {fluov[1]:.2f}" + _sp_ +
              f"b: {fluov[2]:.2f}" + _sp_).upper()
        self.RGB_TXT = bui.textwidget(parent=self.root_widget,position=(110, v-150),size=(50,50),
                         h_align="center",color=(1,1,1), text=tx, v_align="center",maxwidth=280)
        
    def _coloration(self, ID: int, tag: str):
        fluo = Sys.data['Fluo'][self.index][0]
        if tag == '-': fluo[ID] = max(fluo[ID]-1, 1)
        elif tag == '+': fluo[ID] = min(fluo[ID]+1, self.max_brightness)
        self.update_rgb_text(fluo, ID)
        count = self.update_intensity(fluo)
        self._intensity_color(count)
        self.update_square()
        self.update_pct()
        self.update_rgb_text_info()
        Sys.save()

    def _intensity_color(self, intensity):
        max_inten = intensity
        color = PLAYER_COLORS[14]
      
        for num,text in self.intensity_board.items():
            bui.imagewidget(edit=text,color=color)
      
        index = 0
        for x,t in self.intensity_board.items():
            if max_inten == index: break
            index += 1
            if index in [1,2,3]:
                color = (0.3,1.5,0.3)
            if index in [4,5,6]:
                color = (1.5,1.5,0.3)
            if index in [7,8,9]:
                color = (1.5,0.3,0.3)
            bui.imagewidget(edit=t,color=color)
            
    def percentage(self, tag: str = ''):
        if tag == '+':
            self.expct = min(self.expct+1,100)
        elif tag == '-':
            self.expct = max(self.expct-1,1)
        self.pct_thg()
        
    def update_intensity(self, fluo: list):
        intensity = 0
        count = 0
        num = self.max_brightness * len(self.rgb_texts)
        
        for f in fluo: intensity += f
        intensity = int(petage(intensity,num))
        intensity = max(intensity,1)

        for c in range(1,intensity+1):
            if (c%11) == 0: count += 1
        self.expct = intensity
        return count

    def update_pct(self):
        bui.textwidget(edit=self.expct_txt,text=str(self.expct)+'%')

    def pct_thg(self):
        num = len(self.rgb_texts) * self.max_brightness
        fluo = Sys.data['Fluo'][self.index]
        v3 = calculate(self.expct, num)
        v3 = int(v3/3)
        fluo[0] = [v3,v3,v3]
        self.upd_all_dates()

    def update_rgb_text(self, rgb: list, ID: int):
        num = rgb[ID]
        text = self.rgb_texts[ID]
        bui.textwidget(edit=text,text=str(num)+'%')
            
    def update_square(self):
        color = Sys.data['Fluo'][self.index]
        c = color[1]
        f = color[0]
        fluo = (c[0]+calculate(f[0],c[0]),
                 c[1]+calculate(f[1],c[1]),
                 c[2]+calculate(f[2],c[2]))
        bui.imagewidget(edit=self.previmg, color=fluo)
            
    def update_rgb_text_info(self):
        color = Sys.data['Fluo'][self.index]
        c = color[1]
        f = color[0]
        fluov = (c[0]+calculate(f[0],c[0]),
                 c[1]+calculate(f[1],c[1]),
                 c[2]+calculate(f[2],c[2]))
        tx = (f"r: {fluov[0]:.2f}" + _sp_ +
              f"g: {fluov[1]:.2f}" + _sp_ +
              f"b: {fluov[2]:.2f}" + _sp_).upper()
        bui.textwidget(edit=self.RGB_TXT, text=tx)

    def upd_all_dates(self):
        fluo = Sys.data['Fluo'][self.index][0]
        for th in range(3):
            self.update_rgb_text(fluo,th)
        count = self.update_intensity(fluo)
        self._intensity_color(count)
        self.update_rgb_text_info()
        self.update_square()
        self.update_pct()
            
    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')
            self.callback()
            
    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()

def update_data() -> None:
    if not any(Sys.data['Fluo']):
        index = 0
        for index, color in enumerate(PLAYER_COLORS):
            Sys.data['Fluo'][index] = [[1,1,1], color]
            
def add_plugin():
    try: from baBearModz import BearPlugin
    except Exception as e:
        return bs.apptimer(2.5, lambda e=e:
               bs.screenmessage('Error plugin: ' + str(e), (1,0,0)))
               
    BearPlugin(icon='buttonSquare',
               creator='@PatrónModz',
               button_color=(0.70, 0.20, 0.50),
               window_color=(0.1/2, 0.4/2, 0.7/2),
               plugin=FluoColors,
               window=FluoColorsWindow)
            
def fluo_colors_plugin():
    PlayerSpaz.__init__ = new_ps_init
    Sys.make_scripts()
    update_data()
    
# ba_meta export plugin
class FluoColors(bs.Plugin):
    def __init__(self) -> None:
        fluo_colors_plugin()
        add_plugin()