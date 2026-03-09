label start:

    $game_core = core()
    $game_core.tanix_log.info(f"MAIN_GAME")
    $game_core.shuffle()
    call screen minigame2()

    
label end_minigame:
    "mingame done"

    return
    