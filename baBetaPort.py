# ba_meta require api 8

import bascenev1 as bs
import bauiv1 as bui

# ba_meta export plugin
class BetaPort17(bs.Plugin):
    def __init__(self) -> None:
        def a():
            context = bui.app.ui_v1.title_color
            bs.chatmessage(str(context))
            
        bs.apptimer(1.5, a)