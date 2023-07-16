# ba_meta require api 8

from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar

import random
import bascenev1 as bs

from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.popuptext import PopupText
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.game.elimination import Icon
from bascenev1lib.actor.powerupbox import PowerupBox, PowerupBoxFactory

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional

PlayerType = TypeVar('PlayerType', bound='bs.Player')
TeamType = TypeVar('TeamType', bound='bs.Team')

def getlanguage(text, subs: str = ''):
    lang = bs.app.lang.language
    translate = {"Game Name":
                      {"Spanish": "Sin Retorno",
                       "English": "No return",
                       "Portuguese": "Sem retorno"},
                 "Game Description":
                      {"Spanish": "Derrota a todo el equipo enemigo.",
                       "English": "Defeat the opposing team",
                       "Portuguese": "Derrotar a equipe inimiga"},
                 "Rounds":
                      {"Spanish": "Rondas",
                       "English": "Rounds",
                       "Portuguese": "Rodadas"},
                 "S: Powerups":
                      {"Spanish": "Aparecer Potenciadores",
                       "English": "Powerups Spawn",
                       "Portuguese": "Habilitar Potenciadores"},
                 "S: Gloves":
                      {"Spanish": "Habilitar Guantes de Boxeo",
                       "English": "Enable Boxing Gloves",
                       "Portuguese": "Habilitar Luvas de Boxe"},
                 "S: Extreme":
                      {"Spanish": "Modo Extremo",
                       "English": "Extreme Mode",
                       "Portuguese": "Modo Extremo"},
                 "S: Egg":
                      {"Spanish": "Habilitar Huevo Dorado",
                       "English": "Enable Golden Egg",
                       "Portuguese": "Habilitar o Ovo de Ouro"},
                 "Info":
                      {"Spanish": "Derrota %s veces al equipo rival." % subs,
                       "English": "Defeat the opposing team %s times" % subs,
                       "Portuguese": "Derrotar a equipe adversária %s vezes." % subs},
                }
                
    languages = ['Spanish','Portuguese','English']
    if lang not in languages: lang = 'English'

    if text not in translate:
        return text
    return translate[text][lang]

def fake_explosion(position: Sequence[float],
                   radius: float = 1.8,
                   color: Sequence[float] = (0.23,0.23,0.23)):
    explosion = bs.newnode('explosion',
               attrs={'position': position, 'color': color,
                      'radius': radius, 'big': False})
    bs.timer(1.0, explosion.delete)

class Player(bs.Player['Team']):
    """Our player type for this game."""
    
    icons: List[Icon] = []

class Team(bs.Team[Player]):
    """Our team type for this game."""
    
    score = 0
        
class NewPlayerSpaz(PlayerSpaz):
    def __init__(self, *args, mode_extreme: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_hp = self.hitpoints
        
        if mode_extreme:
            self.extreme()
            self.node.color = tuple(
                c*3 for c in self.node.color)
        
    def extreme(self):
        def decrease():
            mag = int(self.old_hp * 0.03)
            self.handlemessage(bs.HitMessage(flat_damage=mag,
                               force_direction=self.node.velocity,
                               pos=self.node.position,hit_type='extreme'))
        self.decrease_hp = bs.Timer(1.5,
            bs.WeakCall(decrease),repeat=True)
        
    def handlemessage(self, msg: Any) -> Any:
        if self.hitpoints > self.old_hp:
            self.old_hp = self.hitpoints
        
        if isinstance(msg, bs.HitMessage):
            old_hp = self.hitpoints
            super().handlemessage(msg)
            new_hp = self.hitpoints
            HP = int(old_hp-new_hp)
            HP = int(HP / 10)
            
            if msg.hit_type == 'extreme' and not self.shield and not self.node.invincible:
                PopupText(text='-'+str(HP)+'%',scale=1.65,
                position=self.node.position_center,color=(1.1,0.2,0)).autoretain()
        elif isinstance(msg, bs.DieMessage):
            self.decrease_hp = None
            super().handlemessage(msg)
        else:
            return super().handlemessage(msg)
        
class GoldenEgg(bs.Actor):
    def __init__(self, position: Tuple[float, float, float] = (0.0, 1.0, 0.0)):
        super().__init__()
        activity = self.activity
        assert isinstance(activity, NoReturns)
        shared = SharedObjects.get()
        
        self._spawn_pos = (position[0], position[1] + 1.0, position[2])
        mesh = bs.getmesh('egg')
        ctex = bs.gettexture('aliColor')

        mats = [shared.object_material]
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': mesh,
                                   'color_texture': ctex,
                                   'body': 'capsule',
                                   'reflection': 'soft',
                                   'mesh_scale': 0.5,
                                   'body_scale': 0.6,
                                   'density': 4.0,
                                   'reflection_scale': [0.15],
                                   'shadow_size': 0.6,
                                   'position': self._spawn_pos,
                                   'materials': mats})
        
        self.shield = bs.newnode('shield',owner=self.node,attrs={'color':(0,1,6),'radius':1.0})
        self.node.connectattr('position', self.shield, 'position')
        bs.timer(20.0, bs.Call(self.handlemessage,bs.DieMessage()))

    def exists(self) -> bool:
        return bool(self.node)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PickedUpMessage):
            activity = self.activity
            assert isinstance(activity, NoReturns)
            team = None

            for player in activity.players:
                if player.is_alive():
                    if player.actor.node is msg.node:
                        team = player.team
                    
            if team is not None:
                team = team
                activity = activity
                teams = activity.teams_list[team]
                oldteams = [p for p in activity.old_teams_list[team]]
                
                for player in oldteams:
                    if player in teams or player.is_alive():
                        oldteams.remove(player)

                if any(oldteams):
                    for player in oldteams:
                        if player.is_alive():
                            oldteams.remove(player)

                if any(oldteams):
                    friend = random.choice(oldteams)
                    if not friend.is_alive():
                        activity.reboot_players(friend)
                        bs.getsound('spawn').play()
                else:
                    for player in activity.teams_list[team]:
                        player.actor.handlemessage(
                            bs.PowerupMessage(poweruptype='health'))
                    bs.getsound('healthPowerup').play()
            self.handlemessage(bs.DieMessage())
        elif isinstance(msg, bs.DieMessage):
            if self.node:
                bs.animate(self.node,'mesh_scale', {0: self.node.mesh_scale, 0.3: 0})
                bs.timer(0.3, self.node.delete)
        else:
            super().handlemessage(msg)
      
class Icon(Icon):
    def handle_player_spawned(self) -> None:
        """Our player spawned; hooray!"""
        if not self.node:
            return
        self.node.opacity = 1.0
        self._player.lives = 1

# ba_meta export bascenev1.GameActivity
class NoReturns(bs.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = getlanguage('Game Name')
    description = getlanguage('Game Description')

    # Es para anunciar la muerte de un jugador (osea el sonido que hace cuando un jugador muere.)
    # Nota: no es el mismo sonido que hace un peronaje cuando muere. 
    announce_player_deaths = True

    #Este metodo es para definir las opciones del minujuego:
    #Solo emplea las que el minijuego necesite. Asimismo puedes agregar opciones nuevas
    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[bs.Session]) -> List[bs.Setting]:
        settings = [

            #Define valores numericos, en este caso puntos para ganar.
            bs.IntSetting(getlanguage('Rounds'),
                min_value=2,
                max_value=8,
                default=2,
                increment=1,
            ),

            #Define un valor numerico que se usara como tiempo limite
            bs.IntChoiceSetting('Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),

            #Define la camara lenta
            bs.BoolSetting('Epic Mode', default=False),
            bs.BoolSetting(getlanguage('S: Powerups'), default=False),
            bs.BoolSetting(getlanguage('S: Gloves'), default=False),
            bs.BoolSetting(getlanguage('S: Extreme'), default=False),
            bs.BoolSetting(getlanguage('S: Egg'), default=False),
        ]

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: Type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        assert bs.app.classic is not None
        maps = bs.app.classic.getmaps('melee')
        maps.remove('Happy Thoughts')
        maps.append('Tower D')
        return maps #Mapa en especifico

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._dingsound = bs.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._score_to_win: Optional[int] = None
        self._wait_restart: Optional[bool] = False
        
        self._points_to_win = int(
            settings[getlanguage('Rounds')])
        self._enable_powerups = bool(
            settings[getlanguage('S: Powerups')])
        self._enable_boxing_gloves = bool(
            settings[getlanguage('S: Gloves')])
        self._enable_extreme = bool(
            settings[getlanguage('S: Extreme')])
        self._enable_egg = bool(
            settings[getlanguage('S: Egg')])
            
        self._time_limit = float(settings['Time Limit'])
        self._allow_negative_scores = bool(
            settings.get('Allow Negative Scores', False))
        self.slow_motion = self._epic_mode

        self.teams_list = {}
        self.old_teams_list = {}
        self.old_players = []
        self._golden_egg_spawn_timer = None
        self.default_music = bs.MusicType.GRAND_ROMP

    def get_instance_description(self) -> Union[str, Sequence]:
        ARG1 = self._score_to_win
        return getlanguage('Info', ARG1)

    def get_instance_description_short(self) -> Union[str, Sequence]:
        ARG1 = self._score_to_win
        return getlanguage('Info', ARG1)

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score, self._score_to_win)

    def spawn_player_spaz(
        self,
        player: PlayerT,
        position: Sequence[float] | None = None,
        angle: float | None = None,
    ) -> PlayerSpaz:
        """Create and wire up a bascenev1.PlayerSpaz for the provided Player."""
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from bascenev1._gameutils import animate
        from bascenev1._coopsession import CoopSession
        from bascenev1lib.actor.playerspaz import PlayerSpaz

        name = player.getname()
        color = player.color
        highlight = player.highlight

        light_color = bs.normalized_color(color)
        display_color = bs.safecolor(color, target_intensity=0.75)
        spaz = NewPlayerSpaz(
            color=color,
            highlight=highlight,
            character=player.character,
            player=player,
        )

        player.actor = spaz
        assert spaz.node

        spaz.node.name = name
        spaz.node.name_color = display_color
        spaz.connect_controls_to_player()
        
        if position is None:
            # In teams-mode get our team-start-location.
            if isinstance(self.session, bs.DualTeamSession):
                position = self.map.get_start_position(player.team.id)
            else:
                # Otherwise do free-for-all spawn locations.
                position = self.map.get_ffa_start_position(self.players)

        
        # Move to the stand position and add a flash of light.
        spaz.handlemessage(
            bs.StandMessage(
                position, angle if angle is not None else random.uniform(0, 360)
            )
        )
        self._spawn_sound.play(1, position=spaz.node.position)
        light = bs.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        bs.timer(0.5, light.delete)
        return spaz

    def players_in_teams(self, player: Player) -> bs.Actor:
        team = player.team
        
        if self.teams_list.get(team) is None:
            self.teams_list[team] = []
           
        if self.teams_list.get(team) is not None:
            if player not in self.teams_list[team]:
                self.teams_list[team].append(player)
                
        if self.old_teams_list.get(team) is None:
            self.old_teams_list[team] = []
           
        if self.old_teams_list.get(team) is not None:
            if player not in self.old_teams_list[team]:
                self.old_teams_list[team].append(player)
        
    def spawn_player(self, player: Player) -> bs.Actor:
        self.players_in_teams(player)
        
        if player not in self.old_players:
            self.old_players.append(player)
            
        spaz = super().spawn_player(player)
        
        if any(player.icons):
            for icon in player.icons:
                icon.handle_player_spawned()
        self._update_icons()
        
        return spaz
   
    def reboot_players(self, player):
        self._wait_restart = False
        if player.actor.node.exists():
            fake_explosion(player.actor.node.position,radius=2.5)
            player.actor.node.delete()

        self.spawn_player(player)
   
    def new_round(self, team, time: float = 4):
        self._wait_restart = True

        if self.slow_motion and time != 0:
            time *= 0.4
            
        if any(self.teams_list):
            for l_teams in self.teams_list:
                self.teams_list[l_teams] = []

        if not team.score >= self._score_to_win:
            for player in self.old_players:
                if player.actor.exists():
                    player.actor.node.invincible = True
                    player.actor.handlemessage(bs.CelebrateMessage(duration=time))
                    player.actor.disconnect_controls_from_player()
                bs.timer(time, bs.Call(self.reboot_players,player))
                
            if time != 0:
                bs.getsound('cheer').play()

        self._update_scoreboard()        

    def mode_teams(self, msg):
        player = msg.getplayer(Player)
        killer = msg.getkillerplayer(Player)
        team = player.team

        for dead_player in self.teams_list[team]:
            if dead_player is player:
                if dead_player in self.teams_list[team]:
                    self.teams_list[team].remove(player)
        
        self._update_points(team)
        
        for icon in player.icons:
            icon.handle_player_died()

    def _update_points(self, team):
        if any(self.teams_list):
            if len(self.teams_list[team]) <= 0:
                for tm in self.teams:
                    if tm is not team:
                        if not self._wait_restart:
                            tm.score += 1
                            self.new_round(tm)
            self._update_scoreboard()

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            # Augment standard behavior.
            super().handlemessage(msg)
            if isinstance(self.session, bs.DualTeamSession):
                bs.timer(0, bs.Call(self.mode_teams,msg))

        else:
            return super().handlemessage(msg)
    
    def _golden_egg_spawn(self):
        try:
            pos = random.choice(
                list(self.map.defs.points.values()))
        except:
            pos = (2,9,2)
        GoldenEgg(pos).autoretain()
    
    def on_begin(self) -> None:
        super().on_begin()
        self._start_time = bs.time()
        self.setup_standard_time_limit(self._time_limit)

        if self._enable_powerups:
            self.setup_standard_powerup_drops()
            
        if self._enable_egg:
            self._golden_egg_spawn_timer = bs.Timer(
                26.0, bs.WeakCall(self._golden_egg_spawn),repeat=True)
            
        self._score_to_win = max(self._points_to_win, 1)
        self._update_scoreboard()
        bs.timer(1.0, self._update, repeat=True)

    def _standard_drop_powerup(self, index: int, expire: bool = True) -> None:
        # pylint: disable=cyclic-import
        powerups_banned = []
        if self._enable_boxing_gloves:
            powerups_banned.append('punch')
        if self._enable_extreme:
            powerups_banned.append('health')

        get_powerup_type = PowerupBoxFactory.get(
            ).get_random_powerup_type(excludetypes=powerups_banned)
        
        PowerupBox(
            position=self.map.powerup_spawn_points[index],
            poweruptype=get_powerup_type,
            expire=expire).autoretain()

    def _update(self):
        if len(self._get_living_teams()) < 2:
            self._round_end_timer = bs.Timer(0.5, self.end_game)
            return

        for team in self.teams:
            if team.score >= self._score_to_win:
                self._round_end_timer = bs.Timer(0, self.end_game)
                return

        self._get_living_players()
        self._update_icons()
                
    def _get_living_teams(self) -> List[Team]:
        return [
            team for team in self.teams
            if len(team.players)
        ]
        
    def _get_living_players(self) -> List[Team]:
        if not any(self.old_players):
            self._round_end_timer = bs.Timer(0, self.end_game)
            return
        
        if len(self.old_players) <= 1:
            self._round_end_timer = bs.Timer(0, self.end_game)
            return
        
        if any(self.old_teams_list):
            for team, list_player in self.old_teams_list.items():
                if len(list_player) <= 0:
                    self._round_end_timer = bs.Timer(0, self.end_game)
                    break
                    
        for team in self.teams:
            if len(team.players) <= 0:
                self._round_end_timer = bs.Timer(0, self.end_game)
                break

    def on_player_join(self, player: Player) -> None:
        # No longer allowing mid-game joiners here; too easy to exploit.
        if self.has_begun():
            # Make sure their team has survival seconds set if they're all dead
            # (otherwise blocked new ffa players are considered 'still alive'
            # in score tallying).
            bs.broadcastmessage(
                bs.Lstr(resource='playerDelayedJoinText',subs=[('${PLAYER}',
                player.getname(full=True))]),color=(0, 1, 0))
            return

        player.icons = [Icon(player, position=(0, 50), scale=0.8, show_lives=False)]
        self._update_icons()
        super().on_player_join(player)
    
    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        team = player.team
        player.icons = []
        if player in self.old_teams_list[team]:
            self.old_teams_list[team].remove(player)
        if player in self.teams_list[team]:
            self.teams_list[team].remove(player)
        if player in self.old_players:
            self.old_players.remove(player)
        self._update_points(team)
        
    def _update_icons(self) -> None:
        for team in self.teams:
            if team.id == 0:
                xval = -80
                x_offs = -100
            else:
                xval = 80
                x_offs = 100
            for player in team.players:
                for icon in player.icons:
                    icon.set_position_and_scale((xval, 30), 0.85)
                xval += x_offs
    
    def end_game(self) -> None:
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)