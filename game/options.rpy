define config.name = _("Example")
define gui.show_name = True
define config.version = "1.0"
define gui.about = _p("""
""")
define build.name = "Example"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

init -1 python hide:
    if os.path.isfile(searchpath() + "\\audio\\main_menu.mp3") and persistent.menu_music:
        config.main_menu_music = "audio/main_menu.mp3"

define config.enter_transition = dissolve
define config.exit_transition = dissolve

define config.intra_transition = dissolve

define config.after_load_transition = None

define config.end_game_transition = None

define config.window = "auto"

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 35

default preferences.afm_time = 15

define config.save_directory = "Example-1679431256"

define config.window_icon = "gui/window_icon.png"

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.documentation('*.html')
    build.documentation('*.txt')
