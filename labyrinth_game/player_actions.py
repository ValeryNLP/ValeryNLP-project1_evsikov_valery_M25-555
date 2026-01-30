def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    inventory = game_state["player_inventory"]
    if inventory:
        items_list = ", ".join(inventory)
        print(f"\nИнвентарь: {items_list}")
    else:
        print("\nИнвентарь пуст.")


def move_player(game_state, direction):
    from labyrinth_game.constants import ROOMS
    from labyrinth_game.utils import (
        describe_current_room,
        random_event,
    )

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if direction not in room["exits"]:
        print("Нельзя пойти в этом направлении")
        return

    new_room_name = room["exits"][direction]

    if new_room_name == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше")
            return
        else:
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
            )

    game_state["current_room"] = new_room_name
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state, item_name):
    from labyrinth_game.constants import ROOMS

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый")
        return

    if item_name not in room["items"]:
        print("Такого предмета здесь нет.")
        return

    game_state["player_inventory"].append(item_name)
    room["items"].remove(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state, item_name):
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Факел освещает всё")

    elif item_name == "sword":
        print("Вы берёте меч в руку")

    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку")
        if "rusty_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("rusty_key")
            print("Внутри вы находите ржавый ключ")
        else:
            print("Шкатулка пуста.")

    elif item_name == "note":
        print("На записке корявым почерком выведено: 'Не верь эху'")
    elif item_name == "glowing_mushroom":
        print("Вы съели светящийся гриб. Ваши руки начали слегка светиться в темноте")
    elif item_name == "berries":
        print("Вы съели горсть ягод. Они оказались горькими, но утолили голод")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
