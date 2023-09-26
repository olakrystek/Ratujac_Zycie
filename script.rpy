define a = Character("Aniela")
define b = Character("Bernard")
define r = Character("Dyspozytor medyczny")

define flash = Fade(0.1, 0.0, 0.5, color="#990000")

image a_walking:
    animation
    "a_def.png"
    parallel:
        xalign 1.0
        linear 5.0 xalign 0.0
    parallel:
        yalign 0.0
        easeout 0.5 yalign 0.25
        easein 0.5 yalign 0.0
        repeat

image b_walking:
    animation
    "b_def.png"
    parallel:
        xalign 0.8
        linear 5.3 xalign 0.2
    parallel:
        yalign 0.0
        easeout 0.5 yalign 0.25
        easein 0.5 yalign 0.0
        repeat

transform alpha_dissolve:
    alpha 0.0 # the bar fades in and out
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0

init:
    $ timer_range = 0
    $ timer_jump = 0
    $ time = 0

screen countdown:
    timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01), false=[Hide('countdown'), Jump(timer_jump)])
        ### ^this code decreases variable time by 0.01 until time hits 0, at which point, the game jumps to label timer_jump (timer_jump is another variable that will be defined later)

    bar value time range timer_range xalign 0.5 yalign 0.9 xmaximum 300 at alpha_dissolve


label start:

    play music "audio/music.wav"
    scene bg1                              #scene 1
    with fade
    show a_walking
    show b_walking

    #$ renpy.pause()
    pause 6.0

    jump question_1

label question_1:

    scene bg2                                        #scene 2
    show a_concerned at left with easeinleft
    a "Zobacz, ktoś tam leży…"
    scene bg3                                        #scene 2-1

    label menu1:
        $ time = 7                                     ### set variable time to 7
        $ timer_range = 7                              ### set variable timer_range to 7 (this is for purposes of showing a bar)
        $ timer_jump = 'menu1_slow'                    ### set where you want to jump once the timer runs out
        show screen countdown                          ### call and start the timer

        show b_concerned at right with dissolve
        play sound "audio/sound.wav"

        menu:
            "To nic, pewnie jest pijany.":                  #F
                hide screen countdown                  ### stop the timer
                stop sound fadeout 1.0

                jump end

            "Sprawdźmy, może potrzebuje pomocy.":           #T
                hide screen countdown                  ### stop the timer
                stop sound fadeout 1.0

                hide a_concerned with easeoutleft
                show b_concerned at right

                b "Sprawdźmy, może potrzebuje pomocy."
                b "Halo! Czy Pan mnie słyszy? Proszę otworzyć oczy."

                show a_concerned at left with dissolve
                a "Sprawdź, czy oddycha, a ja zadzwonię na pogotowie."

                jump question_2

    label menu1_slow:
        hide b_concerned
        stop sound fadeout 1.0
        scene bg3 with hpunch
        with flash
        "{size=+10}{b}Musisz działać szybciej!{/size}{/b}"
        jump menu1

label question_2:                                  #scene 3

    scene bg4
    "Wybierz:"

    label menu2:
        $ time = 7
        $ timer_range = 7
        $ timer_jump = 'menu2_slow'

        show screen countdown
        play sound "audio/sound.wav"

        menu:
            "Pochyl się i zbliż policzek do ust poszkodowanego, staraj się usłyszeć i poczuć oddech.":
                hide screen countdown
                stop sound fadeout 1.0

                show a_concerned at left with dissolve
                a "Pochyl się i zbliż policzek do ust poszkodowanego, staraj się usłyszeć i poczuć oddech."

                scene bg_event                       #scene 3-1
                $ renpy.pause()

                jump question_3

            "Przyłóż lusterko do ust poszkodowanego, jeżeli zaparuje to znaczy, że oddycha.":
                hide screen countdown
                stop sound fadeout 1.0

                jump end

    label menu2_slow:
        hide a_concerned
        stop sound fadeout 1.0
        scene bg4 with hpunch
        with flash
        "{size=+10}{b}Każda sekunda ma znaczenie. Podejmuj decyzje szybciej!{/size}{/b}"
        jump menu2

label question_3:                                #scene 4

    scene bg2

    label menu3:
        $ time = 7
        $ timer_range = 7
        $ timer_jump = 'menu3_slow'

        show screen countdown
        play sound "audio/sound.wav"

        show tel
        $ flag = True
        while flag is True:
            python:
                answer = renpy.input("Wybierz numer:")
                answer = answer.strip()

            if (len(answer) == 3 and answer.isdigit()) and (answer == "999" or answer == "112"):
                hide screen countdown
                stop sound fadeout 1.0

                "Łączę z {b}[answer]{/b}...{w=1.0}{nw}"
                $ flag = False

            else:
                stop sound fadeout 1.0
                hide screen countdown
                with flash
                "{size=+10}{b}Błędny numer.{/size}{/b}"

        scene bg_call with fade                 #scene 4-1

        show r_talk at right with easeinright
        r "Pogotowie ratunkowe, słucham."
        show a_talk at left with easeinleft
        a "Dzień dobry, w pobliżu budynku D1 na kampusie AGH znaleźliśmy nieprzytomnego mężczyznę. Nie oddycha."

        jump question_4

    label menu3_slow:
        hide tel
        stop sound fadeout 1.0
        scene bg2 with hpunch
        with flash
        "{size=+10}{b}Działasz zbyt wolno!{/size}{/b}"
        jump menu3

label question_4:                               #scene 5

    scene bg4 with fade

    show b_think at right with easeinright
    b "Gdzie powinienem uciskać klatkę piersiową?"

    label menu4:
        $ time = 7
        $ timer_range = 7
        $ timer_jump = 'menu4_slow'

        show screen countdown
        play sound "audio/sound.wav"

        menu:
            "W dolnej połowie mostka.":
                hide screen countdown
                stop sound fadeout 1.0

                hide b_think with easeoutright

                show a_happy at left with dissolve
                a "Pogotowie już jedzie."
                hide a_happy with dissolve

                jump question_5

            "W górnej połowie mostka.":
                hide screen countdown
                stop sound fadeout 1.0

                jump end

    label menu4_slow:
        hide b_think
        stop sound fadeout 1.0
        scene bg4 with hpunch
        with flash
        "{size=+10}{b}Pospiesz się!{/size}{/b}"
        jump menu4

label question_5:                             #scene 6

    show b_think at right with dissolve
    b "Co mam zrobić teraz?"

    label menu5:
        $ time = 7
        $ timer_range = 7
        $ timer_jump = 'menu5_slow'

        show screen countdown
        play sound "audio/sound.wav"

        menu:
            "20 uciśnięć, głębokość 5-6 cm, tempo 100-120/min":
                hide screen countdown
                stop sound fadeout 1.0

                jump end

            "30 uciśnięć, głębokość 5-6 cm, tempo 100-120/min":
                hide screen countdown
                stop sound fadeout 1.0

                hide b_think

                show r_talk at left with dissolve
                "{i}Utrzymuj ramiona wyprostowane, prostopadle do klatki piersiowej, nie uginając ich w łokciach podczas ucisku.{/i}" #INFO
                hide r_talk with dissolve

                jump question_6

    label menu5_slow:
        hide b_think
        stop sound fadeout 1.0
        scene bg4 with hpunch
        with flash
        "{size=+10}{b}Czas ucieka...{/size}{/b}"
        jump menu5

label question_6:

    label menu6:
        $ time = 7
        $ timer_range = 7
        $ timer_jump = 'menu6_slow'

        show screen countdown
        play sound "audio/sound.wav"

        $ flag1 = True
        while flag1 is True:
            show b_think at right with dissolve
            python:
                answer1 = renpy.input("Ile powinienem wykonać oddechów ratowniczych?")
                answer1 = answer1.strip()

            if answer1.isdigit() and answer1 == "2":
                hide screen countdown
                stop sound fadeout 1.0
                hide b_think

                show r_talk at left with dissolve
                "{i}Wykonaj spokojny, normalny wdech trwający ok. 1 sek, równocześnie obserwując unoszenie się klatki piersiowej poszkodowanego.{/i}" #INFO
                "{i}Czas na wykonanie 2 wdechów i ponowne rozpoczęcie uciskania klatki piersiowej nie powinien być dłuższy niż 5 sekund.{/i}" #INFO
                hide r_talk with dissolve

                $ flag1 = False

            else:
                stop sound fadeout 1.0
                hide screen countdown
                with flash
                "{size=+10}{b}Nieprawidłowo wykonane oddechy ratownicze, wykonaj je poprawnie.{/size}{/b}"

    scene bg_end with fade                               #scene 7
    show a_vhappy at left with easeinleft
    show b_vhappy at right with easeinright

    a "Pogotowie już jest."
    b "Chyba się udało!"

    jump end_2

    label menu6_slow:
        hide b_think
        stop sound fadeout 1.0
        scene bg4 with hpunch
        with flash
        "{size=+10}{b}Musisz podejmować decyzje szybciej, {color=#990000}ratujesz życie{/color}!{/size}{/b}"
        jump menu6

label end:
    stop sound fadeout 1.0
    scene bg false with vpunch:                             #end scene 1
    "{size=+10}{b}Niestety popełniłeś błąd. Zagraj jeszcze raz.{/b}{/size}"
    jump start
    return

label end_2:
    stop sound fadeout 1.0
    scene bg2 with fade:                                              #end scene 2
    show r_def with zoomin
    show a_vhappy at left with zoomin
    show b_vhappy at right with zoomin
    "{size=+10}{b}GRATULACJE!{/b}{/size}"
    return
