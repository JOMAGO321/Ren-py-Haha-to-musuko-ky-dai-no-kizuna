################################################################################
## General Functions
################################################################################

screen display_hover(img):
    add img 

screen dynamic_button(btn):
    vbox:
        xpos btn["xpos"]
        ypos btn["ypos"]  
        imagebutton:                          
                idle game_core.get_image(btn["idle"])
                if "hover" in btn:
                    hover game_core.get_image(btn["hover"])
                if "action" in btn:
                    if btn["action"][0] == "show":
                        action Show (btn["action"][1])
                    elif btn["action"][0] == "showmap":
                        action Function (game_core.showmap)
                    elif btn["action"][0] == "scene":
                        action Function (game_core.scene,btn["action"][1])
                    elif btn["action"][0] == "jump":
                        action Jump (btn["action"][1])
        if "title" in btn:
            text str(btn["title"])

################################################################################S
## Mini Game Search Item
################################################################################

screen minigame1():
    add game_core.minigame1_background
    default find_item = False
    default tries = 0
    if find_item:
        add "image_ref.png":
            xpos 0.4
            ypos 0.3        
    hbox:
        xpos 0.1
        ypos 0.1
        textbutton "Tries: [tries] - Score: 0"
        textbutton "Return" action Call("game_screen")
    for i in game_core.elements:    
        imagebutton auto i["sprite"]:
            xpos i["pos"][0]
            ypos i["pos"][1]
            if i["selected"]:
                action SetScreenVariable("find_item",True)
            else:
                action SetScreenVariable("tries",tries+1)

################################################################################
## Mini Game Memory Jort
################################################################################
screen minigame2():
    #Add background
    #add "gui/custom/game_screen.png"
    hbox:
        xpos 0.1
        ypos 0.1
        text f"MEMORY {game_core.card_score}"
        textbutton "Return" action Call("end_minigame")
    for i in range(0,2):
        for j in range(0,4):
            vbox:
                xpos 200+500*i
                ypos 400+120*j
                frame:
                    xminimum 100
                    yminimum 100
                    $button_value = game_core.card_display[f"{i}{j}"]
                    textbutton f"{button_value}" action  Function(game_core.select_card,i,j) #,Play("sound", "audio/sfx/click.mp3")

