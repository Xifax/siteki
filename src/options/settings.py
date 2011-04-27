# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# external
from userconfig import UserConfig

# own
from utils.const import _name, __version__

class Config:

    def __init__(self):
        self.defaults = [
            ('position',
                 {'top' : False,
                  'resize' : False,
                  'center' : False,
                  'coordinates' : (0, 0)
                 }
            ),
            ('states',
                {'save_position' : False,
                 'save_buttons' : False,
                 'tray' : False
                }
            ),
             ('buttons',
                {'toggle' : False,
                 'font' : False,
                 'excluded' : False,
                 'options' : False,
                },
            )
        ]

        try:
            self.active_config = UserConfig(_name, self.defaults, version=__version__)
        except IOError, e:
            print e

    # getting position options
    def on_top(self):
        return self.active_config.get('position', 'top')

    def resize(self):
        return self.active_config.get('position', 'resize')

    def center(self):
        return self.active_config.get('position', 'center')

    def get_position(self):
        return self.active_config.get('position', 'coordinates')

    # setting position options
    def set_on_top(self, state):
        self.active_config.set('position', 'top', state)

    def set_resize(self, state):
        self.active_config.set('position', 'resize', state)

    def set_center(self, state):
        self.active_config.set('position', 'center', state)

    def set_position(self, position):
        self.active_config.set('position', 'top', position)

    # getting states options
    def save_position(self):
        return self.active_config.get('states', 'save_position')

    def save_buttons(self):
        return self.active_config.get('states', 'save_buttons')

    # setting states options
    def set_save_position(self, state):
        self.active_config.set('states', 'save_position', state)

    def set_save_buttons(self, state):
        self.active_config.set('states', 'save_buttons', state)

    # getting buttons states
    def toggle(self):
        return self.active_config.get('buttons', 'toggle')

    def font(self):
        return self.active_config.get('buttons', 'font')

    def excluded(self):
        return self.active_config.get('buttons', 'excluded')

    def options(self):
        return self.active_config.get('buttons', 'options')

    # setting buttons states
    def set_toggle(self, state):
        self.active_config.set('buttons', 'toggle', state)

    def set_font(self, state):
        self.active_config.set('buttons', 'font', state)

    def set_excluded(self, state):
        self.active_config.set('buttons', 'excluded', state)

    def set_options(self, state):
        self.active_config.set('buttons', 'options', state)