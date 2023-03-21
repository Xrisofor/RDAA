init:
    image icon_success = "rdaa/icon/ic_success.png"
    image icon_warning = "rdaa/icon/ic_warning.png"

screen download(url, savepath = None, auto_extract = False):
    modal True
    default dl = DownloadHandler(url, savepath, auto_extract)
    on "show" action Function(dl.start)

    showif dl.status():
        frame:
            xysize(700, 300) align(0.5, 0.5)
            has vbox spacing 20 align(0.5, 0.5)

            if dl.runtime_exception():
                add "icon_warning" xalign 0.5
                text _("Error loading the file") color "#FF0" xalign 0.5
                textbutton _("Back to the main menu") action MainMenu() xalign 0.5
            else:
                add "icon_success" xalign 0.5
                text _("Download completed!") color "#0A0" xalign 0.5
                textbutton _("Restart the game") action [SetField(persistent, "download", True), Function(renpy.quit, relaunch = True, status = 0, save = False)] xalign 0.5

    else:
        frame:
            xysize(700, 300) align(0.5, 0.5)
            has vbox spacing 20  align(0.5, 0.5)

            text _("Loading resources...") xalign 0.5
            text _("Progress: %.2f MB / %.2f MB") % (dl.sizelist[0], dl.sizelist[1]) xalign 0.5

            hbox:
                xalign 0.5 spacing 20

                bar value AnimatedValue(dl.gauge, 1.0):
                    xmaximum 350

                text "[[{0:.1%}]".format(dl.gauge)

screen mediafire_dl(shared_url, savepath = None):
    
    default dlfetch = SharedCloudGetFile(shared_url)
    on "show" action Function(dlfetch.start)

    showif dlfetch.status():
        frame:
            xysize(700, 300) align(0.5, 0.5)
            has vbox spacing 20 align(0.5, 0.5)

            if dlfetch.runtime_exception():
                add "icon_warning" xalign 0.5
                text _("Error occurred while retrieving the URL") color "#FF0" xalign 0.5
                textbutton _("Back to the main menu") action MainMenu() xalign 0.5
            else:
                timer 0.01 action [Hide("mediafire_dl"), Show("download", url = dlfetch.end_url(), savepath = savepath)]

    else:
        frame:
            xysize(700, 300) align(0.5, 0.5)
            has vbox spacing 20  align(0.5, 0.5)

            text _("Wait a few seconds") xalign 0.5
            text _("Getting download URLs...") xalign 0.5
