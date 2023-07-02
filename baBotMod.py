# ba_meta require api 8

from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui

import random, json, os, time, math
from bauiv1lib.settings import advanced
from bascenev1lib.actor.spaz import Spaz, PunchHitMessage
from bauiv1lib.popup import PopupWindow, PopupMenuWindow
from bauiv1lib.confirm import ConfirmWindow
from bascenev1lib.mainmenu import MainMenuSession
from bascenev1lib.actor.spazbot import SpazBotSet, BrawlerBot, SpazBot

def settings_distribution():
    return {"Bot Color": (1,0.5,0),
            "Bot Highlight": (1,0,0),
            "Character": 0,
            "HP": 1000,
            "Tab": 'Bot Default',
            "Icon List": 'Icons',
            "Text": 'Bot 3',
            "Icon": '\ue048',
            "Create Bot": {}}

class Sys:
    data: dict[Any, Any] = {}
    dir = bs.app.python_directory_user
    folder = dir + '/Configs'
    file = folder + '/BotModSettings.json'

    @classmethod
    def make(cls) -> None:
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
            cls.data = settings_distribution()
            cls.save()

def getlanguage(txt):
    lang = bs.app.lang.language
    texts = {"Bot Default":{"Spanish": "Bots por defecto",
                 "English": "Default bots",
                 "Portuguese": "Bots padrão"},
             "Create Bot":{"Spanish": "Crea un bot",
                 "English": "Create a bot",
                 "Portuguese": "Crie um bot"},
             "Bot List":{"Spanish": "Lista de bots guardados",
                 "English": "List of saved bots",
                 "Portuguese": "Lista de bots salvos"},
             "Delete Bot":{"Spanish": "¿Quieres eliminar este bot?",
                 "English": "Do you want to delete this bot?",
                 "Portuguese": "Você quer remover este bot?"},
             "Delete Bot Message":{"Spanish": "Bot eliminado",
                 "English": "Bot removed",
                 "Portuguese": "Bot removido"},
             "Save Bot Message":{"Spanish": "Bot Guardado",
                 "English": "Bot Saved",
                 "Portuguese": "Bot salvo"},
             "No Bot Text":{"Spanish": "No hay bots disponibles",
                 "English": "No bots available",
                 "Portuguese": "Nenhum bot disponível"},
             "Bot Exists":{"Spanish": "Este nombre ya está ocupado",
                 "English": "This name is not available",
                 "Portuguese": "Este nome não está disponível"},
             "Add Text":{"Spanish": "Agrégale un nombre a tu bot",
                 "English": "Add a name to your bot",
                 "Portuguese": "Adicione um nome ao seu bot"},
             "Spawn Bot":{"Spanish": "Generar bot",
                 "English": "Spawn Bot",
                 "Portuguese": "Aparecer bot"},
             "Bot Name":{"Spanish": "Nombre",
                 "English": "Name",
                 "Portuguese": "Nome"},
             "Forbidden Menu":{"Spanish": "No disponible desde el menú",
                 "English": "Not available in the menu",
                 "Portuguese": "Não disponível no menu"},
             "Channel":{"Spanish": "Canal de Youtube",
                 "English": "Youtube Channel",
                 "Portuguese": "Canal do Youtube"},
             "Channel Confirm":{"Spanish": "¿Visitar este canal?",
                 "English": "Enter this channel?",
                 "Portuguese": "Entrar neste canal?"},
             "Flags":{"Spanish": "Banderas",
                 "English": "Flags",
                 "Portuguese": "Bandeiras"},
             "Icons":{"Spanish": "Íconos",
                 "English": "Icons",
                 "Portuguese": "Ícones"},
             "Character Text":{"Spanish": "Personaje",
                 "English": "Character",
                 "Portuguese": "Personagem"},
             "Color Text":{"Spanish": "Color principal",
                 "English": "Main color",
                 "Portuguese": "Cor Principal"},
             "Highlight Text":{"Spanish": "Color secundario",
                 "English": "Secondary color",
                 "Portuguese": "Cor secundária"},
             "AI Evil":
                    {"Spanish": "Bot enemigo (IA)",
                     "English": "Evil bot (IA)",
                     "Portuguese": "Bot do mal (AI)"
                    },
             "AI Buddy":
                    {"Spanish": "Bot compañero (IA)",
                     "English": "Buddy bot (AI)",
                     "Portuguese": "Amigo do bot (AI)"
                    },
            }
                 
    language = ['Spanish', 'Portuguese', 'English']
    if lang not in language:
        lang = 'English'
       
    if txt not in texts:
        return txt
        
    return texts[txt][lang]

def get_bot_list():
    return {"AlexVro":
                {"Character":'Taobao Mascot',"Color":(0,0,1),"Highlight":(0,1,0.9),"Icon":'\ue04d',
                 "Channel": 'https://m.youtube.com/channel/UC3Dh3dEM-y9OF2cWSAQOA0g'},
            "AllStar":
                {"Character":'Taobao Mascot',"Color":(0,0.5,0.7),"Highlight":(0.23,0.23,0.23),"Icon":'\ue035',
                 "Channel": 'https://m.youtube.com/channel/UCP3lS0SE35FNJyLaG6LDkZg'},
            "byANG3L":
                {"Character":'Agent Johnson',"Color":(0.10,0.50,0.10),"Highlight":(0.8,0.23,0.23),"Icon":'\ue033',
                 "Channel": 'https://m.youtube.com/channel/UCSgL3Dz7XDFlj-aYi3VThhQ'},
            "Bastian Diamante":
                {"Character":'Easter Bunny',"Color":(1,1,0),"Highlight":(1,1,1),"Icon":'\ue061',
                 "Channel": 'https://m.youtube.com/channel/UC0i6aEz_uWwqDgkPEhNA32A'},
            "BomberYT":
                {"Character":'Frosty',"Color":(0.10,0.10,0.50),"Highlight":(0,0.8,0.8),"Icon":'\ue05f',
                 "Channel": 'https://m.youtube.com/channel/UC72b06dZNM1WEctkhhq0cSw'},
            "Cxzr":
                {"Character":'Spaz',"Color":(1,1,1),"Highlight":(0,0.9,0.8),"Icon":'\ue033',
                 "Channel": 'https://m.youtube.com/channel/UC9MmSna8xJfG0l5pZvKNeWQ'},
            "Dani Squad":
                {"Character":'Spaz',"Color":(1,1,0),"Highlight":(0,1,0),"Icon":'\ue033',
                 "Channel": 'https://m.youtube.com/channel/UCQBFKexZZzVRwm4LJl3oAJQ'},
            "Froshlee14K":
                {"Character":'Bernard',"Color":(0.23,0.23,0.23),"Highlight":(0,0.8,0.9),"Icon":'\ue043',
                 "Channel": 'https://m.youtube.com/channel/UCUCaAkivMPDLh_ZQpNFcoMQ/featured'},
            #"Locuras":
            #    {"Character":'Snake Shadow',"Color":(0.0,1.0,0.0),"Highlight":(0.23,0.23,0.23),"Icon":'\ue01e',
            #     "Channel": 'https://m.youtube.com/channel/UCEwKSOYv-EMRKvg2eOLOuAQ/featured'},
            "PatrónModz":
                {"Character":'Bernard',"Color":(1,0.5,0),"Highlight":(1,0,0),"Icon":'\ue048',
                 "Channel": 'https://m.youtube.com/channel/UCWk6lhc1ih4SrL-OTqXnojw'},
            "PeMexZ":
                {"Character":'Taobao Mascot',"Color":(0.1,1,0.1),"Highlight":(0.8,0,0),"Icon":'\ue033',
                 "Channel": 'https://m.youtube.com/channel/UCkCtfh-XGjYTQrtfZGHLlKw'},
            "Tu Loco ADMK":
                {"Character":'Mel',"Color":(0,1,0),"Highlight":(1,1,1),"Icon":'\ue01e',
                 "Channel": 'https://m.youtube.com/channel/UCVV2GRj66yZNh1Fe9oFN1Kw'},
            "VaL3N - DWH":
                {"Character":'Taobao Mascot',"Color":(0,0.2,1),"Highlight":(0.23,0.23,0.23),"Icon":'\ue05f',
                 "Channel": 'https://m.youtube.com/channel/UCHkhvCkI7RAxnR0kwYZR2hw'}}

def banned_name():
    return ["Bot 3", "Bot", "Antonio", "Luis", "Edgar", "Pro",
            "Bombsquad", "Eric", "Froemling", "UwU",
            "Gloria", "Egg", "Quixote", "Texas", "Puta",
            "Ohio", "Lou", "Gordo", "Negro", "Locureishon", "Gringo",
            "Alberto", "Josa", "Josafatxlol", "Emilio", "Oscar", "Puto"]

def get_character():
    return list(bs.app.classic.spaz_appearances)
    
def get_icons():
    return ["\ue043","\ue048","\ue046","\ue047","\ue041",
            "\ue042","\ue044","\ue045","\ue049","\ue04a",
            "\ue04b","\ue04c","\ue04d","\ue04e","\ue04f",
            "\ue062","\ue026","\ue00c","\ue01e","\ue063",
            "\ue01d","\ue019","\ue01a","\ue01b","\ue01c",
            "\ue05b","\ue020","\ue030","\ue05c","\ue031",
            "\ue02b","\ue02c","\ue02f"]
    
def get_flags():
    return ["\ue033","\ue032","\ue039","\ue05f","\ue061",
            "\ue035","\ue036","\ue03b","\ue037","\ue03f",
            "\ue034","\ue038","\ue03a","\ue03c","\ue03d",
            "\ue03e","\ue040","\ue051","\ue054","\ue053",
            "\ue052","\ue056","\ue057","\ue058","\ue059",
            "\ue05d","\ue05e","\ue060","\ue055","\ue050"]

GLOBAL = {"Advanced": [], "Bot": [], "ID": 0}

def bot_ID():
    GLOBAL['ID'] += 2
    a = random.randint(1,10000*10)
    b = GLOBAL['ID']
    return (f'#{a-b}')

def bot_mod(self):
    if not isinstance(self.session, MainMenuSession):
        bui.containerwidget(edit=self._root_widget,transition='out_left')
        BotModWindow()
    else:
        bs.getsound('error').play()
        bs.screenmessage(getlanguage('Forbidden Menu'),(1,0,0))
    
class BotChest:
    pass
    
class BotSet(SpazBotSet):
    node: bs.Node = None
    owner: bs.Node = None
    buddy: bool = False

    def _update(self) -> None:
        a = bs.get_foreground_host_activity()
        
        try:
            bot_list = self._bot_lists[self._bot_update_list] = ([
                b for b in self._bot_lists[self._bot_update_list] if b])
            self.node = bot_list[-1].node
        except Exception:
            bot_list = []

        self._bot_update_list = (self._bot_update_list +
                                 1) % self._bot_list_count

        player_pts = []
        
        nodes = []
        
        if self.buddy:
            nodes = list(getattr(a, 'ai_evil_bots', []))
            for spaz in self.getspazzes():
                if spaz.source_player:
                    nodes.append(spaz)
        
        nodes.append(self.node)
        
        for node in self.getspazzes():
            try:
                cls = node.getdelegate(object)
                if node in nodes or cls._dead:
                    continue
                player_pts.append((bs.Vec3(node.position),
                                   bs.Vec3(node.velocity)))
                    
            except Exception:
                pass

        for bot in bot_list:
            bot.set_player_points(player_pts)
            bot.update_ai()

        try:
            if not self.owner.exists() or not self.node.exists():
                self._bot_update_timer = None
                self.node.handlemessage(bs.DieMessage())
        except:
            pass
            
    def getspazzes(self) -> list:
        spazzes = []
        if bs.getnodes() != []:
            for node in bs.getnodes():
                if node.getnodetype() == 'spaz':
                    spazzes.append(node)
        return spazzes

class CustomBot(BrawlerBot):
    run: bool = True
    buddy: bool = False
    default_boxing_gloves: bool = False
    
    def __init__(self, **kwargs):
        super().__init__()
        
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        self.apply()
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, PunchHitMessage):
            try:
                node = bs.getcollision().opposingnode
                if node.getnodetype() == 'spaz':
                    self._pick_up(node)
            except Exception as e:
                print(type(e))
        return super().handlemessage(msg)
    
    def apply(self) -> None:
        self.hitpoints_max = self.hitpoints
        self.node.color = self.bot_color
        self.node.highlight = self.bot_highlight
        self.bg._update(self.node)
        
        if self.buddy:
            a = bs.get_foreground_host_activity()
            a.ai_evil_bots.append(self.node)
        
class BotGenerator:
    def __init__(self,
                 icon: str = '\ue030',
                 botname: str = 'Bot 3',
                 character: str = 'Bernard',
                 enable_sound: bool = True,
                 color: Sequence[float] = (1.0,0.5,0.0),
                 highlight: Sequence[float] = (1.0,0.0,0.0),
                 hp: int = 2550,
                 category: str = 'Neutral',
                 ) -> None:
        
        foreground = f = bs.get_foreground_host_activity()
        
        self.enable_sound = enable_sound
        self.character = character
        self.color = color
        self.icon = icon
        self.botname = botname
        
        with foreground.context:
            if not hasattr(f, 'evil_bots'):
                f.evil_bots = []
                
                f.buddy_bots = []
                f.ai_evil_bots = []
                
                f.evil_bots = BotSet()
                f.buddy_bots = BotSet()
                f.buddy_bots.buddy = True
                
            try:
                activity = bs.getactivity()
                actor = activity.players[0].actor
                position = actor.node.position
            except:
                position = (1.0, 3.0, 1.0)
           
            if category == 'AI Evil':
                class EvilBot(CustomBot):
                    bot_highlight = highlight
                    character = self.character
                    bot_color = color
                    hitpoints = hp
                    bg = self

                f.evil_bots.spawn_bot(
                    bot_type=EvilBot,
                    pos=position,
                    spawn_time=0.0,
                    on_spawn_call=None)
                return

            elif category == 'AI Buddy':
                class BuddyBot(CustomBot):
                    source_player = actor.source_player
                    bot_highlight = highlight
                    character = self.character
                    bot_color = color
                    hitpoints = hp
                    buddy = True
                    bg = self

                
                f.buddy_bots.spawn_bot(
                    bot_type=BuddyBot,
                    pos=position,
                    spawn_time=0.0,
                    on_spawn_call=None)
                return
                
            else:
                bot = Spaz(character=character,
                           highlight=highlight,
                           color=color,
                           can_accept_powerups=False).autoretain()

            bot.hitpoints = hp
            bot.hitpoints_max = hp
            
            self._update(bot.node)
            
            bot.node.handlemessage(
                bs.StandMessage(position=(
                    position[0]-2+random.random()*3,
                    position[1]+0.5,
                    position[2]-2+random.random()*3)))

            if self.character == "Bernard":
                bot.node.handlemessage('celebrate', 1000*10)

        if self.enable_sound:
            bui.getsound('shieldUp').play()

    def _update(self, bot: ba.Node) -> None:
        NameInGame(owner=bot,
                   name=(f"{self.icon}{self.botname}"),
                   name_color=bs.safecolor(self.color, target_intensity=0.75))

class NameInGame:
    def __init__(self,
                 owner: bs.Node = None,
                 name: str = 'CHARACTER',
                 name_color: Sequence[float] = (1.0 ,1.0 ,1.0),
                 name_scale: Sequence[float] = (0.0, 0.7, 0.0)):

        m = bs.newnode('math',owner=owner,attrs={'input1': name_scale,'operation': 'add'})
        owner.connectattr('position_center', m, 'input2')
        text: bs.Node = bs.newnode(
            owner=owner,
            type='text',
            attrs={'text': name,
                   'in_world': True,
                   'scale': 0.02,
                   'shadow': 0.5,
                   'flatness': 1.0,
                   'color': name_color,
                   'h_align': 'center'}) 
        m.connectattr('output', text, 'position')
        bs.animate(text, 'scale', {0: 0.017,0.4: 0.017, 0.5: 0.014})

##### WINDOW ####
class BotModWindow(PopupWindow):
    def __init__(self, transition: str = 'in_right'):
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.tab_buttons = {}
        self.tab_data = {}
        self.info_bot = {}

        self.defaultbot = get_bot_list()
        self.set_characters = get_character()
        self._current_tab = Sys.data['Tab']
        self.createbot = Sys.data['Create Bot']

        self.tabdefs = {
            "Bot Default": ['heart',(1.0, 0.0, 0.5)],
            "Create Bot": ['inventoryIcon', (1.0, 1.0, 1.0)],
            "Bot List": ['folder', (0.9, 0.9, 0.0)],
            #"AI Bots": ['settingsIcon', (1.0, 1.0, 1.0)]
            }

        app = bui.app.ui_v1
        uiscale = app.uiscale

        self._root_widget = bui.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5 if uiscale is bui.UIScale.SMALL else 1.0,
                           stack_offset=(0,-30) if uiscale is bui.UIScale.SMALL else  (0,0))
        
        self._back_button = b = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(60,self._height-15),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=bui.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=bs.Call(self._back2))
        bui.buttonwidget(edit=self._back_button, button_type='backSmall',size=(60, 60),label=bui.charstr(bui.SpecialChar.BACK))

        bui.containerwidget(edit=self._root_widget,cancel_button=b)
        self.titletext = bui.textwidget(parent=self._root_widget,position=(0, height-15),size=(width,50),
                          h_align="center",color=(1,1,1),v_align="center",maxwidth=width*1.3)
        
        pst = 0
        for tab in self.tabdefs:
            self.tab_buttons[tab] = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                   position=(620,self._height-50*1.5-pst),size=(170*1.5, 60),
                                   scale=1,text_scale=1.1,label=getlanguage(tab),icon_color=(self.tabdefs[tab][1]),
                                   icon=bui.gettexture(self.tabdefs[tab][0]),iconscale=1.1,enable_sound=False,
                                   on_activate_call=bs.Call(self._set_tab,tab,sound=True))
            pst += 80
        
        self._make_sw  = lambda: bui.scrollwidget(
            parent=self._root_widget, position=(self._width*0.08,51*1.8),
            size=(self._sub_width -140,self._scroll_height +60*1.2),
            selection_loops_to_parent=True)
            
        self._scrollwidget = self._make_sw()
        self._tab_container = None
        
        self._set_tab(self._current_tab)
        bs.apptimer(0.0, bs.Call(self._in_game))

    def _back2(self):
        try: self._saved_text()
        except: pass
        self._back()

    def _set_tab(self, tab, sound=False):
        if Sys.data['Tab'] != tab:
            if self._scrollwidget:
                self._scrollwidget.delete()
                self._scrollwidget = self._make_sw()
                
        Sys.data['Tab'] = tab
        self.sound = sound
        Sys.save()
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()

        if self.sound:
            bui.getsound('click01').play()

        bui.textwidget(edit=self.titletext,text=getlanguage(tab))

        if tab == "Bot Default":
            sub_height = len(self.defaultbot) / 0.5 * 88
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
            
            bot_x = 150
            bot_y = 40
            position = 0
            for bot in self.defaultbot:
                bot_pos = len(bot) * 1.5
                character = self.defaultbot[bot]['Character']
                appearance = bui.app.classic.spaz_appearances[character]
                texture = bui.gettexture(appearance.icon_texture)
                tint_texture = bui.gettexture(appearance.icon_mask_texture)
                color = self.defaultbot[bot]['Color']
                highlight = self.defaultbot[bot]['Highlight']
                link = self.defaultbot[bot]['Channel']
                
                sz = 110
                
                t = bui.textwidget(parent=c,position=(bot_x-20+bot_pos,v-bot_y-position),size=(205 * 1.8,53),
                    h_align="center",color=(bui.app.ui_v1.title_color), v_align="center",maxwidth=width*1.6,
                    text=(f"Youtuber: {bot}"))
                
                self.img_bot = bui.imagewidget(parent=c,position=(bot_x-110, v-bot_y-position-60),size=(sz,sz),
                                mesh_transparent=bui.getmesh('image1x1'),texture=texture,
                                mask_texture=bui.gettexture('characterIconMask'),tint_texture=tint_texture,
                                tint_color=color,tint2_color=highlight)
                
                self.buttonyoutube = bui.buttonwidget(parent=c,autoselect=True,
                       position=(bot_x+120*1.7,v-position-100),size=(130,40),
                       label=getlanguage('Channel'),scale=1.2,text_scale=1.2,
                       color=(0.6, 0.53, 0.63),enable_sound=False,
                       on_activate_call=bs.Call(self._youtuber,link,bot))
                
                b = bui.buttonwidget(parent=c,autoselect=True,
                       position=(bot_x+20,v-position-100),size=(130,40),
                       label=getlanguage('Spawn Bot'),
                       color=(0.5,0.5,1),enable_sound=True,scale=1.2)
                       
                bui.buttonwidget(edit=b, on_activate_call=bs.Call(self._spawn_bot,
                        b, dict(
                        botname=bot,
                        icon=self.defaultbot[bot]['Icon'],
                        character=self.defaultbot[bot]['Character'],
                        color=self.defaultbot[bot]['Color'],
                        highlight=self.defaultbot[bot]['Highlight'])
                    ))
                       
                position += 60*2.9
                
        elif tab == "Create Bot":
            sub_height = 450
            v = sub_height - 55
            width = 300
            self.info_bot = {}

            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
            
            tp = 40
            t = bui.textwidget(parent=c,position=(60*1.3-tp,v-20*1.8),size=(205 * 1.8,53),selectable=False,
                              h_align="center",color=(bui.app.ui_v1.title_color), text=getlanguage('Add Text'), v_align="center",maxwidth=width*1.6)
            
            self.iconpos = (240*1.8,v - 90)
            self.tab_data['Icon'] = bui.buttonwidget(parent=c,position=self.iconpos,size=(40,40),
                            color=(0.52,0.48,0.63),label=Sys.data['Icon'],button_type='square',repeat=False,
                            scale=1.3,autoselect=True,on_activate_call=bs.Call(self._icon))
            
            self.tab_data['Editable Text'] = bui.textwidget(parent=c,position=(60*1.3-tp,v-50*1.8),size=(205 * 1.8,53),selectable=True,
                              editable=True,max_chars=16,description=bui.Lstr(resource='editProfileWindow.nameText'),
                              h_align="center",color=(1,1,1), text=Sys.data['Text'], v_align="center",maxwidth=width*1.6)
            
            v -= 100
            
            sz = 150
            len_char = len(self.set_characters) - 1
            g = min(Sys.data['Character'], len_char)
            appearance = bui.app.classic.spaz_appearances[self.set_characters[g]]
            texture = bui.gettexture(appearance.icon_texture)
            tint_texture = bui.gettexture(appearance.icon_mask_texture)
            self.img_character = bui.imagewidget(parent=c,position=(180, v-140*1.5),size=(sz,sz),
                            mesh_transparent=bui.getmesh('image1x1'),texture=texture,
                            mask_texture=bui.gettexture('characterIconMask'),tint_texture=tint_texture,
                            tint_color=Sys.data['Bot Color'],tint2_color=Sys.data['Bot Highlight'])

            bot_name = bui.Lstr(translate=("characterNames", self.set_characters[g]))
            self.text_bot_name = bui.textwidget(parent=c, position=(61,v-55), size=(205 * 1.8,53),
                    h_align="center", color=bui.app.ui_v1.title_color,
                    text=bot_name, v_align="center", maxwidth=width*1.6)

            bot_pos = 0
            for button_bot in ["Bot Color", "Bot Highlight"]:
                self.tab_data[button_bot] = bui.buttonwidget(parent=c,position=(100+bot_pos,v - 200),size=(40,40),label='',button_type='square',
                            color=Sys.data[button_bot],scale=1.3,autoselect=True,on_activate_call=bs.Call(self._make_picker,button_bot))
                bot_pos += 250
    
            arrow_pos = 0
            for arrow in ["\ue001", "\ue002"]:
                self.tab_data[arrow] = bui.buttonwidget(parent=c,position=(100+arrow_pos,v - 100),size=(40,40),
                            label=arrow,button_type='square',repeat=True,
                            scale=1.3,autoselect=True,on_activate_call=bs.Call(self._character_arrow, arrow))
                arrow_pos += 250

            self.tab_data['Save'] = bui.buttonwidget(parent=c,position=(190,v - 280),size=(100,40),color=(0.4,0.4,0.8),enable_sound=False,
                    label=bui.Lstr(resource='saveText'),scale=1.3,autoselect=True,on_activate_call=bs.Call(self._save_bot))
                    
            self.tab_data['Spawn'] = bui.buttonwidget(parent=c,position=(190 * 0.1, v - 280),size=(100,40),color=(0.4,0.8,0.8),enable_sound=True,
                    label=getlanguage('Spawn Bot'),scale=1.3,autoselect=True,on_activate_call=self.spawn_bot_instant)
                    
            self.tab_data['HP'] = bui.buttonwidget(parent=c,position=(190 * 1.9, v - 280),size=(100,40),color=(0.8,0.4,0.8),enable_sound=True,
                    label=('HP'),scale=1.3,autoselect=True,on_activate_call=bs.Call(Windowscito, value='HP', config=Sys.data, max=[1000, 50, 7000]))

        elif tab == "Bot List":
            sub_height = len(self.createbot) / 0.5 * 88
            v = sub_height - 55
            width = 300
            botname = getlanguage('Bot Name')
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            for bot, client in self.createbot.items():
                char = client['Character']
                if char not in get_character():
                    self.createbot.pop(bot)
                    self._set_tab('Bot List')
                    return

            if len(self.createbot) == 0:
                t = bui.textwidget(parent=c,position=(80,v-150),size=(205 * 1.8,53),
                    h_align="center",color=(bui.app.ui_v1.title_color), text=getlanguage('No Bot Text'), v_align="center",maxwidth=width*1.6)

            bot_x = 125
            bot_y = 40
            position = 0
            for bot in self.createbot:
                bot_pos = len(bot) * 1.5
                character = self.createbot[bot]['Character']
                appearance = bui.app.classic.spaz_appearances[character]
                texture = bui.gettexture(appearance.icon_texture)
                tint_texture = bui.gettexture(appearance.icon_mask_texture)
                color = self.createbot[bot]['Color']
                highlight = self.createbot[bot]['Highlight']
                
                sz = 110
                bp = bot_pos * 5
                
                t = bui.textwidget(parent=c,position=(bot_x-20+bot_pos,v-bot_y-position),size=(205 * 1.8,53),
                    h_align="center",color=(bui.app.ui_v1.title_color), v_align="center",maxwidth=width*1.6,
                    text=(f"{botname}: {bot}"))
                
                self.img_bot = bui.imagewidget(parent=c,position=(bot_x-110, v-bot_y-position-60),size=(sz,sz),
                                mesh_transparent=bui.getmesh('image1x1'),texture=texture,
                                mask_texture=bui.gettexture('characterIconMask'),tint_texture=tint_texture,
                                tint_color=color,tint2_color=highlight)

                b = bui.buttonwidget(parent=c,autoselect=True,
                       position=(bot_x+20,v-bot_y-position-60),size=(130,40),
                       label=getlanguage('Spawn Bot'),color=(0.5,0.5,1),
                       enable_sound=True,scale=1.2)
                       
                bui.buttonwidget(edit=b, on_activate_call=bs.Call(
                    self._spawn_bot, b, dict(
                        botname=bot,
                        icon=self.createbot[bot]['Icon'],
                        character=self.createbot[bot]['Character'],
                        color=self.createbot[bot]['Color'],
                        highlight=self.createbot[bot]['Highlight'],
                        hp=self.createbot[bot]['HP'])
                    ))
       
                self.info_bot[bot] = bui.buttonwidget(parent=c,autoselect=True,
                       position=(bot_x+120*2+bp/1.2,v+10-bot_y-position),size=(40,40),
                       label='?',color=(0.5,0.5,1),button_type='square',
                       scale=0.7,on_activate_call=bs.Call(self._bot_info,bot,
                       self.createbot[bot]['ID'],
                       self.createbot[bot]['Icon'],
                       self.createbot[bot]['Character'],
                       self.createbot[bot]['Color'],
                       self.createbot[bot]['Highlight']))
       
                self.tab_data[bot] = bui.buttonwidget(parent=c,position=(bot_x+120*1.7,v-bot_y-position-60),
                    size=(130,40),color=(0.6, 0.53, 0.63),scale=1.2,text_scale=0.8,
                    label=bui.Lstr(resource='deleteText'),autoselect=True,
                    on_activate_call=bs.Call(
                    self._delete_bot,bot))
                       
                position += 60*2.9
                
        for select_tab,button_tab in self.tab_buttons.items():
            if select_tab == tab:
                bui.buttonwidget(edit=button_tab,color=(0.5,0.4,0.93))
            else: bui.buttonwidget(edit=button_tab,color=(0.52,0.48,0.63))

    def spawn_bot_instant(self) -> None:
        g = Sys.data['Character']
        kwargs = dict(
            botname=Sys.data['Text'],
            character=self.set_characters[g],
            color=Sys.data['Bot Color'],
            highlight=Sys.data['Bot Highlight'],
            icon=Sys.data['Icon'],
            hp=Sys.data['HP'])
        self._spawn_bot(self.tab_data['Spawn'], kwargs)
                
    def _spawn_bot(self, button: bui.Widget, attrs: dict) -> None:
        pos = button.get_screen_space_center()
        bot_type = ['AI Buddy', 'AI Evil', 'Neutral']
        bot_type_lstr = [bui.Lstr(value=getlanguage(s)) for s in bot_type]
        
        p = PopupMenuWindow(
                delegate=self,
                position=pos,
                scale=2.5,
                choices=bot_type,
                choices_display=bot_type_lstr,
                current_choice='none')
                
        p.attrs = attrs
        p.tag = 'Spawn Bot'
        
    def popup_menu_selected_choice(self, popup: PopupMenuWindow, choice: str) -> None:
        if popup.tag == 'Spawn Bot':
            BotGenerator(**popup.attrs, category=choice)
            
    def popup_menu_closing(self, popup: PopupMenuWindow) -> None:
        pass

    def _save_bot(self):
        self._saved_text()
        self.text = Sys.data['Text']
        if self.text in self._not_duplicate():
            bui.getsound('error').play()
            bs.screenmessage(bui.Lstr(resource='nameNotEmptyText'))
            return
        if self.text in self.createbot:
            bui.getsound('error').play()
            bs.screenmessage(getlanguage('Bot Exists'),(1.0,0.5,0.0))
            return
        if self.text in get_bot_list():
            bui.getsound('error').play()
            bs.screenmessage(bui.Lstr(resource='unavailableText'))
            return
        for name in banned_name():
            name = name.upper()
            text = self.text.upper()
            if name in text:
                bui.getsound('error').play()
                bs.screenmessage(bui.Lstr(resource='unavailableText'))
                return
        
        self._bot_appearance()
        self.save_bot_actions()
        
    def _bot_appearance(self):
        g = Sys.data['Character']
        name = Sys.data['Text']
        character = self.set_characters[g]
        color = Sys.data['Bot Color']
        highlight = Sys.data['Bot Highlight']
        icon = Sys.data['Icon']
        hp = Sys.data['HP']
        
        Sys.data['Create Bot'][name] = {"Character": character, "HP": hp, "Color": color,
                                   "Highlight": highlight,"Icon": icon, "ID": bot_ID()}
        
    def save_bot_actions(self):
        bui.getsound('gunCocking').play()
        bs.screenmessage(f"{getlanguage('Save Bot Message')}: {Sys.data['Text']}",(0,1,0))

    def _delete_bot(self, delete_bot):
        text = (f"{getlanguage('Delete Bot')}\n\"{delete_bot}\"")
        def confirm():
            del Sys.data['Create Bot'][delete_bot]
            self._set_tab('Bot List')
            bs.screenmessage(f"{getlanguage('Delete Bot Message')}: {delete_bot}",(1,0,0))
            bui.getsound('shieldDown').play()
        ConfirmWindow(text,width=400, height=120, action=confirm, ok_text=bui.Lstr(resource='okText'))

    def _character_arrow(self, arrow):
        count = len(self.set_characters) - 1
        if arrow == "\ue001":
            if Sys.data['Character'] == 0:
                Sys.data['Character'] = count
            else: Sys.data['Character'] -= 1
        else:
            if Sys.data['Character'] == count:
                Sys.data['Character'] = 0
            else: Sys.data['Character'] += 1
            
        g = Sys.data['Character']
        appearance = bui.app.classic.spaz_appearances[self.set_characters[g]]
        texture = bui.gettexture(appearance.icon_texture)
        tint_texture = bui.gettexture(appearance.icon_mask_texture)
        bui.imagewidget(edit=self.img_character,tint_texture=tint_texture,texture=texture)
        bot_name = bui.Lstr(translate=("characterNames", self.set_characters[g]))
        bui.textwidget(edit=self.text_bot_name, text=bot_name)

    def _make_picker(self,tag):
        from bauiv1lib.colorpicker import ColorPicker
        if tag == 'Bot Color': initial_color = Sys.data['Bot Color']
        elif tag == 'Bot Highlight': initial_color = Sys.data['Bot Highlight']
        ColorPicker(parent=self._root_widget,position=(0,0),
        initial_color=initial_color,delegate=self,tag=tag)
        
    def color_picker_closing(self, picker):
        pass

    def color_picker_selected_color(self, picker, color):
        tag = picker.get_tag()
        if tag == 'Bot Color':
            Sys.data['Bot Color'] = color
            bui.buttonwidget(edit=self.tab_data['Bot Color'] , color=color)
        elif tag == 'Bot Highlight':
            Sys.data['Bot Highlight'] = color
            bui.buttonwidget(edit=self.tab_data['Bot Highlight'] , color=color)
        bui.imagewidget(edit=self.img_character,tint_color=Sys.data['Bot Color'],tint2_color=Sys.data['Bot Highlight'])

    def _icon(self):
        self._saved_text()
        IconWindow(pos=(self.iconpos[0]-60*6,self.iconpos[1]-60*2),
                   callback=bs.Call(self._set_tab, Sys.data['Tab']))
        
    def _youtuber(self, link, channel):
        YT = getlanguage('Channel Confirm')
        text = (f"{YT} \n \"{channel}\"")
        def confirm():
            bui.open_url(link)
        ConfirmWindow(text,width=400, height=120, action=confirm, ok_text=bui.Lstr(resource='okText'))
        bui.getsound('ding').play()

    def _bot_info(self, bot, ID, icon, character,
                  color: float, highlight: float):
        
        c1 = self._converter(color[0])
        c2 = self._converter(color[1])
        c3 = self._converter(color[2])

        h1 = self._converter(highlight[0])
        h2 = self._converter(highlight[1])
        h3 = self._converter(highlight[2])

        char = getlanguage('Character Text')
        name = getlanguage('Bot Name')
        gcolor = getlanguage('Color Text')
        ghighlight = getlanguage('Highlight Text')
        strcolor = (f'({c1}, {c2}, {c3})')
        strhighlight = (f'({h1},{h2},{h3})')
        strhp = Sys.data['Create Bot'][bot]['HP']
        
        text = (f"ID: {ID}" "\n"
                f"HP: {strhp}" "\n"
                f"{char}: {character}" "\n"
                f"{name}: {icon}{bot}" "\n"
                f"{gcolor}: {strcolor}" "\n"
                f"{ghighlight}: {strhighlight}")
        
        ConfirmWindow(text,width=200,
            height=100*1.5,cancel_button=False,
            origin_widget=self.info_bot[bot],
            ok_text=bui.Lstr(resource='okText'))

    def _converter(self, color):
        create_text = ""
        repeat = 0        
        for number in str(color):
            if repeat == 3: break
            else: create_text += number
            repeat += 1
        return create_text

    def _not_duplicate(self):
        text = ""
        duplicate = []        
        for x in range(20):
            duplicate.append(text)
            text += " "
        return duplicate

    def _saved_text(self):
        Sys.data['Text'] = bui.textwidget(query=self.tab_data['Editable Text'])

    def _in_game(self):
        session = bs.get_foreground_host_session()
        if isinstance(session, MainMenuSession):
            bui.getsound('error').play()
            bs.screenmessage(getlanguage('Forbidden Menu'), color=(1, 0, 0))
            self._back()

    def _back(self):
        bui.containerwidget(edit=self._root_widget,transition='out_left')
        advanced.AdvancedSettingsWindow()
        self._saved_text()
        Sys.save()
        
class IconWindow(PopupWindow):
    def __init__(self, pos=(0,0), callback=None):
        self.callback = callback
        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        scale = 2 if uiscale is bui.UIScale.SMALL else 1.3
        ipos = 0
        self._width = 380
        self._height = 300
        sub_width = self._width - 90
        sub_height = 100*6
        v = sub_height - 30
        bg_color = (0.5, 0.4, 0.6)
        self.time = time.time()

        self._current_tab = Sys.data['Icon List']
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

        iconlist = [("Icons",getlanguage('Icons')), ("Flags",getlanguage('Flags'))]
        for x,j in iconlist:
            self.collect[x] = bui.buttonwidget(parent=self.root_widget,size=(150*1.3, 60),
                scale=0.5,position=(60*1.5+ipos, self._height - 45),label=j,
                button_type='tab',enable_sound=False,autoselect=True,
                on_activate_call=bs.Call(self._set_tab,x,sound=True))
            ipos += 100
            
        self._subcontainer = None
        self._set_tab(self._current_tab)

    def _set_tab(self, tab, sound=False):
        if Sys.data['Icon List'] != tab:
            if self._scrollwidget:
                self._scrollwidget.delete()
                self._scrollwidget = self._make_sw()
        
        self.sound = sound
        Sys.data['Icon List'] = tab
        Sys.save()

        if self._subcontainer is not None and self._subcontainer.exists():
            self._subcontainer.delete()
            
        if self.sound:
            self._tick_and_call()

        if tab == 'Icons':
            large = 5
            len_icons = len(get_icons())
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
                        label=get_icons()[id],color=(0.8,0.8,0.8),on_activate_call=bs.Call(self._icons,id),autoselect=True)
                        
                    s['x'] += 60
                    s['id'] += 1
                    
                s['y'] += 1
      
        elif tab == 'Flags':
            large = 5
            len_icons = len(get_flags())
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
                        label=get_flags()[id],color=(0.8,0.8,0.8),on_activate_call=bs.Call(self._flags,id),autoselect=True)
                        
                    s['x'] += 60
                    s['id'] += 1
                    
                s['y'] += 1

        for icons in self.collect:
            if icons == tab:
                bui.buttonwidget(edit=self.collect[icons],color=(0.5, 0.4, 0.93))
            else: bui.buttonwidget(edit=self.collect[icons],color=(0.52, 0.48, 0.63))

    def _icons(self, icon):
        Sys.data['Icon'] = get_icons()[icon]
        self._on_cancel_press()

    def _flags(self, flag):
        Sys.data['Icon'] = get_flags()[flag]
        self._on_cancel_press()

    def _tick_and_call(self):
        bui.getsound('click01').play()

    def on_popup_cancel(self) -> None:
        self._on_cancel_press()
        
    def _on_cancel_press(self) -> None:
        self._transition_out()
        self.callback()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

class Windowscito(PopupWindow):
    def __init__(self,
                 value: str = '',
                 config: dict = {},
                 round: int = 2,
                 max: list[float] = [1, 1, 10]):
        self.value = value
        self.max = max
        self.round = round
        self.config = config

        m = 5.0
        bgc = (0.5, 0.25, 0.5)
        size = (70.0 * m, 70.0 * m)
        sc = 1.0 if bui.app.ui_v1.uiscale is bui.UIScale.SMALL else 0.6
        
        PopupWindow.__init__(self,
            position=(0.0, 0.0),
            size=size, scale=sc,
            bg_color=bgc)
        
        rw = self.root_widget
        cancel_btn = bui.buttonwidget(parent=rw,
            autoselect=True, color=(0.83, 0.33, 0.33),
            position=(size[0]*0.1, size[1]*0.8), size=(40, 40),
            scale=1.0, label='', icon=bui.gettexture('crossOut'),
            on_activate_call=self.on_popup_cancel)
        bui.containerwidget(edit=self.root_widget, cancel_button=cancel_btn)
        
        self.num_text = bui.textwidget(parent=rw,position=(size[0]*0.35, size[1]*0.5),
            size=(size[0]*0.31,50), scale=2.3,
            color=(0.11, 1.0, 0.11),h_align="center",v_align="center",
            text=f"{config[value]}/{max[2]}",maxwidth=size[0]*0.35*30)
        
        _x = -10
        btn = bui.buttonwidget(parent=rw,
            autoselect=True, color=(1.0, 0.0, 0.0), repeat=True,
            position=(_x+size[0]*0.3, size[1]*0.1), size=(50, 50),
            scale=1.5, label='-', button_type='square',
            on_activate_call=bs.Call(self._call, '-'))
            
        btn = bui.buttonwidget(parent=rw,
            autoselect=True, color=(0.0, 0.4, 1.0), repeat=True,
            position=(_x+(size[0]*0.3)*1.85, size[1]*0.1), size=(50, 50),
            scale=1.5, label='+', button_type='square',
            on_activate_call=bs.Call(self._call, '+'))
        
    def _call(self, type: str) -> None:
        cf = self.config
        n = self.config[self.value]
        
        if type == '+':
            m = self.max[2]
            if n >= m:
                self.config[self.value] = self.max[0]
            else:
                self.config[self.value] += self.max[1]
        else:
            m = self.max[0]
            if n <= m:
                self.config[self.value] = self.max[2]
            else:
                self.config[self.value] -= self.max[1]

        self.config[self.value] = round(self.config[self.value], self.round)
        bui.app.config.apply_and_commit()
        v = self.config[self.value]
        bui.textwidget(edit=self.num_text, text=f"{v}/{self.max[2]}")

    def on_popup_cancel(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        Sys.save()
        
def add_plugin():
    try: from baBearModz import BearPlugin
    except Exception as e:
        return bs.apptimer(2.5, lambda e=e:
               bs.screenmessage('Error plugin: ' + str(e), (1,0,0)))
               
    BearPlugin(icon='cuteSpaz',
               creator='@PatrónModz',
               button_color=(0.25, 1.05, 1.05),
               plugin=BotMod,
               window=BotModWindow)

# ba_meta export plugin
class BotMod(bs.Plugin):
    def __init__(self) -> None:
        add_plugin()
        Sys.make()