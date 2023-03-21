define e = Character("Maria")

image maria_happy = 'images/maria_happy.png'
image maria_happy2 = 'images/maria_happy2.png'
image maria_miserable = 'images/maria_miserable.png'
image bg = 'images/bg.png'
define gama_music = "audio/music.mp3"

label start:

    stop music fadeout 1.0

    $ link = "https://www.dropbox.com/s/con9os8cd11be67/test.zip?dl=1"
    $ path = searchpath() + "/game_data.zip"

    if not persistent.download:
        call screen download(url = link, savepath = path, auto_extract = True)

    scene bg

    show maria_happy with dissolve

    e "Hello, my name is Maria. I am a test character of this project. Thank you so much for downloading very important files before talking to me!"

    menu:
        e "Do you want to check the performance of the music file downloaded with me?"

        "Yes":
            play music gama_music

            e "Everything seems to be working! Now let's check all my sprites."

            stop music fadeout 1.0

            show maria_happy2 with dissolve

            pause(2.0)

            show maria_miserable with dissolve
        
        "No":
            e "OK, let's check my sprites then"

            show maria_happy2 with dissolve

            pause(2.0)

            show maria_miserable with dissolve

    e "Sprites also work, and now our little dialogue ends and I give you a small gift in the form of music in the main menu."

    $ persistent.menu_music = True

    return
