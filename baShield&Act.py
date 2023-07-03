"""SandA."""

# ba_meta require api 8

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

import bascenev1 as bs
import bauiv1 as bui

import random,time,datetime,weakref,json,os
from bascenev1lib.actor.spazappearance import *

from bauiv1lib.profile.edit import EditProfileWindow
from bauiv1lib.profile.browser import ProfileBrowserWindow
from bauiv1lib.colorpicker import ColorPicker
from bauiv1lib.popup import PopupWindow, PopupMenu
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.bomb import BombFactory
from bascenev1lib.actor.flag import FlagFactory
from bascenev1lib.actor.powerupbox import PowerupBox
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spazfactory import SpazFactory

class Articles:
    def translate(x):
        tras = {
             "Button Style":
                {"Spanish": "Nuevo Estilo",
                 "English": "New Style",
                 "Portuguese": "Novo Estilo"},
             "Character":
                {"Spanish": "Mi Personaje",
                "English": "My Character",
                "Portuguese": "Meu personagem"},
             "Shield":
                {"Spanish": "Electro-escudo",
                "English": "Shield",
                "Portuguese": "Escudo"},
             "Actor":
                {"Spanish": "Actor   ",
                "English": "Actor    ",
                "Portuguese": "Ator   "},
             "Head":{"Spanish": "Cabeza",
                "English": "Head",
                "Portuguese": "Cabeça"},
             "Hand":{"Spanish": "Manos",
                "English": "Hands",
                "Portuguese": "Mãos"},
             "Pelvis":{"Spanish": "Pelvis",
                "English": "Pelvis",
                "Portuguese": "Pélvis"},
             "Color":{"Spanish": "Color del personaje",
                 "English": "Character color",
                 "Portuguese": "Cor do personagem"},
             "Mask":{"Spanish": "Textura",
                 "English": "Texture",
                 "Portuguese": "Textura"},
             "Torso":{"Spanish": "Torso",
                 "English": "Torso",
                 "Portuguese": "Tronco"},
             "Toes":{"Spanish": "Dedos de los pies",
                 "English": "Toes",
                 "Portuguese": "Dedos do pé"},
             "Style":{"Spanish": "Estilo",
                 "English": "Style",
                 "Portuguese": "Estilo"},
             "Others":{"Spanish": "Otros...",
                 "English": "Others...",
                 "Portuguese": "Outras..."},
             "Shield Text 1":{"Spanish": "Escudo con",
                 "English": "Shield with",
                 "Portuguese": "Escudo com"},
             "Shield Text Color":{"Spanish": "Color del personaje",
                 "English": "Character color",
                 "Portuguese": "Cor do personagem"},
             "Shield Text Name":{"Spanish": "Mostrar salud",
                 "English": "Show health",
                 "Portuguese": "Mostrar saúde"},
             "Shield text 2":{"Spanish": "Color personalizado",
                 "English": "Custom color",
                 "Portuguese": "Cor customizada"},
             "Shield text 3":{"Spanish": "Tamaño del escudo",
                 "English": "Shield size",
                 "Portuguese": "Tamanho do escudo"},
             "Others Text 1":{"Spanish": "Personaliza la textura (BANDERA)",
                 "English": "Customize the texture (FLAG)",
                 "Portuguese": "Personalize a textura (FLAG)"},
             "Others Text 2":{"Spanish": "Personaliza la textura (TNT)",
                 "English": "Customize the texture (TNT)",
                 "Portuguese": "Personalize a textura (TNT)"},
             "Actor Name":{"Spanish": "Mostrar salud del personaje.",
                 "English": "Show character health.",
                 "Portuguese": "Mostre a saúde do personagem."},
             "Mode Invisibility":{"Spanish": "Los Jugadores aparecen invisibles.",
                 "English": "Players are invisible.",
                 "Portuguese": "Os jogadores são invisíveis."},
             "Mode Night":{"Spanish": "Modo oscuro.",
                 "English": "Dark mode.",
                 "Portuguese": "Modo escuro."},
             "Random Character":{"Spanish": "Aparecer con un personaje aleatorio.",
                 "English": "Appear with a random character.",
                 "Portuguese": "Aparece com um caractere aleatório."},
             "Random Powerup":{"Spanish": "Los jugadores aparecen con \nun potenciador aleatorio.",
                 "English": "Players appear with a random powerup.",
                 "Portuguese": "Os jogadores aparecem com \num power-up aleatório."},
             "More Health":{"Spanish": f"Aumentar \"{ats.extra_points()}\" puntos de \"HP\".",
                 "English": f"Increase \"{ats.extra_points()}\" points of \"HP\".",
                 "Portuguese": f"Aumente \"{ats.extra_points()}\" pontos de \"HP\"."}
            }
            
        lang = bs.app.lang.language
        langs = ["Portuguese", "English", "Spanish"]
        if x not in tras:
            return x
        
        if lang not in langs:
            lang = langs[1]
        return tras[x][lang]

    def head():
        return ['neoSpazHead','zoeHead','ninjaHead','kronkHead','melHead','jackHead',
                'santaHead', 'frostyHead','bonesHead','bearHead','penguinHead','aliHead',
                'cyborgHead','agentHead','wizardHead','pixieHead','bunnyHead']
    
    def color():
        return ['neoSpazColor','zoeColor','ninjaColor','kronkColor','melColor','jackColor',
                'santaColor', 'frostyColor','bonesColor','bearColor','penguinColor','aliColor',
                'cyborgColor','agentColor','wizardColor','pixieColor','bunnyColor']
    
    def pelvis():
        return ['neoSpazPelvis','zoePelvis','ninjaPelvis','kronkPelvis','melPelvis','jackPelvis',
                'santaPelvis', 'frostyPelvis','bonesPelvis','bearPelvis','penguinPelvis','aliPelvis',
                'cyborgPelvis','agentPelvis','wizardPelvis','pixiePelvis','bunnyPelvis']
    
    def colormask():
        return ['neoSpazColorMask','zoeColorMask','ninjaColorMask','kronkColorMask','melColorMask','jackColorMask',
                'santaColorMask', 'frostyColorMask','bonesColorMask','bearColorMask','penguinColorMask','aliColorMask',
                'cyborgColorMask','agentColorMask','wizardColorMask','pixieColorMask','bunnyColorMask']
    
    def toes():
        return ['neoSpazToes','zoeToes','ninjaToes','kronkToes','melToes','jackToes',
                'santaToes', 'frostyToes','bonesToes','bearToes','penguinToes','aliToes',
                'cyborgToes','agentToes','wizardToes','pixieToes','bunnyToes']
    
    def hand():
        return ['neoSpazHand','zoeHand','ninjaHand','kronkHand','melHand','jackHand',
                'santaHand', 'frostyHand','bonesHand','bearHand','penguinHand','aliHand',
                'cyborgHand','agentHand','wizardHand','pixieHand','bunnyHand']
    
    def torso():
        return ['neoSpazTorso','zoeTorso','ninjaTorso','kronkTorso','melTorso','jackTorso',
                'santaTorso', 'frostyTorso','bonesTorso','bearTorso','penguinTorso','aliTorso',
                'cyborgTorso','agentTorso','wizardTorso','pixieTorso','bunnyTorso']
    
    def style():
        return ['female','kronk','santa','frosty','bones','bear',
                'penguin','spaz','bunny','pixie']
    
    def images():
        return [i.split('.')[0] for i in
                os.listdir('ba_data/textures/')]
    
    def _characters():
        return ['Spaz','Kronk','Bones','Frosty','Santa Claus','Bernard','Pixel',
                'Pascal','Taobao Mascot','Agent Johnson','Grumbledorf','B-9000',
                'Easter Bunny','Zoe','Mel','Snake Shadow']
    
    def extra_points():
        return 6300 - (1000)
    
    def settings_distribution():
        return {"Tab": 'Actor',
                "Shield Color": False,
                "Shield Name": False,
                "Actor Name": False,
                "Mode Night": False,
                "Mode Invisibility": False,
                "Random Character": False,
                "Random Powerup": False,
                "More Health": False,
                "Shield Radius": 1.25,
                "Flag Texture": ats.images().index('flagColor'),
                "TNT Texture": ats.images().index('tnt'),
                "Shield Color Custom": (0.3, 0.2, 2.0),
                "Head": 'neoSpazHead',
                "Torso": 'neoSpazTorso',
                "Color": 'neoSpazColor',
                "Pelvis": 'neoSpazPelvis',
                "Mask": 'neoSpazColorMask',
                "Toes": 'neoSpazToes',
                "Hand": 'neoSpazHand',
                "Style": 'spaz'}

    def _root(root):
        return (bs.app.python_directory_user + root)
    
    def _profiles():
        perfiles = []
        for profiles in bs.app.config['Player Profiles']:
            if profiles == "__account__" or profiles == "‏‏": continue
            icon = bs.app.config['Player Profiles'][profiles]['icon']
            if icon == '\ue01e': icon = ''
            perfiles.append(icon+profiles)
        return perfiles

ats = Articles

class Sys:
    data: dict[Any, Any] = {}
    dir = bs.app.python_directory_user
    folder = dir + '/Configs'
    file = folder + '/' + 'ShieldActSettings' + '.json'

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
        if cls.data == {}:
            cls.data = ats.settings_distribution()
            cls.save()
    
bomb_factory = BombFactory.__init__
def bomb_factory_init(self):
    bomb_factory(self)
    c = Sys.data['TNT Texture']
    self.tnt_tex = bs.gettexture(ats.images()[c])
    
flag_factory = FlagFactory.__init__
def flag_factory_init(self):
    flag_factory(self)
    c = Sys.data['Flag Texture']
    self.flag_texture = bs.gettexture(ats.images()[c])
    
playerspaz = PlayerSpaz.__init__
def playerspaz_init(self,*args,**kwargs):
    playerspaz(self, *args,**kwargs)
    from bascenev1 import get_default_powerup_distribution as powers

    self._powerups = []
    for powerups,element in powers():
        if powerups in ['curse','health']:
            continue
        self._powerups.append(powerups)
    
    if Sys.data['Random Powerup']:
        self.node.handlemessage(bs.PowerupMessage(
        random.choice(self._powerups),self.node))
    
    if Sys.data['More Health']:
        self.hitpoints += ats.extra_points()
        self.hitpoints_max = self.hitpoints
    
    if Sys.data['Mode Invisibility']:
        self.node.head_mesh = None
        self.node.torso_mesh = None
        self.node.pelvis_mesh = None
        self.node.upper_arm_mesh = None
        self.node.forearm_mesh = None
        self.node.hand_mesh = None
        self.node.upper_leg_mesh = None
        self.node.lower_leg_mesh = None
        self.node.toes_mesh = None
        self.node.style = 'ali'
    
sact = Spaz.__init__
def sact_new_init(self,*args, **kwargs):
    sact(self, *args, **kwargs)
    
    flash = 40
    source_player = (self.node.color[0] * flash,
                     self.node.color[1] * flash,
                     self.node.color[2] * flash)

    if Sys.data['Random Character']:
        factory = SpazFactory.get()
        character = random.choice(ats._characters())
        media = factory.get_media(character)
        self.node.jump_sounds = media['jump_sounds']
        self.node.attack_sounds = media['attack_sounds']
        self.node.impact_sounds = media['impact_sounds']
        self.node.death_sounds = media['death_sounds']
        self.node.pickup_sounds = media['pickup_sounds']
        self.node.fall_sounds = media['fall_sounds']
        self.node.color_texture = media['color_texture']
        self.node.color_mask_texture = media['color_mask_texture']
        self.node.head_mesh = media['head_mesh']
        self.node.torso_mesh = media['torso_mesh']
        self.node.pelvis_mesh = media['pelvis_mesh']
        self.node.upper_arm_mesh = media['upper_arm_mesh']
        self.node.forearm_mesh = media['forearm_mesh']
        self.node.hand_mesh = media['hand_mesh']
        self.node.upper_leg_mesh = media['upper_leg_mesh']
        self.node.lower_leg_mesh = media['lower_leg_mesh']
        self.node.toes_mesh = media['toes_mesh']
        self.node.style = factory.get_style(character)

    if Sys.data['Mode Night']:
        self.node.color = source_player
        bs.getactivity().globalsnode.tint = (0,0,1)
    
    def text():
        m = bs.newnode('math',owner=self.node,attrs={'input1': (0, 1.05, 0),'operation': 'add'})
        self.node.connectattr('position_center', m, 'input2')
        self._text = bs.newnode('text',owner=self.node,
                attrs={'in_world': True,
                      'text': '',
                      'scale': 0.02,
                      'shadow': 0.5,
                      'flatness': 1.0,
                      'color':(1,1,1),
                      'h_align': 'center'}) 
        m.connectattr('output', self._text, 'position')
        bs.animate(self._text, 'scale', {0: 0.017,0.4: 0.017, 0.5: 0.011})
                
    def update_timer():
        heart = bui.charstr(bui.SpecialChar.HEART)
        if self.node.exists():
            hp = None
            if Sys.data['Shield Name']:
                if self.shield:
                    hp = self.shield_hitpoints
                else: self._text.text = ""
                self._text.color = (0,1,0)
            if Sys.data['Actor Name']:
                if self.node:
                    hp = self.hitpoints
                self._text.color = (1,1,1)
            if Sys.data['Shield Name'] and Sys.data['Actor Name']:
                if self.shield:
                    hp = self.shield_hitpoints
                else:
                    hp = self.hitpoints
                self._text.color = (0,1,0) if self.shield else (1,1,1)
                
            if hp is not None:
                self._text.text = (heart + str(int(hp)))
        
    if Sys.data['Shield Name'] or Sys.data['Actor Name']:
        text()
        self._hp_time = bs.Timer(0.1, bs.Call(update_timer),repeat=True)

super_equip_shields = Spaz.equip_shields
def new_equip_shields(self, decay: bool = False) -> None:
    super_equip_shields(self, decay)
    
    flash = 1.5
    nodecolor = (self.node.color[0] * flash,
                 self.node.color[1] * flash,
                 self.node.color[2] * flash)
    Sys.data_color = (Sys.data['Shield Color Custom'][0] * flash,
                 Sys.data['Shield Color Custom'][1] * flash,
                 Sys.data['Shield Color Custom'][2] * flash)
    scolor = nodecolor if Sys.data['Shield Color'] else Sys.data_color
    tcolor = (1,1,1) if Sys.data['Mode Night'] else scolor

    if self.shield is not None:
        self.shield.color = tcolor
        self.shield.radius = Sys.data['Shield Radius']

#### WINDOW ####
class SandAMenu(PopupWindow):
    def __init__(self, transition='in_scale'):
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;

        self._current_tab = Sys.data['Tab']
        self._radius_text = Sys.data['Shield Radius']

        app = bui.app.ui_v1
        uiscale = app.uiscale
                         
        happy = random.randint(1,50)
        if happy == 45:
            name = random.choice(ats._profiles())
            day = (f"Congratulations!! Lucky profile is: {name}")
            color = random.choice([(0,1,1),(0,1,0),(1,0,1),(1,1,0)])
            bui.screenmessage(day,color)
            bui.getsound('cheer').play()
              
        self._root_widget = bui.containerwidget(size=(width,height),transition=transition,
                           scale=1.5 if uiscale is bui.UIScale.SMALL else 1.0, stack_offset=(0,-30) if uiscale is bui.UIScale.SMALL else  (0,0))
        
        self._backButton = b = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(40,self._height-50),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=bui.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=bui.Call(self._back))
        bui.buttonwidget(edit=self._backButton, button_type='backSmall',size=(60, 60),label=bui.charstr(bui.SpecialChar.BACK))

        bui.containerwidget(edit=self._root_widget,cancel_button=b)
        self.titletext = bui.textwidget(parent=self._root_widget,position=(-70, height-60),size=(width,50), force_internal_editing=True,
                          h_align="center",color=bui.app.ui_v1.title_color, v_align="center",maxwidth=width*1.3)
                          
        self._sw = lambda: bui.scrollwidget(
            parent=self._root_widget,
            position=(self._width*0.08,51*1.1),
            size=(self._sub_width -140,self._scroll_height +60*1.2),selection_loops_to_parent=True)
                          
        self._scrollwidget = self._sw()

        self._time_text = bui.textwidget(parent=self._root_widget,position=(100*3.1, height-100*4.3),size=(width,50),
            scale=0.8,h_align="center",color=bui.app.ui_v1.title_color, v_align="center",maxwidth=width*1.1)
        self._time_time = bui.AppTimer(0.1, bui.Call(self.update_time), repeat=True)

        pst = 0
        self.tabs_buttons = []
        self.tabs_defs = ['Character','Actor','Shield','Others']
        for tabs in self.tabs_defs:
            
            icon = ("cuteSpaz" if tabs == 'Character' else
                    "settingsIcon" if tabs == 'Actor' else
                    "powerupShield" if tabs == 'Shield' else "logIcon")
                    
            self.button_tabs = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                   position=(620,self._height-50*2.2-pst),size=(170, 60),
                                   scale=1,text_scale=1.1,label=ats.translate(tabs),
                                   icon=bui.gettexture(icon),iconscale=1.1,
                                   on_activate_call=bui.Call(self._set_tab,tabs))
            self.tabs_buttons.append(self.button_tabs)
            pst += 80
                    
        self._tab_container = None
        self._set_tab(self._current_tab)
        
    def _set_tab(self, tab):
        if Sys.data['Tab'] != tab:
            if self._scrollwidget:
                self._scrollwidget.delete()
                self._scrollwidget = self._sw()
        
        self._current_tab = tab
        Sys.data['Tab'] = tab
        Sys.save()
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()
        self._tab_data = {}

        if tab == 'Character':
            sub_height = 500
            v = sub_height - 55
            c_width = self._scroll_width
            width = 700
            c_height = min(self._scroll_height, 200*1.0+100)
            istab = 0
            #bui.screenmessage( bui.Lstr(resource='settingsWindowAdvanced.mustRestartText'), color=(1.0, 0.5, 0.0))
            bui.textwidget(edit=self.titletext, text=ats.translate('Character'))
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)
 
            pos = 0
            nv = 290
            f = 80*2
            corpo = ['Head','Torso','Color','Pelvis',
                     'Mask','Hand','Toes','Style']
            for char in corpo:
                choices = (ats.head() if char=='Head' else
                           ats.torso() if char=='Torso' else
                           ats.color() if char=='Color' else
                           ats.pelvis() if char=='Pelvis' else
                           ats.colormask() if char=='Mask' else
                           ats.hand() if char=='Hand' else
                           ats.toes() if char=='Toes' else ats.style())
                lstr_choices = [bui.Lstr(value=c) for c in choices]
                xpos = (50-nv if char=='Color' else 
                        50-nv if bui.app.lang.language == "Spanish" else 
                        30-nv if bui.app.lang.language == "Portuguese" else -nv)
                
                _popup_menu_torso = PopupMenu(
                    parent=c,position=(300,270-pos+f),width=90,scale=2.4,
                    choices=choices,
                    choices_display=lstr_choices,
                    current_choice=Sys.data[char],
                    on_value_change_call=bui.Call(self._character,char))
                    
                self.popup_text = bui.textwidget(parent=c,position=(xpos,f-pos+270),size=(width,50),
                          text=ats.translate(char),h_align="center", v_align="center",maxwidth=width*1.3)
                pos += 60
            
        elif tab == 'Actor':
            sub_height = 585
            width = 700
            v = sub_height - 55
            sc = 1.3
            q = -260
            pst = 0
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1+100)
            istab = 1
            bui.textwidget(edit=self.titletext, text=ats.translate('Actor'))

            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)

            values = ['Mode Night','Actor Name','Mode Invisibility',
                      'More Health','Random Character','Random Powerup']
            for actor in values:
                
                self.check = bui.checkboxwidget(parent=c,position=(5,v-pst),value=Sys.data[actor],
                             on_value_change_call=bui.Call(self._switches,actor),maxwidth=self._scroll_width*0.9,
                             text=ats.translate(actor),autoselect=True)
                pst += 100

        elif tab == 'Shield':
            sub_height = 0
            v = sub_height - 55
            q = -260
            width = 700
            pst = 0
            self._txt_list = []
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1.0+100)
            istab = 2
            bui.textwidget(edit=self.titletext, text=ats.translate('Shield'))

            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)

            for text in range(4):
                if text == 0: txt = ats.translate('Shield Text 1')
                elif text == 1: txt = ats.translate('Shield Text 1')
                elif text == 2: txt = ats.translate('Shield text 3')
                else: txt = ats.translate('Shield text 2')

                position = ((50+q,v-pst) if bui.app.lang.language=="Spanish" else
                            (40+q,v-pst) if bui.app.lang.language=="Portuguese" else
                            (q,v-pst)) if text in [2,3] else (q,v-pst)
                
                color = ((1,0,0) if Sys.data['Shield Color']
                         else bui.app.ui_v1.title_color)
                        
                self._info_text_shield = bui.textwidget(parent=c,position=position,size=(width,50),scale=1.2,
                          text=txt,  h_align="center",color=(color if text == 3
                          else bui.app.ui_v1.title_color), v_align="center",maxwidth=width*0.6)
                self._txt_list.append(self._info_text_shield)
                pst += 100
            
            self.check = bui.checkboxwidget(parent=c,position=(265,v+9),value=Sys.data['Shield Color'],
                        on_value_change_call=bui.Call(self._shieldcolor),maxwidth=self._scroll_width*0.9,
                        text=ats.translate('Shield Text Color'),autoselect=True)
            
            self.check2 = bui.checkboxwidget(parent=c,position=(265,v+9-100),value=Sys.data['Shield Name'],
                        on_value_change_call=bui.Call(self._switches,'Shield Name'),maxwidth=self._scroll_width*0.9,
                        text=ats.translate('Shield Text Name'),autoselect=True)

            scp = 0
            array = [("-",1), ("+",2)]
            for button,value in array:
                sc = bui.buttonwidget(parent=c,position=(400+scp*1.6,v - 200),size=(40,40),label=button,
                            autoselect=True,repeat=True,on_activate_call=bui.Call(self._button_sc,value))
                scp += 40
                
            self.t = bui.textwidget(parent=c,position=(-10,v-210),size=(width,50),scale=1.2,
                          text=str(Sys.data['Shield Radius']),h_align="center",color=(0,1,0), v_align="center",maxwidth=width*0.6)
            
            self.shieldcolor = bui.buttonwidget(parent=c,position=(100*3.2,v - 100*3),size=(40,40),label='', button_type='square',
                            color=Sys.data['Shield Color Custom'],scale=1.3,autoselect=True,on_activate_call=bui.Call(self._make_picker,'Shield'))
                            
            self.button_defaultshieldcolor = bui.buttonwidget(parent=c,position=(100*4,v - 100*3),size=(90,40),label='Default', button_type='square',
                            color=(0.3, 0.2, 2.0),scale=1.3,autoselect=True,on_activate_call=bui.Call(self._defaultshieldcolor))
        
        else:
            sub_height = 500
            width = 700
            v = sub_height - 55
            vv = 5
            c_width = self._scroll_width
            c_height = min(self._scroll_height, 200*1+100)
            istab = 3
            bui.textwidget(edit=self.titletext, text=ats.translate('Others'))

            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                            size=(self._sub_width,sub_height),
                            background=False,selection_loops_to_parent=True)

            pt = 20
            g = Sys.data['Flag Texture']
            self.t = bui.textwidget(parent=c,position=(-90,v-pt),size=(width,50),scale=1.2,
                          text=ats.translate('Others Text 1'),h_align="center",color=(1,2,2), v_align="center",maxwidth=width*0.6)
            
            bui.containerwidget(parent=c,position=(110*1.6-110+vv,v - 120-pt),
                                      color=(0.2,0.2,0.7),scale=1.3,size=(300,80),background=True)
            
            self._image_flag = bui.buttonwidget(parent=c,position=(145*1.5+vv,v - 100-pt),size=(50,50),label='', button_type='square',
                        texture=bui.gettexture(ats.images()[g]),color=(1,1,1),scale=1.5,autoselect=True,
                        on_activate_call=bui.Call(self.othersmessage,'Flag'))

            btp = 0
            btnp = ["Min","Max"]
            for btt in btnp:
                spchar = (bui.charstr(bui.SpecialChar.LEFT_ARROW) if btt==("Min") else
                          bui.charstr(bui.SpecialChar.RIGHT_ARROW))
                          
                b1 = bui.buttonwidget(parent=c,position=(80+btp+vv,v - 100-pt),size=(40,40),label=spchar, button_type='square',
                    color=(0,0,1),scale=1.3,autoselect=True,repeat=True,on_activate_call=bui.Call(self._flag_texture,btt))
                btp += 120*2.5
            
            ###TNT
            pt = 290
            g = Sys.data['TNT Texture']
            self.t = bui.textwidget(parent=c,position=(-90,v-pt),size=(width,50),scale=1.2,
                          text=ats.translate('Others Text 2'),h_align="center",color=(2,1,1), v_align="center",maxwidth=width*0.6)
            
            bui.containerwidget(parent=c,position=(110*1.6-110+vv,v - 120-pt),
                                      color=(0.7,0.2,0.2),scale=1.3,size=(300,80),background=True)
            
            self._image_tnt = bui.buttonwidget(parent=c,position=(145*1.5+vv,v - 100-pt),size=(50,50),label='', button_type='square',
                        texture=bui.gettexture(ats.images()[g]),color=(1,1,1),scale=1.5,autoselect=True,
                        on_activate_call=bui.Call(self.othersmessage,'Tnt'))

            btp = 0
            for btt in btnp:
                spchar = (bui.charstr(bui.SpecialChar.LEFT_ARROW) if btt==("Min") else
                          bui.charstr(bui.SpecialChar.RIGHT_ARROW))
                          
                b1 = bui.buttonwidget(parent=c,position=(80+btp+vv,v - 100-pt),size=(40,40),label=spchar, button_type='square',
                    color=(1,0,0),scale=1.3,autoselect=True,repeat=True,on_activate_call=bui.Call(self._tnt_texture,btt))
                btp += 120*2.5
   
        for tab_color in self.tabs_buttons:
            bui.buttonwidget(edit=tab_color,color = (0.5,0.5,0.5))
        bui.buttonwidget(edit=self.tabs_buttons[istab],color = (0.0, 0.9, 0.0))
        
    def _button_sc(self, config):
        val = 0.1
        if config == 1:
            self._radius_text = round(max(0.5,self._radius_text - val), 2)
            bui.textwidget(edit=self.t,text=str(self._radius_text))
            Sys.data['Shield Radius'] = self._radius_text
            Sys.save()
        elif config == 2:
            self._radius_text = round(min(2.5,self._radius_text + val), 2)
            bui.textwidget(edit=self.t,text=str(self._radius_text))
            Sys.data['Shield Radius'] = self._radius_text
            Sys.save()
        
    def _defaultshieldcolor(self):
        Sys.data['Shield Color Custom'] = (0.3, 0.2, 2.0)
        bui.buttonwidget(edit=self.shieldcolor,color=Sys.data['Shield Color Custom'])
        Sys.save()
        
    def _character(self,tag,m):
        Sys.data[tag] = m
        Sys.save()
        
    def _switches(self,tag,m):
        Sys.data[tag] = False if m==0 else True
        Sys.save()
        
    def _flag_texture(self, main):
        n = (len(ats.images()) - 1)
        self._image = Sys.data['Flag Texture']
        if main == 'Max': Sys.data['Flag Texture'] = min(n,self._image + 1)
        elif main == 'Min': Sys.data['Flag Texture'] = max(0,self._image - 1)
        self._flag_update()
    
    def _flag_update(self):
        c = Sys.data['Flag Texture']
        bui.buttonwidget(edit=self._image_flag,texture=bui.gettexture(ats.images()[c]))
        
    def _tnt_texture(self, tnt):
        n = (len(ats.images()) - 1)
        self._image = Sys.data['TNT Texture']
        if tnt == 'Max': Sys.data['TNT Texture'] = min(n,self._image + 1)
        elif tnt == 'Min': Sys.data['TNT Texture'] = max(0,self._image - 1)
        self._tnt_update()
        
    def _tnt_update(self):
        c = Sys.data['TNT Texture']
        bui.buttonwidget(edit=self._image_tnt,texture=bui.gettexture(ats.images()[c]))
        
    def othersmessage(self, message):
        if message == 'Flag':
            o = Sys.data['Flag Texture']
        elif message == 'Tnt':
            o = Sys.data['TNT Texture']
        imgs = ats.images()
        c = imgs[o]
        i = imgs.index(c)
        bui.screenmessage(f"{i}: {c}")
        
    def _shieldcolor(self,m):
        Sys.data['Shield Color'] = False if m==0 else True
        bui.textwidget(edit=self._txt_list[3],color=(1,0,0) if Sys.data['Shield Color'] else bui.app.ui_v1.title_color)
        
    def _make_picker(self,tag):
        if tag == 'Shield': initial_color = Sys.data['Shield Color Custom']
        ColorPicker(parent=self._root_widget,position=(0,0),
        initial_color=initial_color,delegate=self,tag=tag)
    
    def color_picker_closing(self, picker):
        pass

    def color_picker_selected_color(self, picker, color):
        tag = picker.get_tag()
        if tag == 'Shield':
            Sys.data['Shield Color Custom'] = color
            bui.buttonwidget(edit=self.shieldcolor, color=color)
        
    def update_time(self):
        hour = time.strftime('%H:%M:%S')
        date = time.strftime('%d/%m/%Y')
        
        fecha = ("Fecha: " if bui.app.lang.language=='Spanish' else
                 "Data: " if bui.app.lang.language=='Portuguese' else "Date: ")
        hora = ("Hora: " if bui.app.lang.language in ['Spanish','Portuguese'] else "Hour: ")
        
        tiempo = (hora + hour + "\n" + fecha + date)
        
        if self._time_text:
            bui.textwidget(edit=self._time_text, text=tiempo)
        
    def _back(self):
        self._time_time = None
        Sys.save()
        appc()
        bui.containerwidget(edit=self._root_widget,transition='out_right')
        ProfileBrowserWindow(transition='in_left').get_root_widget()

#### ---- ####
def appc() -> None:
    t = Appearance('My Character')
    t.color_texture = Sys.data['Color']
    t.color_mask_texture = Sys.data['Mask']
    t.default_color = (1, 1, 1)
    t.default_highlight = (1, 1, 1)
    t.icon_texture = 'neoSpazIcon'
    t.icon_mask_texture = 'neoSpazIconColorMask'
    t.head_mesh = Sys.data['Head']
    t.torso_mesh = Sys.data['Torso']
    t.pelvis_mesh = Sys.data['Pelvis']
    t.upper_arm_mesh = 'ninjaUpperArm'
    t.forearm_mesh = 'ninjaForeArm'
    t.hand_mesh = Sys.data['Hand']
    t.upper_leg_mesh = 'ninjaUpperLeg'
    t.lower_leg_mesh = 'ninjaLowerLeg'
    t.toes_mesh = Sys.data['Toes']
    ninja_attacks = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    ninja_hits = ['ninjaHit' + str(i + 1) + '' for i in range(8)]
    ninja_jumps = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    t.jump_sounds = ninja_jumps
    t.attack_sounds = ninja_attacks
    t.impact_sounds = ninja_hits
    t.death_sounds = ['ninjaDeath1']
    t.pickup_sounds = ninja_attacks
    t.fall_sounds = ['ninjaFall1']
    t.style = Sys.data['Style']

def plugin():
    BombFactory.__init__ = bomb_factory_init
    FlagFactory.__init__ = flag_factory_init
    PlayerSpaz.__init__ = playerspaz_init
    Spaz.__init__ = sact_new_init
    Spaz.equip_shields = new_equip_shields
    appc()

#### BEARMODZ ####
def add_plugin():
    try: from baBearModz import BearPlugin
    except Exception as e:
        return bs.timer(2.5, lambda e=e:
               bs.screenmessage('Error plugin: ' + str(e), (1,0,0)))

    ShieldAndActor.__name__ = 'Shield&Act'
    BearPlugin(icon='nub',
               icon_color=(0.025, 0.43, 1.1),
               button_color=(1.25, 0.0, 1.25),
               #window_color=(0.25,0.25,0.25),
               creator='@PatrónModz',
               plugin=ShieldAndActor,
               window=SandAMenu)

# ba_meta export plugin
class ShieldAndActor(bs.Plugin):
    def __init__(self):
        Sys.make_scripts()
        add_plugin()
        plugin()
        