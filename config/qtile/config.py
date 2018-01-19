import re
import subprocess
from pathlib import Path

from libqtile import layout, hook
from libqtile.config import Group, Match, Screen

from bars import main_bar, bar1, bar2
from keys import keys, mouse, sc  # NOQA
from util import nb_monitors, init_notifications

init_notifications('some_name')

monitor_cmd = 'xrandr --output DP-1 --auto --primary --left-of eDP-1'

float_rules = [
    {'wname': 'Friends'},
    {'wmclass': 'feh'},
    {'wmclass': 'Sms.py'},
    {'wmclass': 'leagueclientux.exe'},
    {'wmclass': 'Gcr-prompter'},
]

floating_layout = layout.Floating(border_focus='#ffb6c1',
                                  float_rules=float_rules)

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2, border_focus='#ffb6c1')
]

widget_defaults = {'font': 'Sans', 'fontsize': 17, 'padding': 4}

main_screen = Screen(top=main_bar)
screen1 = Screen(top=bar1)
screen2 = Screen(top=bar2)

nb_screens = nb_monitors(enabled=True)
if nb_screens == 1:
    screens = [main_screen]
    groups = [Group(i) for i in 'asdf']
elif nb_screens == 2:
    screens = [screen1, screen2]
    groups = [Group(i) for i in 'asdfuiop']

groups.extend([
    Group('game', layouts=[layout.Max()], persist=False, init=False,
          matches=[Match(wm_class=['Steam'])], label='', exclusive=True),

    Group('chat', layouts=[layout.Max()], persist=False, init=False,
          matches=[Match(wm_class=['discord'])], label='', exclusive=True),

    Group('music', layouts=[layout.Max()], persist=False, init=False,
          matches=[Match(wm_class=[re.compile('spotify', re.I)])], label=''),
])


def wallpaper():
    img_name = 'wishyouwerehere_fancy.png'
    img_path = Path.home() / 'Pictures' / img_name
    subprocess.run(['feh', '--bg-scale', img_path])


@hook.subscribe.startup
def autostart():
    wallpaper()
    sc.set_profile('analog')


@hook.subscribe.startup_once
def autostart_once():
    subprocess.run(['compton', '-b'])


@hook.subscribe.addgroup
def go_to_group(qtile, group):
    try:
        qtile.groupMap[group].cmd_toscreen()
    except AttributeError:
        pass


@hook.subscribe.screen_change
def configure_screens(qtile, ev):
    nb_plugged = nb_monitors()
    if nb_plugged == 1:
        subprocess.run(['xrandr', '--auto'])
        qtile.cmd_restart()
    elif nb_plugged == 2:
        subprocess.run(monitor_cmd.split())
        qtile.cmd_restart()
    else:
        qtile.cmd_restart()


dgroups_app_rules = []
dgroups_key_binder = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'focus'
wmname = 'LG3D'
