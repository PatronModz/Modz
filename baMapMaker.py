# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING

import ba, _ba, random, os, enum
from bastd.ui.popup import PopupWindow, PopupMenu
from bastd.ui.confirm import ConfirmWindow
from bastd.gameutils import SharedObjects
from bastd.ui.colorpicker import ColorPicker
from bastd.actor import playerspaz

PlayerSpaz = playerspaz.PlayerSpaz

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

calls: List = [None]

blocks: List[ba.Node] = []
block_type: str = 'Cube'
block_size: List[float] = [1.0, 1.0, 1.0]
block_color: Sequence[float] = (1.0, 0.0, 0.0)
speed: float = 0.5

ffa_spawns: List[float] = []
team_spawns: List[float] = []
powerup_spawns: List[float] = []
tnt_spawns: List[float] = []
map_name: str = 'Map#' + str(random.randint(0, 100000))
flag_default_spawn: Sequence[float] = None
original_camera_position: Dict[str, Sequence[float]] = {} 

all_block_types: List[str] = [
    'Cube', 'FFA Spawn', 'Team Spawn',
    'Powerup Spawn', 'TNT Spawn', 'Flag Default Spawn']

def save_map_as_plugin():
    meta1 = ['#', 'ba_meta', 'require', 'api', '7']
    meta2 = ['#', 'ba_meta export', 'plugin']
    blks = [f"dict(position={b[0]}, color={b[1]}, size={b[2]}),\n              " for b in blocks]
    
    t1 = [f"points['ffa_spawn{n+1}'] = {pos}\n    " for n, pos in enumerate(ffa_spawns)]
    t2 = [f"points['spawn{n+1}'] = {pos}\n    " for n, pos in enumerate(team_spawns)]
    t3 = [f"points['powerup_spawn{n+1}'] = {pos}\n    " for n, pos in enumerate(powerup_spawns)]
    t4 = [f"points['flag_default'] = {flag_default_spawn}\n    "]
    t5 = [f"points['tnt{n+1}'] = {pos}\n    " for n, pos in enumerate(tnt_spawns)]
    t6 = [f"points['flag{n+1}'] = {pos}\n    " for n, pos in enumerate(team_spawns)]
    
    return """
%s
from __future__ import annotations
from typing import TYPE_CHECKING

import ba, _ba, random
from bastd.ui.popup import PopupWindow
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

class MyMapPoints:
    # This file was automatically generated from "hockey_stadium.ma"
    # pylint: disable=all
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.0, 0.7956858119, 0.0) + (
        0.0, 0.0, 0.0) + (30.80223883, 0.5961646365, 13.88431707)
    boxes['map_bounds'] = (0.0, 0.7956858119, -0.4689020853) + (0.0, 0.0, 0.0) + (
        35.16182389, 12.18696164, 21.52869693)
    %s

class MyMap(ba.Map):

    defs = MyMapPoints
    name = '%s'

    @classmethod
    def get_play_types(cls) -> List[str]:
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'eggTex3'

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {}
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.locs = []
        self.regions = []
        
        self.collision = ba.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        set = [
              %s]

        for i, map in enumerate(set):
            self.locs.append(
                ba.newnode('locator',
                    attrs={'shape': 'box',
                           'position': set[i]['position'],
                           'color': set[i]['color'],
                           'opacity': 1.0,
                           'draw_beauty': True,
                           'size': set[i]['size'],
                           'additive': False}))
                           
            self.regions.append(
                ba.newnode('region',
                    attrs={'scale': tuple(set[i]['size']),
                           'type': 'box',
                           'materials': [self.collision,
                                         shared.footing_material]}))
            self.locs[-1].connectattr('position', self.regions[-1], 'position')

        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': ba.getmodel('tipTopBG'),
                'lighting': False,
                'background': True,
                'color_texture': ba.gettexture('black')})

        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)
        
%s
class MapMaker(ba.Plugin):
    def __init__(self) -> None:
        ba._map.register_map(MyMap)
    """ % (
           ' '.join(meta1), 
           ''.join(t1+t2+t3+t4+t5+t6),
           map_name, ''.join(blks), ' '.join(meta2))

def getlanguage(text, alm: str = ''):
    lang = _ba.app.lang.language
    translate = {
        "Cube":
            {"Spanish": "Bloque",
             "English": "Block",
             "Portuguese": "Bloco"},
        "Change Size":
            {"Spanish": "Tamaño reajustado",
             "English": "Size changed",
             "Portuguese": "Tamanho alterado"},
        "Save":
            {"Spanish": "Guardar",
             "English": "Save",
             "Portuguese": "Salvar"},
        "Error Msg Saved":
            {"Spanish": "Error: Faltan agregar más datos.",
             "English": "Error: Incomplete data",
             "Portuguese": "Erro: Ainda faltam dados"},
        "Msg Saved":
            {"Spanish": "¡Mapa guardado con éxito!",
             "English": "Your map was saved correctly!",
             "Portuguese": "Seu mapa foi salvo corretamente!"},
        "Msg Name":
            {"Spanish": "Nombre",
             "English": "Name",
             "Portuguese": "Nome"},
        "Action 1":
            {"Spanish": "Moldear bloque",
             "English": "Block molding",
             "Portuguese": "Bloco de moldagem"},
        "Action 2":
            {"Spanish": "Construir",
             "English": "Build map",
             "Portuguese": "Construir mapa"},
        "Action 3":
            {"Spanish": "Mover cámara",
             "English": "Free camera",
             "Portuguese": "Câmera livre"},
        "Action 4":
            {"Spanish": "Guardar mapa",
             "English": "Save map",
             "Portuguese": "Salvar mapa"},
        "Only in MMG":
            {"Spanish": "Sólo disponible en el Creador de Mapas",
             "English": "Only in Map-Maker",
             "Portuguese": "Solamente no Map-Maker"},
        "Game Name":
            {"Spanish": "Creador de Mapas",
             "English": "Map Maker",
             "Portuguese": "Map Maker"},
        "Color":
            {"Spanish": "Color",
             "English": "Color",
             "Portuguese": "Cor"},
        "Speed":
            {"Spanish": "Velocidad",
             "English": "Speed",
             "Portuguese": "Rapidez"},
        "File Exists Message":
            {"Spanish": "El nombre de este mapa ya está en uso.",
             "English": "Name in use, please enter another name.",
             "Portuguese": "Nome em uso, por favor, digite outro nome."},
        "Action 5":
            {"Spanish": "Importar mapa",
             "English": "Import data",
             "Portuguese": "Importar dados"},
        "Confirm Map Data":
            {"Spanish": "¿Deseas importar los datos\n de este mapa?",
             "English": "Are you sure to import\n the data from this map?",
             "Portuguese": "Você tem certeza de importar\n os dados deste mapa?"},
        "Imported Map Message":
            {"Spanish": "¡Mapa importado con éxito!",
             "English": "Map successfully imported!",
             "Portuguese": "Mapa importado com sucesso!"},
        "Creator":
            {"Spanish": "Mod creado por @PatrónModz",
             "English": "Mod created by @PatrónModz",
             "Portuguese": "Mod creado by @PatrónModz"},
        "Mod Info":
            {"Spanish": "¿Aburrido de siempre jugar los mismos mapas?\n ¡Ya no más! ahora con este increíble mod\n podrás crear y compartir tus propios mapas.",
             "English": "Bored of always playing the same maps?\n Not anymore! Now with this amazing mod\n you can create and share your own maps.",
             "Portuguese": "Aborrecido de jogar sempre os mesmos mapas?\n não mais! Agora com este incrível mod,\n você pode criar e compartilhar\n seus próprios mapas."},
        }
                
    languages = ['Spanish','Portuguese','English']
    if lang not in languages: lang = 'English'

    if text not in translate:
        return text
    return translate[text][lang]

def make(tag: str):
    global block_size
    data = []
    
    if tag == 'Cube':
        act = _ba.get_foreground_host_activity()
        with ba.Context(act):
            cursor_pos = act.cursor.position
            act._map.locs.append(
                ba.newnode('locator',
                    attrs={'shape': 'box',
                           'position': cursor_pos,
                           'color': block_color,
                           'opacity': 1.0,
                           'draw_beauty': True,
                           'size': block_size,
                           'additive': False}))
            cube = act._map.locs[-1]
            data = [cube.position, cube.color, cube.size]
        blocks.append(data)
        
    else:
        self = _ba.get_foreground_host_activity()

        if tag == 'FFA Spawn':
            with ba.Context(self):
                self.ffa_spawns.append(
                    ba.newnode('shield',
                        attrs={'color': (1, 1, 0),
                               'radius': 0.67,
                               'position': self.cursor.position}))
                data = self.ffa_spawns[-1].position
            ffa_spawns.append(data)
            
        elif tag == 'Powerup Spawn':
            with ba.Context(self):
                self.powerup_spawns.append(
                    ba.newnode('shield',
                        attrs={'color': (2, 0, 0),
                               'radius': 0.67,
                               'position': self.cursor.position}))
                data = self.powerup_spawns[-1].position
            powerup_spawns.append(data)
            
        elif tag == 'Team Spawn':
            if len(self.team_spawns) >= 2:
                return

            with ba.Context(self):
                self.team_spawns.append(
                    ba.newnode('shield',
                        attrs={'color': (0, 1, 1),
                               'radius': 0.67,
                               'position': self.cursor.position}))
                data = self.team_spawns[-1].position
            team_spawns.append(data)
            
        elif tag == 'TNT Spawn':
            if len(self.tnt_spawns) >= 4:
                return

            with ba.Context(self):
                self.tnt_spawns.append(
                    ba.newnode('shield',
                        attrs={'color': (2, 1, 0),
                               'radius': 0.67,
                               'position': self.cursor.position}))
                data = self.tnt_spawns[-1].position
            tnt_spawns.append(data)
            
        elif tag == 'Flag Default Spawn':
            global flag_default_spawn
            if flag_default_spawn is not None:
                return

            with ba.Context(self):
                self.flag_default_spawn = ba.newnode('shield',
                        attrs={'color': (2, 0, 2),
                               'radius': 0.67,
                               'position': self.cursor.position})
                data = self.flag_default_spawn.position
            flag_default_spawn = data
            
    return data

def update_position_cursor():
    a = ba.getactivity()
    p = tuple(round(s, 2) for s in a.cursor.position)
    pt = tuple(str(sn) for sn in p)
    t = "X: %s \n Z: %s \n Y: %s" % pt
    a._cursor_pos_text.text = t
    a.cursor.position = p

class CreationsMapPoints:
    # This file was automatically generated from "hockey_stadium.ma"
    # pylint: disable=all
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.0, 0.7956858119, 0.0) + (0.0, 0.0, 0.0) + (30.80223883, 0.5961646365, 13.88431707)
    points['ffa_spawn2'] = (0.0000000000, 0.0000000000, -0.0000000000)
    boxes['map_bounds'] = (0.0, 0.7956858119, -0.4689020853) + (0.0, 0.0, 0.0) + (35.16182389, 12.18696164, 21.52869693)
    
class CreationsMap(ba.Map):
    """Stadium map used for ice hockey games."""

    defs = CreationsMapPoints
    name = 'CreationsMap'

    @classmethod
    def get_play_types(cls) -> List[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'menuBG'

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {}
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.locs = []
        self.regions = []
        
        self.collision = ba.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        set = []

        for i, map in enumerate(set):
            self.locs.append(
                ba.newnode('locator',
                    attrs={'shape': 'box',
                           'position': set[i]['position'],
                           'color': set[i]['color'],
                           'opacity': 1.0,
                           'draw_beauty': True,
                           'size': set[i]['size'],
                           'additive': False}))
                           
            self.regions.append(
                ba.newnode('region',
                    attrs={'scale': tuple(set[i]['size']),
                           'type': 'box',
                           'materials': [self.collision,
                                         shared.footing_material]}))
            self.locs[-1].connectattr('position', self.regions[-1], 'position')
        
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': ba.getmodel('thePadBG'),
                'lighting': False,
                'background': True,
                'color_texture': ba.gettexture('menuBG')})
        
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.3, 1.3)
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        
############################


class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0

class MePlayerSpaz(PlayerSpaz):
    pass

class PlayerBall(PlayerSpaz):
    move_1 = 5
    
    def on_move_up_down(self, x) -> None:
        a = ba.getactivity()
        if not hasattr(a, 'cursor'):
            return

        pos = list(a.cursor.position)
        position = list(a.cursor.position)
        if x < 0:
            position[2] -= (x/100) * self.move_1
        elif x > 0:
            position[2] -= (x/100) * self.move_1
        a.cursor.position = tuple(position)
        update_position_cursor()
        
    def on_move_left_right(self, x) -> None:
        a = ba.getactivity()
        if not hasattr(a, 'cursor'):
            return

        pos = list(a.cursor.position)
        position = list(a.cursor.position)
        if x < 0:
            position[0] += (x/100) * self.move_1
        elif x > 0:
            position[0] += (x/100) * self.move_1
        a.cursor.position = tuple(position)
        update_position_cursor()
        
    def on_pickup_press(self) -> None:
        a = ba.getactivity()
        if not hasattr(a, 'cursor'):
            return

        position = list(a.cursor.position)
        position[1] += 0.3
        a.cursor.position = tuple(position)
        update_position_cursor()
        
    def on_jump_press(self) -> None:
        a = ba.getactivity()
        if not hasattr(a, 'cursor'):
            return

        position = list(a.cursor.position)
        position[1] -= 0.3
        a.cursor.position = tuple(position)
        update_position_cursor()
        
    def on_punch_press(self) -> None:
        global block_type
        if block_type == 'Cube':
            make(block_type)
            ba.playsound(ba.getsound('punch01'))
        
    def on_bomb_press(self) -> None:
        global blocks, block_type
        a = ba.getactivity()
        if len(blocks) > 0:
            blocks.pop()
            a._map.locs[-1].delete()
            a._map.locs.pop()
            ba.playsound(ba.getsound('shieldDown'))

class Ball(ba.Actor):
    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        _scale = 0.20

        self.no_collision = ba.Material()
        self.no_collision.add_actions(
            actions=(('modify_part_collision', 'collide', False)))

        self.node = ba.newnode('prop',
                               delegate=self,
                               attrs={
                                   'model': None,
                                   'color_texture': ba.gettexture('null'),
                                   'is_area_of_interest': True,
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [1.3],
                                   'materials': [self.no_collision]})
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            a = self._activity()
            assert a
            a.cursor.position = (0, 0, 0)
            

        elif isinstance(msg, ba.OutOfBoundsMessage):
            a = self._activity()
            assert a
            a.cursor.position = (0, 0, 0)
            
        
        else:
            super().handlemessage(msg)
        
# ba_meta export game
class MapMakerGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = getlanguage('Game Name')
    description = ''

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = []

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return issubclass(sessiontype, ba.FreeForAllSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        maps = ['CreationsMap']
        return maps

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._score_to_win: Optional[int] = None
        self._epic_mode = False
        
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.FORWARD_MARCH)

    def get_instance_description(self) -> Union[str, Sequence]:
        return ''

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return ''

    def on_team_join(self, team: Team) -> None:
        if self.has_begun():
            pass

    def spawn_player(self, player: Player) -> ba.Actor:
        playerspaz.PlayerSpaz = PlayerBall
        spaz = self.spawn_player_spaz(player)
        playerspaz.PlayerSpaz = MePlayerSpaz
        spaz.node.delete()
        #spaz.disconnect_controls_from_player()
        return spaz

    def on_begin(self) -> None:
        global blocks, block_size
        blocks = []
        block_size = [1.0, 1.0, 1.0]
        super().on_begin()
        
        self.ffa_spawns = []
        self.team_spawns = []
        self.powerup_spawns = []
        self.tnt_spawns = []
        self.flag_default_spawn = None

        self.aoib = ba.getactivity().globalsnode.area_of_interest_bounds
        
        self.cursor = ba.newnode('shield',
            attrs={'color': (5, 5, 5),
                   'radius': 0.67,
                   'position': CreationsMapPoints.points['ffa_spawn2']})
        self.ball = Ball().autoretain()
        self.cursor.connectattr('position', self.ball.node, 'position')
        
        self._ax_text = ba.newnode('text',
                    attrs={'in_world': False,
                          'text': getlanguage(block_type),
                          'scale': 1.5,
                          'color': (1,1,1),
                          'position': (450, 240),
                          'h_align': 'center'})
        
        self._cursor_pos_text = ba.newnode('text',
                    attrs={'in_world': False,
                          'text': '',
                          'scale': 1.5,
                          'color': (1,1,1),
                          'position': (-0, 270),
                          'h_align': 'center'})
        update_position_cursor()
        
        self._cursor_speed_text = ba.newnode('text',
                    attrs={'in_world': False,
                          'text': "%s x%s" % (getlanguage('Speed'), speed),
                          'scale': 1.5,
                          'color': (1,1,1),
                          'position': (0, -100*3),
                          'h_align': 'center'})
        _ba.set_party_icon_always_visible(True)
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PlayerDiedMessage):
            """
            super().handlemessage(msg)
            player = msg.getplayer(Player)
            #self.respawn_player(player)
            """
        else: return super().handlemessage(msg)

    def _standard_drop_powerup(self, index: int, expire: bool = True) -> None:
        return

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)

GLOBAL = {"Tab": 'Action 1'}

class MapMakerWindow(PopupWindow):
    def __init__(self, transition= 'in_right'):
        columns = 2
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.tab_buttons = {}
        self._old_maps = []
        
        self.tabdefs = {"Action 1": ['frameInset',(1,0,0.5)],
                        "Action 2": ['inventoryIcon',(1,1,1)],
                        "Action 3": ['achievementDualWielding',(1,1,1)],
                        "Action 4": ['file',(0.9,0.9,0.9)],
                        "Action 5": ['folder',(1.0,1.0,0.2)],
                        "About": ['heart', (0.9,0,0)]}
                        
        self.listdef = list(self.tabdefs)
        
        self.count = len(self.tabdefs) - 1
                        
        self._current_tab = GLOBAL['Tab']

        app = ba.app.ui
        uiscale = app.uiscale

        self._root_widget = ba.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5 if uiscale is ba.UIScale.SMALL else 1.0,
                           stack_offset=(0,-30) if uiscale is ba.UIScale.SMALL else  (0,0),
                           background=True)
        
        self._back_button = b = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(60,self._height-15),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=ba.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=ba.Call(self._back))
        ba.buttonwidget(edit=self._back_button, button_type='backSmall',size=(60, 60),label=ba.charstr(ba.SpecialChar.BACK))
        ba.containerwidget(edit=self._root_widget,cancel_button=b)
        
        self.titletext = ba.textwidget(parent=self._root_widget,position=(0, height-15),size=(width,50),
                          h_align="center",color=ba.app.ui.title_color, text='titletext', v_align="center",maxwidth=width*1.3)
        
        index = 0
        for tab in range(self.count):
            for tab2 in range(columns):
                
                tag = self.listdef[index]
                
                position = (620+(tab2*120),self._height-50*2.5-(tab*120))
                
                text = {'About':
                            ba.Lstr(resource='gatherWindow.aboutText')
                        }.get(tag, getlanguage(tag))
                
                self.tab_buttons[tag] = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                        position=position,size=(110, 110),
                                        scale=1,label='',enable_sound=False,
                                        button_type='square',on_activate_call=ba.Call(self._set_tab,tag,sound=True))
                                       
                self.text = ba.textwidget(parent=self._root_widget,
                            position=(position[0]+55,position[1]+30),
                            size=(0, 0),scale=1,color=ba.app.ui.title_color,
                            draw_controller=self.tab_buttons[tag],maxwidth=100,
                            text=text,h_align='center',v_align='center')
                                       
                self.image = ba.imagewidget(parent=self._root_widget,
                             size=(60,60),color=self.tabdefs[tag][1],
                             draw_controller=self.tab_buttons[tag],
                             position=(position[0]+25,position[1]+40),
                             texture=ba.gettexture(self.tabdefs[tag][0]))

                index += 1
        
                if index > self.count:
                    break
       
            if index > self.count:
                break
        
        self._make_sw  = lambda: ba.scrollwidget(
            parent=self._root_widget, position=(self._width*0.08,51*1.8),
            size=(self._sub_width -140,self._scroll_height +60*1.2),
            selection_loops_to_parent=True)
            
        self._scrollwidget = self._make_sw()
        self._tab_container = None
        self._set_tab(self._current_tab)
        ba.timer(0.1, ba.Call(self._in_game))

    def _set_tab(self, tab, sound: bool = False):
        if GLOBAL['Tab'] != tab:
            if self._scrollwidget:
                self._scrollwidget.delete()
                self._scrollwidget = self._make_sw()
            
        self.sound = sound
        GLOBAL['Tab'] = tab
        
        if tab != "About":
            text = getlanguage(tab)
        else: text = ba.Lstr(resource='gatherWindow.aboutText')
        ba.textwidget(edit=self.titletext, text=text)
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()

        if self.sound:
            ba.playsound(ba.getsound('click01'))

        if tab == 'Action 1':
            global blocks
            sub_height = 480
            v = sub_height - 55
            width = 300
            
            self.block_tn = []
            
            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
                
            for n, exe in enumerate(['X', 'Z', 'Y', 'Color']):
                max = 120.0
                ccolor = (0.15, 0.54, 0.89)
                
                ba.containerwidget(parent=c,position=(7.0, v-50-(max*n)),
                    color=ccolor,scale=1.3,size=(390, 70),background=True)

                t = ba.textwidget(parent=c,position=(-30, v-15-(max*n)),size=(width,50),
                    h_align="center",color=(0,1,0), text=getlanguage(exe), v_align="center",maxwidth=width*1.3)
                    
                if exe == 'Color':
                    b = ba.buttonwidget(parent=c,autoselect=True,
                            position=(405.0, v-15-(max*n)), size=(50, 50),
                            scale=1.0,label='',button_type='square', color=block_color,
                            on_activate_call=ba.Call(self._make_picker, 'block'))
                else:
                    self.block_tn.append(ba.textwidget(parent=c,position=(165, v-15-(max*n)),size=(width,50),
                        h_align="center",color=(1,1,0), text=str(block_size[n]), v_align="center",maxwidth=width*1.3))
                        
                    dipos = 0
                    for direc in ['+', '-']:
                        ba.buttonwidget(parent=c,autoselect=True,
                                    position=(405.0-(dipos), v-10-(n*max)), size=(100,100),
                                    repeat=True,scale=0.4,label=direc,button_type='square',text_scale=4,
                                    on_activate_call=ba.Call(self._mold_cube, direc, n))
                        dipos += 50

        elif tab == 'Action 2':
            GLOBAL['Tab'] = tab = 'Action 1'
            if not self.get_mapmaker():
                ba.screenmessage(getlanguage('Only in MMG'), (1,0,0))
                ba.playsound(ba.getsound('error'))
                self._set_tab(GLOBAL['Tab'])
            else:
                ba.containerwidget(edit=self._root_widget,transition='out_left')
                OnScreenControlsWindow()

        elif tab == 'Action 3':
            GLOBAL['Tab'] = 'Action 1'
            ba.containerwidget(edit=self._root_widget,transition='out_left')
            FreeCameraWindow()

        elif tab == 'Action 4':
            sub_height = 300
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            t = ba.textwidget(parent=c,position=(120, v-15),size=(width,50),
                    h_align="center",color=(0.0, 1.0, 0.0),maxwidth=width*1.3,
                    text=getlanguage('Msg Name'), v_align="center")
                
            self.text_map_name = ba.textwidget(parent=c,position=(120, v-60),size=(width,50), editable=True,
                    h_align="center",color=ba.app.ui.title_color, text=map_name, v_align="center",maxwidth=width*1.3)

            save = ba.buttonwidget(parent=c,autoselect=True,
                            position=(180.0, v-150), size=(150, 50),
                            scale=1.0,label=getlanguage('Save'), color=(0,0.4,1),
                            on_activate_call=ba.Call(self._save_map_as_plugin))

        elif tab == 'Action 5':
            a = _ba.get_foreground_host_activity()
            if not isinstance(a, MapMakerGame):
                GLOBAL['Tab'] = tab = 'Action 1'
                ba.screenmessage(getlanguage('Only in MMG'), (1,0,0))
                ba.playsound(ba.getsound('error'))
                self._set_tab(GLOBAL['Tab'])
                return

            self.old_maps()
            maps = self._old_maps
            
            sub_height = (70*len(maps))
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
            self.old_map_buttons = list()

            for n, mp in enumerate(maps):
                self.old_map_buttons.append(
                    ba.buttonwidget(parent=c,position=(120, v-10-(70*n)),size=(width,50),
                        label=mp.__name__+' @ '+mp.map_name, autoselect=True,
                        on_activate_call=ba.Call(self.load_map_data, n)
                    ))

        else:
            sub_height = 0
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = ba.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            t = ba.textwidget(parent=c,position=(110, v-20),size=(width,50),
                      scale=1.4,color=(1.2,0.2,0.2),h_align="center",v_align="center",
                      text="Map Maker",maxwidth=width*30)

            t = ba.textwidget(parent=c,position=(110, v-90),size=(width,50),
                      scale=1,color=(1.3,0.5,1.0),h_align="center",v_align="center",
                      text=getlanguage('Creator'),maxwidth=width*30)

            t = ba.textwidget(parent=c,position=(110, v-180),size=(width,50),
                      scale=1,color=(1.0,1.2,0.3),h_align="center",v_align="center",
                      text=getlanguage('Mod Info'),maxwidth=width*30)

        for select_tab,button_tab in self.tab_buttons.items():
            if select_tab == tab:
                ba.buttonwidget(edit=button_tab,color=(0.5,0.4,1.5))
            else: ba.buttonwidget(edit=button_tab,color=(0.52,0.48,0.63))

    def _save_map_as_plugin(self):
        a =_ba.get_foreground_host_activity()
        if not isinstance(a, MapMakerGame):
            ba.screenmessage(getlanguage('Only in MMG'), (1,0,0))
            ba.playsound(ba.getsound('error'))
            return
        
        global map_name
        map_name = ba.textwidget(query=self.text_map_name)

        if not len(ffa_spawns) > 0 or len(team_spawns) != 2 or flag_default_spawn is None:
            ba.screenmessage(getlanguage('Error Msg Saved'), (1,0,0))
            ba.playsound(ba.getsound('error'))
            return 
        
        d = ba.app.python_directory_user
        fl = f'{d}/{map_name}.py'
        if os.path.exists(fl):
            ba.screenmessage(getlanguage('File Exists Message'), (1,0,0))
            ba.playsound(ba.getsound('error'))
            return
            
        with open(fl, 'w') as x:
            plugin = save_map_as_plugin()
            x.write(plugin)
        
        self.save_map_data()
        ba.screenmessage(map_name+' @ '+getlanguage('Msg Saved'), (0,1,0))
        ba.playsound(ba.getsound('ding'))

    def _mold_cube(self, val: str, num: int):
        global block_size
        if val == '+':
            block_size[num] = round(block_size[num]+0.5, 2)
        else: block_size[num] = round(block_size[num]-0.5, 2)
        block_size[num] = max(block_size[num], 0.5)
        ba.textwidget(edit=self.block_tn[num], text=str(block_size[num]))

    def save_map_data(self):
        n = int(1)
        while n:
            fd = Folder+'map'+str(n)+'.py'
            if not os.path.exists(fd):
                with open(fd, 'w') as c:
                    blks = str([b for b in blocks]).replace('[(', '\n    [(')
                    data = [
                    "all = globals()",
                    f"map_name = '{map_name}'",
                    f"ffa_spawns = {ffa_spawns}",
                    f"team_spawns = {team_spawns}",
                    f"powerup_spawns = {powerup_spawns}",
                    f"tnt_spawns = {tnt_spawns}",
                    f"flag_default_spawn = {flag_default_spawn}",
                    f"blocks = {blks}"]
                    c.write('\n'.join(data))
                break
            else:
                n += 1

    def old_maps(self):
        self._old_maps.clear()
        
        def add_map(m):
            self._old_maps.append(m)
            
        n = int(1)
        while n:
            fd = Folder+'map'+str(n)+'.py'
            if os.path.exists(fd):
                exec(f"from MyMaps import map{n} as Mp")
                exec("add_map(Mp)")
                n += 1
            else: break
        
    def load_map_data(self, id: int):
        def call():
            a = _ba.get_foreground_host_activity()
            map = self._old_maps[id]
            data = dict(list(map.all.items())[10:])
    
            for attr, obj in data.items():
                if attr == 'blocks':
                    _attrs = ['block_color', 'block_size']
                    for x in obj:
                        x[2] = list(x[2])
                        globals()[_attrs[0]] = x[1]
                        globals()[_attrs[1]] = x[2]
                        
                        with ba.Context(a):
                            a.cursor.position = x[0]
                            make('Cube')

            ba.screenmessage(getlanguage('Imported Map Message'), (0,1,0))
            ba.playsound(ba.getsound('gunCocking'))
            self._set_tab('Action 2')
        
        ConfirmWindow(getlanguage('Confirm Map Data'),
            height=100*1.5,cancel_button=True,width=200,
            action=call,ok_text=ba.Lstr(resource='okText'))
        
    def _actions(self, type: int):
        global block_type
        if type == 0:
            block_type = 'Cube'
        elif type == 1:
            block_type = 'FFA Spawn'

        act = _ba.get_foreground_host_activity()
        with ba.Context(act):
            act._ax_text.text = getlanguage(block_type)
            ba.playsound(ba.getsound('deek'))

    def _in_game(self):
        try:
            act = _ba.get_foreground_host_activity()
        except Exception as e:
            act = None

        if act is None:
            r = 'getTicketsWindow.unavailableTemporarilyText'
            ba.playsound(ba.getsound('error'))
            ba.screenmessage(ba.Lstr(resource=r), color=(1, 0, 0))
            self._back()

    def get_mapmaker(self):
        a = _ba.get_foreground_host_activity()
        return isinstance(a, MapMakerGame)

    # Color Picker
    def _make_picker(self, tag: Any):
        ColorPicker(
            parent=self._root_widget, position=(0,0),
            delegate=self, tag=tag, initial_color=block_color)

    def color_picker_closing(self, picker):
        self._set_tab(GLOBAL['Tab'])

    def color_picker_selected_color(self, picker, color):
        global block_color
        block_color = tuple(round(c, 2) for c in color)
        self._set_tab(GLOBAL['Tab'])
    
    def _back(self):
        pass

class OnScreenControlsWindow(PopupWindow):
    def __init__(self, transition= 'in_right'):
        columns = 2
        self._width = width = 1200
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.buttons = []

        app = ba.app.ui
        uiscale = app.uiscale

        self._root_widget = ba.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5, background=False,
                           stack_offset=(0,-30) if uiscale is ba.UIScale.SMALL else  (0,0))
        
        self._back_button = b = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(200,self._height-90),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=ba.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=ba.Call(self._back))
        ba.buttonwidget(edit=self._back_button, button_type='backSmall',size=(60, 60),label=ba.charstr(ba.SpecialChar.BACK))
        ba.containerwidget(edit=self._root_widget,cancel_button=b)
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280, self._height-170),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'u')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280, self._height-300),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'd')))
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(210.5, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'l')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(352.55, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'r')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(200*4.75, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'z+')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(200*4.75, self._height-235*1.3),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'z-')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,
                   position=(352.55*2.3, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=getlanguage('+'), enable_sound=False,
                   button_type='square', on_activate_call=ba.Call(self._actions, 'add')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,
                   position=(352.55*2.3, self._height-235*1.30),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=getlanguage('='), enable_sound=False,
                   button_type='square', on_activate_call=ba.Call(self._actions, '=')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,
                   position=(352.55*2.9, self._height-235*0.45),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DELETE), enable_sound=False,
                   button_type='square', on_activate_call=ba.Call(self._actions, 'del')))
        
        str_choices = all_block_types
        lstr_choices = [ba.Lstr(value=getlanguage(x)) for x in str_choices]
        
        _popupmenu0 = PopupMenu(parent=self._root_widget,
                    position=(352.55*2.35, self._height-235*0.68),
                    width=90,scale=2.4,
                    choices=str_choices,
                    current_choice=block_type,
                    choices_display=lstr_choices,
                    on_value_change_call=ba.Call(self._block_type))
        self.reanude()

    def _block_type(self, x: str):
        global block_type
        block_type = x
        
        act = _ba.get_foreground_host_activity()
        with ba.Context(act):
            act._ax_text.text = getlanguage(block_type)
            ba.playsound(ba.getsound('deek'))
        
    def _actions(self, val: str = 'none'):
        global blocks, block_type, ffa_spawns, flag_default_spawn
        a = _ba.get_foreground_host_activity()
        
        if val == 'add':
            make(block_type)
            ba.playsound(ba.getsound('punch01'))
            
        elif val == '=':
            if len(blocks) > 0 and block_type == 'Cube':
                with ba.Context(a):
                    pos = blocks[-1][0]
                    a.cursor.position = pos
            
        elif val == 'del':
            if block_type == 'Cube':
                if len(blocks) > 0:
                    blocks.pop()
                    
                    with ba.Context(a):
                        a._map.locs[-1].delete()
                        a._map.locs.pop()
                    
            elif block_type == 'FFA Spawn':
                if len(ffa_spawns) > 0:
                    ffa_spawns.pop()
                    
                    with ba.Context(a):
                        a.ffa_spawns[-1].delete()
                        a.ffa_spawns.pop()
                        
            elif block_type == 'Powerup Spawn':
                if len(powerup_spawns) > 0:
                    powerup_spawns.pop()
                    
                    with ba.Context(a):
                        a.powerup_spawns[-1].delete()
                        a.powerup_spawns.pop()
                        
            elif block_type == 'Team Spawn':
                if len(team_spawns) > 0:
                    team_spawns.pop()
                    
                    with ba.Context(a):
                        a.team_spawns[-1].delete()
                        a.team_spawns.pop()
                    
            elif block_type == 'TNT Spawn':
                if len(tnt_spawns) > 0:
                    tnt_spawns.pop()
                    
                    with ba.Context(a):
                        a.tnt_spawns[-1].delete()
                        a.tnt_spawns.pop()
                    
            elif block_type == 'Flag Default Spawn':
                if flag_default_spawn is not None:
                    flag_default_spawn = None
                    
                    with ba.Context(a):
                        if hasattr(a.flag_default_spawn, 'delete'):
                            a.flag_default_spawn.delete()
                        a.flag_default_spawn = None
                    
            ba.playsound(ba.getsound('shieldDown'))
        self.update_position_cursor()

    def _move(self, val: str = 'none'):
        pos = [0.0, 0.0, 0.0]
        if val == 'u':
            pos[2] = -speed
        elif val == 'd':
            pos[2] = speed
        elif val == 'l':
            pos[0] = -speed
        elif val == 'r':
            pos[0] = speed
        elif val == 'z-':
            pos[1] = -speed
        elif val == 'z+':
            pos[1] = speed
            
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            p = list(a.cursor.position)
            a.cursor.position = (p[0]+pos[0], p[1]+pos[1], p[2]+pos[2])
        self.update_position_cursor()

    def reanude(self):
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            a.globalsnode.paused = False

    def update_position_cursor(self):
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            update_position_cursor()
            
    def _back(self):
        ba.containerwidget(edit=self._root_widget,transition='out_right')
        MapMakerWindow()

class FreeCameraWindow(PopupWindow):
    def __init__(self, transition= 'in_right'):
        columns = 2
        self._width = width = 1200
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.buttons = []

        app = ba.app.ui
        uiscale = app.uiscale

        self._root_widget = ba.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5, background=False,
                           stack_offset=(0,-30) if uiscale is ba.UIScale.SMALL else  (0,0))
        
        self._back_button = b = ba.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(200,self._height-90),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=ba.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=ba.Call(self._back))
        ba.buttonwidget(edit=self._back_button, button_type='backSmall',size=(60, 60),label=ba.charstr(ba.SpecialChar.BACK))
        ba.containerwidget(edit=self._root_widget,cancel_button=b)
        
        _x = 0.0
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-170),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'u')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-300),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'd')))
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(210.5+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'l')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(352.55+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'r')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*4.75+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'z+')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*4.75+_x, self._height-235*1.3),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'z-')))

        _x += 650
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-170),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'ar')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(280+_x, self._height-300),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'ab')))
        
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(210.5+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'iz')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(352.55+_x, self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'de')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*7.5+(_x-_x), self._height-235),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.UP_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'w+')))
                   
        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,enable_sound=False,
                   position=(100*7.5+(_x-_x), self._height-235*1.3),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                   button_type='square', on_activate_call=ba.Call(self._move, 'w-')))

        self.buttons.append(
            ba.buttonwidget(parent=self._root_widget,autoselect=True,
                   position=(352.55*2.9, self._height-235*0.45),size=(80, 80), repeat=True,
                   scale=0.8,text_scale=1.2, label='*', enable_sound=False,
                   button_type='square', on_activate_call=ba.Call(self._move, '*')))

        self.save_camera_pos()

    def _move(self, val: str = 'none'):
        pos = [0.0, 0.0, 0.0] + [0.0, 0.0, 0.0]
        max = 5.0
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

        elif val == 'ar':
            pos[5] = -max
        elif val == 'ab':
            pos[5] = max
        elif val == 'iz':
            pos[3] = -max
        elif val == 'de':
            pos[3] = max
        elif val == 'w-':
            pos[4] = -max
        elif val == 'w+':
            pos[4] = max
        
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            p = list(a.globalsnode.area_of_interest_bounds)
            if val == '*':
                global original_camera_position
                name = str(type(a))
                aoib = original_camera_position[name]
                a.globalsnode.area_of_interest_bounds = aoib
            else:
                a.globalsnode.area_of_interest_bounds = (
                    p[0]+pos[3], p[1]+pos[4], p[2]+pos[5],
                    p[3]+pos[0], p[4]+pos[1], p[5]+pos[2])

    def save_camera_pos(self):
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            name = str(type(a))
            if name not in original_camera_position:
                pos = a.globalsnode.area_of_interest_bounds
                original_camera_position[name] = pos
                
    def reanude(self):
        a = _ba.get_foreground_host_activity()
        with ba.Context(a):
            a.globalsnode.paused = False

    def _back(self):
        ba.containerwidget(edit=self._root_widget,transition='out_right')
        MapMakerWindow()

def command(val: str, *args):
    global block_size
    calls[0](val, *args)

    try:
        a = _ba.get_foreground_host_activity()
        if not isinstance(a, MapMakerGame):
            return

        if val == 'c':
            a = _ba.get_foreground_host_activity()
            with ba.Context(a):
                cm = a.globalsnode.camera_mode
                if cm == 'rotate':
                    a.globalsnode.camera_mode = 'follow'
                else: a.globalsnode.camera_mode = 'rotate'
        elif val == 'e':
            def _back(self):
                self._root_widget.delete()
                
            mmw = MapMakerWindow
            mmw._back = _back
            with ba.Context('ui'):
                mmw()
        else:
            if val[0] == 'x':
                global speed
                x = val
                val = val.replace('x', '')
                speed = max(float(val), 0.5)
                a = _ba.get_foreground_host_activity()
                with ba.Context(a):
                    a._cursor_speed_text.text = "%s x%s" % (getlanguage('Speed'), speed)
                ba.screenmessage("%s %s" % (getlanguage('Speed'), x))
                return

            msg = val.split(' ')
            if len(msg) == 3:
                block_size = [max(float(n), 0.5) for n in msg]
                ba.screenmessage(getlanguage('Change Size'))
                
    except Exception as e:
        pass

def add_plugin():
    try: from baBearModz import BearPlugin
    except Exception as e:
        return ba.timer(2.5, lambda e=e:
               ba.screenmessage('Error plugin: ' + str(e), (1,0,0)))
               
    BearPlugin(icon='multiplayerExamples',
               creator='@PatrónModz',
               button_color=(0.25, 1.05, 0.05),
               plugin=MapMaker,
               window=MapMakerWindow)

def make_folder():
    r = _ba.app.python_directory_user
    folder = r + '/MyMaps'
    if not os.path.exists(folder):
        os.mkdir(folder)

    globals()['Folder'] = folder + '/'

# ba_meta export plugin
class MapMaker(ba.Plugin):
    def __init__(self) -> None:
        ba._map.register_map(CreationsMap)
        add_plugin()
        make_folder()
        
        if calls[0] is None:
            calls[0] = _ba.chatmessage
        _ba.chatmessage = command