# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui

import random,time,datetime,weakref,json,os
from bauiv1lib.colorpicker import ColorPicker
from bauiv1lib.confirm import ConfirmWindow
from bauiv1lib.popup import PopupWindow, PopupMenu
from bascenev1lib.actor import playerspaz as ps
from bascenev1lib.actor import powerupbox as pb

GLOBAL = {"Tab": 'Action 1',
          "Players": dict(),
          "ETxt": ['', '']}
          
apg = bs.app.config
          
def getlanguage(text, alm: list = []):
    if not any(alm):
        alm = [a for a in range(62)]
    lang = bs.app.lang.language
    setphrases = {"Action 1":
                      {"Spanish": "Crear roles",
                       "English": "Make roles",
                       "Portuguese": "Criar roles"},
                  "Color":
                      {"Spanish": "Color",
                       "English": "Color",
                       "Portuguese": "Cor"},
                  "Save":
                      {"Spanish": "Guardar",
                       "English": "Save",
                       "Portuguese": "Salvar"},
                  "Empty Text":
                      {"Spanish": "Aún falta agregar más datos",
                       "English": "More data is still missing",
                       "Portuguese": "Ainda faltam mais dados"},
                  "Double Role":
                      {"Spanish": "Role ya agregado",
                       "English": "This role already exists",
                       "Portuguese": "Este role já existe"},
                  "Updated Role":
                      {"Spanish": "¡Role actualizado!",
                       "English": "Updated Role!",
                       "Portuguese": "Role atualizado!"},
                  "Action 2":
                      {"Spanish": "Añadir role",
                       "English": "Add role",
                       "Portuguese": "Adicionar role"},
                  "No Players":
                      {"Spanish": "No hay jugadores",
                       "English": "No Players",
                       "Portuguese": "Não há jogadores"},
                  "Add":
                      {"Spanish": "Añadir",
                       "English": "Add",
                       "Portuguese": "Adicionar"},
                  "Obj":
                      {"Spanish": "Objeto",
                       "English": "Object",
                       "Portuguese": "Objeto"},
                  "...":
                      {"Spanish": "Ninguno",
                       "English": "None",
                       "Portuguese": "Nenhum"},
                  "Floating Friend":
                      {"Spanish": "Amigo flotante",
                       "English": "Floating Friend",
                       "Portuguese": "Amigo Flutuante"},
                  "Registered Player":
                      {"Spanish": "Cuenta ya registrado",
                       "English": "Registered account",
                       "Portuguese": "Jogador já registrado"},
                  "Change Notice":
                      {"Spanish": "No podrás recuperar los cambios.\n ¿Estás seguro?",
                       "English": "This cannot be undone.\n Are you sure?",
                       "Portuguese": "Isso não pode ser desfeito.\n Tem certeza?"},
                  "Info Player":
                      {"Spanish": f"Cuenta: {alm[0]}\n Nombre: {alm[1]}\n Pb: {alm[2]}",
                       "English": f"Account: {alm[0]}\n Name: {alm[1]}\n Pb: {alm[2]}",
                       "Portuguese": f"Conta: {alm[0]} Nome: {alm[1]}\n Pb: {alm[2]}"},
                  "Creator":
                      {"Spanish": "Mod creado por @PatrónModz",
                       "English": "Mod created by @PatrónModz",
                       "Portuguese": "Mod creado by @PatrónModz"},
                  "Mod Info":
                      {"Spanish": f"Crea roles, añade accesorios...\n ¡Y mucho más!",
                       "English": f"Create roles, add accessories\n and much more!",
                       "Portuguese": f"Criar roles, adicionar acessórios\n e muito mais!"},
                  }
    language = ["Spanish", "English", "Portuguese"]
    if lang not in language:
        lang = "English"
        
    if text not in setphrases:
        return text
    return setphrases[text][lang]
    
def tag(self,
        text: str = '',
        pos: Sequence[float] = (0.0, 1.05, 0.0)):
        m = bs.newnode('math',owner=self.node,attrs={'input1': pos,'operation': 'add'})
        self.node.connectattr('position_center', m, 'input2')
        _text = bs.newnode('text',owner=self.node,
                attrs={'in_world': True,
                      'text': text,
                      'scale': 0.02,
                      'shadow': 0.5,
                      'flatness': 1.0,
                      'color':(1,1,1),
                      'h_align': 'center'}) 
        m.connectattr('output', _text, 'position')
        bs.animate(_text, 'scale', {0: 0.017,0.4: 0.017, 0.5: 0.011})
        return _text

class Settings:
    dir: str = bs.app.python_directory_user
    dir2: str = (dir + '/Configs')
    dir3: str = (dir2 + '/Roles.json')
    config: dict = None

    def __init__(self) -> None:
        self.file_exists()
        self._save()

    def _save(self):
        if self.config is None:
            with open(self.dir3, 'r') as f:
                self.config = json.loads(f.read())

        if isinstance(self.config, dict):
            if not self.file_exists():
                return False

            with open(self.dir3, 'w') as f:
                dumps = json.dumps(self.config, indent=4)
                f.write(dumps)
              
            with open(self.dir3, 'r') as f:
                self.config = json.loads(f.read())
               
    def file_exists(self):
        if not os.path.exists(self.dir2):
            os.mkdir(self.dir2)
        if not os.path.exists(self.dir3):
            with open(self.dir3, 'w') as f:
                f.write('{}')
        return os.path.exists(self.dir3)
   
   
    def edit_tag_from_chat(self, msg: str) -> None:
        error = lambda: bs.getsound('error').play()
        
        a1 = msg.split(' ')[0]
        if a1 != 'e.role':
            return

        a2 = msg.replace(a1, '').strip()
        args = a2.split(' ')
        
        if len(args) > 1:
            for role in self.config:
                if role in a2:
                    a3 = a2.replace(role, '').strip()
                    self.config[role]['Tag'] = a3
                    self._save()
                    bs.screenmessage(getlanguage('Updated Role'), (0,1,0))
                    bs.getsound('dingSmall').play()
                    break
            else: error()
        else: error()
   
stg = Settings()

class LittlePet(bs.Actor):
    def __init__(self,
                 node: bs.Node = None,
                 item: str = 'item1',
                 obey_position: bool = False,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        
        self.kwargs = dict(
            node=node,
            item=item,
            obey_position=True,
            position=position)
            
        self.owner = node
        self.multitex = []
        
        self.no_collision = bs.Material()
        self.no_collision.add_actions(
            actions=(('modify_part_collision', 'collide', False)))
                
        pfac = pb.PowerupBoxFactory.get()
        mesh = bs.getmesh('aliHead')
        tex = bs.gettexture('aliColor')
        
        mats = [self.no_collision,
                pfac.powerup_material]
        
        mesh, tex = {"item1":
                          (bs.getmesh('aliHead'),
                           bs.gettexture('aliColor')),
                      "item2":
                          (bs.getmesh('impactBomb'),
                           [bs.gettexture('impactBombColor'),
                            bs.gettexture('impactBombColorLit')]),
                      "item3":
                          (bs.getmesh('frostyHead'),
                           bs.gettexture('frostyColor')),
                      "item4":
                          (bs.getmesh('shield'),
                           [bs.gettexture('powerupIceBombs'),
                            bs.gettexture('aliColorMask')]),
                      "item5":
                          (bs.getmesh('puck'),
                           bs.gettexture('puckColor')),
                      "item6":
                          (bs.getmesh('egg'),
                           bs.gettexture('eggTex1')),
                      "item7":
                          (bs.getmesh('powerup'),
                           list({bs.gettexture(i.split('.')[0] if 'power' in i
                                else 'powerupCurse') for i in
                                os.listdir('ba_data/textures/')})),
                      "item8":
                          (bs.getmesh('landMine'),
                           [bs.gettexture('landMine'),
                            bs.gettexture('landMineLit')]),
                      "item9":
                          (bs.getmesh('bombSticky'),
                           bs.gettexture('bombStickyColor')),
                      "item10":
                          (bs.getmesh('shrapnelSlime'),
                           [bs.gettexture('cyborgColor'),
                            bs.gettexture('bunnyColor')]),
                      }.get(item,
                           (bs.getmesh('aliHead'),
                            bs.gettexture('aliColor')))
        
        scale = {"item4": 0.15,
                 "item5": 0.5,
                 "item6": 0.4,
                 "item2": 0.7,
                 "item7": 0.6,
                 "item10": 0.2,
                }.get(item, 0.8)
        
        body = {"item5": 'puck',
                "item6": 'puck',
               }.get(item, 'box')
               
        type = {"item9": 'bomb',
               }.get(item, 'prop')
        
        ref, refs = {"item2": ('powerup', 1.0),
                     "item4": ('powerup', 1.0),
                     "item8": ('powerup', 1.0),
                     "item9": ('sharper', 1.8),
                    }.get(item, ('soft', 0.2))
        
        if isinstance(tex, list):
            self.multitex = [t for t in tex]
            tex = tex[0]
        
        if not obey_position:
            position = (position[0], position[1]+7.5, position[2])
        
        self.node = bs.newnode(
                type, owner=node,
                delegate=self,
                attrs={'body': body,
                       'position': position,
                       'mesh': mesh,
                       'color_texture': tex,
                       'reflection': ref,
                       'mesh_scale': scale,
                       'shadow_size': 0.2,
                       'reflection_scale': [refs],
                       'materials': mats})
        self._move()

        if type == 'bomb':
            self.node.fuse_length = 0.5

        if any(self.multitex):
            self.changing_textures()

    def changing_textures(self):
        self.texture_sequence = bs.newnode('texture_sequence',
            owner=self.node,attrs={
                'rate': 100, 'input_textures': self.multitex})
        self.texture_sequence.connectattr(
            'output_texture', self.node, 'color_texture')

    def _move(self):
        t = 0.1
        self.pos_timer = bs.Timer(
            t, bs.WeakCall(self.update_pos, t), repeat=True)

    def update_pos(self, t: float):
        if not self.node.exists():
            self.pos_timer = None
            return
            
        calls = []
        def vel(t):
            if not self.node.exists():
                self.pos_timer = None
                return
            
            t = max(t, 0)
            n = list(self.node.velocity)
            p = list(self.owner.velocity)

            bs.animate_array(self.node, 'velocity', 3, {0: n, t: p})
            
            bs.timer(0.3, lambda: calls[1](t, [random.random()*1.5,
                         random.choice([0.8, 0.9, 1.0, 0.5]), random.choice([0.3])
                ]))
        calls.append(vel)

        def pos(t, l):
            if not self.node.exists():
                self.pos_timer = None
                return
            
            n = list(self.node.position)
            p = list(self.owner.position)
            p[1] += l[0]
            
            p[0] = p[0]+l[1] if p[0] < 0 else p[0]-l[1]
            
            t = max(t+l[2], 0)
            bs.animate_array(self.node, 'position', 3, {0: n, t: p})
        calls.append(pos)
        bs.timer(0.0, lambda: calls[0](t*2))

    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
                
                if self.owner.exists():
                    actor = self.owner.getdelegate(object)
                    if not actor._dead:
                        self.kwargs['position'] = self.owner.position
                        self.__class__(**self.kwargs).autoretain()
                
        return super().handlemessage(msg)

class NewPlayerSpaz(ps.PlayerSpaz):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_player_info_and_add_role()

    def save_player_info_and_add_role(self):
        self._role = None
        access = False
        s_player = self._player._sessionplayer
        i_player = s_player.inputdevice
        
        pb = s_player.get_v1_account_id()
        name = s_player.getname(True)
        account = i_player.get_v1_account_name(True)
        
        if account:
            GLOBAL['Players'][account] = [name, pb]
        else: return

        pos = (0.0, 1.05, 0.0)
        if ('SandA Settings') in apg:
            cfg = apg['SandA Settings']
            if cfg['Shield Name'] or cfg['Actor Name']:
                pos = (0.0, 1.35, 0.0)

        for data in stg.config.values():
            if account in data['Ids']:
                access = True
                break
            else:
                for id in data['Ids'].values():
                    if id['Pb'] is pb:
                        access = True
                        break
                else: access = False

        if access:
            self._role = tag(self, text=data['Tag'], pos=pos)
            array = {0.4*i: c for i, c in enumerate(data['Colors'])}
            bs.animate_array(self._role, 'color', 3, array, True)
            if data['Obj'] != '...':
                self.add_pet(data['Obj'])

    def add_pet(self, obj: str):
        LittlePet(item=obj, node=self.node,
                  position=self.node.position).autoretain()

#### WINDOWS ####
class TagWindow(PopupWindow):
    def __init__(self, transition= 'in_right'):
        columns = 2
        self._width = width = 800
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self.tab_buttons = {}
        
        self.tabdefs = {"Action 1": ['inventoryIcon', (1,1,1)],
                        "Action 2": ['star', (1,0,0.5)],
                        "About": ['heart', (0.9,0,0)]}
                        
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
                
                text = {'About':
                            bui.Lstr(resource='gatherWindow.aboutText')
                        }.get(tag, getlanguage(tag))
                
                position = (620+(tab2*120),self._height-50*2.5-(tab*120))

                self.tab_buttons[tag] = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                        position=position,size=(110,110),
                                        scale=1,label='',enable_sound=False,
                                        button_type='square',on_activate_call=bui.Call(self._set_tab,tag,sound=True))
                                       
                self.text = bui.textwidget(parent=self._root_widget,
                            position=(position[0]+55,position[1]+30),
                            size=(0, 0),scale=1,color=bui.app.ui_v1.title_color,
                            draw_controller=self.tab_buttons[tag],maxwidth=100,
                            text=text,h_align='center',v_align='center')
                                       
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
        
        self._make_sw  = lambda: bui.scrollwidget(
            parent=self._root_widget, position=(self._width*0.08,51*1.8),
            size=(self._sub_width -140,self._scroll_height +60*1.2),
            selection_loops_to_parent=True)
            
        self._scrollwidget = self._make_sw()
        self._tab_container = None
        self._set_tab(self._current_tab)

    def _set_tab(self, tab, sound: bool = False):
        if GLOBAL['Tab'] != tab:
            if self._scrollwidget:
                self._scrollwidget.delete()
                self._scrollwidget = self._make_sw()
            
        self.sound = sound
        GLOBAL['Tab'] = tab
        
        if tab != "About":
            text = getlanguage(tab)
        else: text = bui.Lstr(resource='gatherWindow.aboutText')
        
        bui.textwidget(edit=self.titletext,text=text)
        
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()

        if self.sound:
            bui.getsound('click01').play()

        if tab == 'Action 1':
            sub_height = 460
            v = sub_height - 90
            width = 300
            
            self._popupmenu = None
            self._role_colors = []
            self._friend = '...'
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)
            
            t1 = bui.textwidget(parent=c,position=(-60, v),size=(width,50),
                text='Role:',color=bui.app.ui_v1.title_color,h_align="center", v_align="center",maxwidth=width*1.3)
            
            self.t_edit1 = bui.textwidget(parent=c,position=(160, v),size=(width,50),editable=True,max_chars=15,
                description='Role', text=GLOBAL['ETxt'][0],color=bui.app.ui_v1.title_color,h_align="center", v_align="center",maxwidth=width*1.3)
            
            v -= 90
            t2 = bui.textwidget(parent=c,position=(-60, v),size=(width,50),
                text='Tag:',color=bui.app.ui_v1.title_color,h_align="center", v_align="center",maxwidth=width*1.3)
            
            self.t_edit2 = bui.textwidget(parent=c,position=(160, v),size=(width,50),editable=True,max_chars=20,
                description='Tag', text=GLOBAL['ETxt'][1],color=bui.app.ui_v1.title_color,h_align="center", v_align="center",maxwidth=width*1.3)
            v -= 90
            
            t4 = bui.textwidget(parent=c,position=(-20, v+15),size=(width,50),
                text=getlanguage('Floating Friend')+':',color=bui.app.ui_v1.title_color,h_align="center", v_align="center",maxwidth=width*1.3)
            
            str_choices = ['...'] + ['item'+str(i+1) for i in range(10)]
            lstr_choices = [bui.Lstr(value=getlanguage('...'))] + [
                bui.Lstr(value=getlanguage('Obj')+f' {s+1}') for s in range(10)]
            
            self._popupmenu4 = PopupMenu(parent=c,
                    position=(312, v+15),width=90,scale=2.4,
                    choices=str_choices,
                    choices_display=lstr_choices,
                    on_value_change_call=bui.Call(self.select_friend))

            self.c_button = bui.buttonwidget(parent=c,position=(100*3.9,v-80),size=(40,40),label='', button_type='square',
                color=(1.0, 1.0, 1.0),scale=1.3,autoselect=True,on_activate_call=bui.Call(self._make_picker, 'roles'))
            
            t3 = bui.textwidget(parent=c,position=(100*1.6,v-80),size=(width,50),v_align="center",
                text=getlanguage('Color')+':',color=bui.app.ui_v1.title_color,h_align="center", maxwidth=width*1.3)
            
            save_button = bui.buttonwidget(parent=c,position=(100*1.7,v-180),size=(110, 40),label=getlanguage('Save'),
                color=(0.2, 1.2, 0.5),scale=1.3,autoselect=True,on_activate_call=bui.Call(self._save_role))
            self._data = [c, v]

        elif tab == 'Action 2':
            accounts = list(n for n in GLOBAL['Players'].keys())
            sub_height = (len(stg.config) * 130)
            
            if not any(accounts):
                sub_height = 0
            
            v = sub_height - 45
            width = 300
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            if not any(accounts):
                t2 = bui.textwidget(parent=c,position=(100, v-140),size=(width,50),
                    text=getlanguage('No Players'),color=bui.app.ui_v1.title_color,h_align="center",
                    v_align="center",maxwidth=width*1.3)
            else:
                if any(stg.config):
                    for i, role in enumerate(stg.config):
                        bui.containerwidget(parent=c,position=(30, v-70),
                            color=(0.8, 0.0, 1.3),scale=1.3,size=(360, 80),background=True)
                            
                        t2 = bui.textwidget(parent=c,position=(30, v-15),size=(width,50),
                            text=f'Role: {role}',color=(0,1.3,0),h_align="center",
                            v_align="center",maxwidth=width*1.3)
                            
                        b1 = bui.buttonwidget(parent=c,position=(100,v-60),
                            label=bui.Lstr(resource='deleteText'),
                            color=(0.2, 0.6, 1.0),size=(80, 25),
                            scale=1.3,autoselect=True,on_activate_call=bui.Call(self.delete_role, role))
                            
                        str_choices = list(accounts)
                        lstr_choices = [bui.Lstr(value=s) for s in str_choices]
                        self._popupmenu2 = PopupMenu(
                            parent=c,width=90,scale=2.4,
                            position=(230, v-60),
                            choices=str_choices,
                            choices_display=lstr_choices,
                            on_value_change_call=bui.Call(self.add_account, role))
                            
                        str_accs = []
                        str_choices = []
                        for acc in stg.config[role]['Ids']:
                            u = stg.config[role]['Ids'][acc]
                            str_accs.append(acc)
                            str_choices.append(bui.Lstr(value=acc))
                        
                        self._popupmenu3 = None
                        if any(str_choices):
                            self._popupmenu3 = PopupMenu(
                                parent=c,width=90,scale=2.4,
                                position=(360, v-60),
                                choices=str_accs,
                                choices_display=str_choices,
                                on_value_change_call=bui.Call(self.del_account, role))
                            
                        icon = bui.charstr(bui.SpecialChar.DELETE)
                        for t, p in [('Add', self._popupmenu2),
                                     (icon, self._popupmenu3)]:
                            if p is None: continue
                            bui.buttonwidget(
                                edit=p._button,label=getlanguage(t),
                                size=(100, 40), color=(0.1,0.5,1.0))
                        v -= 130
                else:
                    t2 = bui.textwidget(parent=c,position=(100, v-140),size=(width,50),
                        text=getlanguage('No Roles'),color=bui.app.ui_v1.title_color,h_align="center",
                        v_align="center",maxwidth=width*1.3)
        else:
            sub_height = 0
            v = sub_height - 55
            width = 300
            
            self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
                size=(self._sub_width,sub_height),
                background=False,selection_loops_to_parent=True)

            t = bui.textwidget(parent=c,position=(110, v-20),size=(width,50),
                      scale=1.4,color=(1.2,0.2,1.2),h_align="center",v_align="center",
                      text="Make Role Mod - Beta",maxwidth=width*30)

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

    #color picker
    def _make_picker(self, tag: Any):
        ColorPicker(
            parent=self._root_widget, position=(0,0),
            delegate=self, tag=tag)

    def color_picker_closing(self, picker):
        try:
            self._role_colors.append(picker._color)
            self.view_colors()
            bui.getsound('gunCocking').play()
        except Exception: pass

    def color_picker_selected_color(self, picker, color):
        picker._color = color

    def delete_role(self, role: str):
        def call():
            if role in stg.config:
                stg.config.pop(role)
                stg._save()
                bui.getsound('shieldDown').play()
                self._set_tab(GLOBAL['Tab'])

        ConfirmWindow(getlanguage('Change Notice'),
            height=100*1.5,cancel_button=True,width=200,
            action=call,ok_text=bui.Lstr(resource='okText'))

    def add_account(self, role: str, acc: str):
        u = GLOBAL['Players'][acc]
        
        def call():
            nm, pb = u[0], u[1]
            for data in stg.config.values():
                if acc in data['Ids']:
                    bui.screenmessage(getlanguage('Registered Player'), color=(1,0,0))
                    bui.getsound('error').play()
                    return
            
            if acc not in stg.config[role]['Ids']:
                stg.config[role]['Ids'][acc] = {
                    "Pb": pb, "Name": nm}
                stg._save()
                
                bui.screenmessage(f'{role} @ {acc}', color=(0,1,1))
                bui.getsound('dingSmallHigh').play()
                self._set_tab(GLOBAL['Tab'])
                
        tx = getlanguage('Info Player',
             alm=[acc, u[0], u[1]])
        
        ConfirmWindow(tx, width=200,
            height=100*1.5,cancel_button=True,
            action=call,ok_text=bui.Lstr(resource='okText'))
    
    def del_account(self, role: str, acc: str):
        def call():
            u = stg.config[role]
            u['Ids'].pop(acc)
            stg._save()
            
            bui.screenmessage(f"{role} @ {acc}", color=(1,0,0))
            bui.getsound('shieldDown').play()
            self._set_tab(GLOBAL['Tab'])
        
        ConfirmWindow(getlanguage('Change Notice'),
            height=100*1.5,cancel_button=True,width=200,
            action=call,ok_text=bui.Lstr(resource='okText'))
    
    def select_friend(self, obj: str):
        self._friend = obj
    
    def _vi_colors(self, val):
        val = tuple(float(n) for n in
              val.replace('(', '').replace(')',
              '').replace(',','').split(' '))
        bui.buttonwidget(edit=self.c_button, color=val)
        
    def view_colors(self):
        choices = []
        for c in self._role_colors:
            t_colors = ()
            for s in c:
                t_colors += (round(s, 2), )
            choices.append(t_colors)
        self._role_colors = choices
            
        str_choices = [str(c) for c in choices]
        if self._popupmenu:
            self._popupmenu.get_button().delete()
            self._popupmenu = None
        
        lstr_choices = [bui.Lstr(value=s) for s in str_choices]
        self._popupmenu = PopupMenu(
                parent=self._data[0],
                position=(60, self._data[1]-80),width=90,scale=2.4,
                choices=str_choices,
                choices_display=lstr_choices,
                on_value_change_call=bui.Call(self._vi_colors))

    def _save_role(self):
        GLOBAL['ETxt'][0] = role = bui.textwidget(query=self.t_edit1).strip()
        GLOBAL['ETxt'][1] = tag = bui.textwidget(query=self.t_edit2).strip()
        friend = self._friend
        colors = self._role_colors

        if role in stg.config:
            #stg.config[role]['Tag'] = tag
            stg.config[role]['Obj'] = friend
            if any(colors):
                stg.config[role]['Colors'] = colors
            stg._save()
            bui.screenmessage(getlanguage('Updated Role'), color=(0,1,0))
            bui.getsound('dingSmall').play()
            return

        if role == '' or tag == '' or colors == []:
            bui.screenmessage(getlanguage('Empty Text'), color=(1,0,0))
            bui.getsound('error').play()
            return

        stg.config[role] = dict()
        stg.config[role]['Tag'] = tag
        stg.config[role]['Ids'] = dict()
        stg.config[role]['Obj'] = friend
        stg.config[role]['Colors'] = colors
        stg._save()
        bui.screenmessage('%s @ %s' % (role, tag), color=(0,1,0))
        bui.getsound('gunCocking').play()
        
    def _back(self):
        pass

chatmsg = bs.chatmessage
def new_chatmsg(msg, *args):
    val = chatmsg(msg, *args)
    gcm = bs.get_chat_messages()[-1]
    m = gcm.split(': ')[0]+':'
    m = gcm.replace(m, '').strip()
    stg.edit_tag_from_chat(m)
    return val

def add_plugin():
    try: from baBearModz import BearPlugin
    except Exception as e:
        return bs.timer(2.5, lambda e=e:
               bs.screenmessage('Error plugin: ' + str(e), (1,0,0)))

    BearPlugin(icon='achievementsIcon',
               icon_color=(0.5, 0.2, 1.3),
               button_color=(0.8, 1.3, 0.8),
               creator='@PatrónModz',
               plugin=RoleMakerMod,
               window=TagWindow)
               
# ba_meta export plugin
class RoleMakerMod(bs.Plugin):
    ps.PlayerSpaz = NewPlayerSpaz
    bs.chatmessage = new_chatmsg

    def __init__(self) -> None:
        add_plugin()