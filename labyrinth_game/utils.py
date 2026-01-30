import math

from labyrinth_game.constants import (
    EVENT_PROBABILITY,
    EVENT_TYPES_COUNT,
    ROOMS,
    TRAP_DAMAGE_RANGE,
    TRAP_DAMAGE_THRESHOLD,
)
from labyrinth_game.player_actions import get_input


def pseudo_random(seed, modulo):
    sin_value = math.sin(seed * 12.9898)
    stretched = sin_value * 43758.5453
    fractional_part = stretched - math.floor(stretched)
    result = fractional_part * modulo
    return int(result)


def trigger_trap(game_state):
    print("Ловушка активирована.")
    inventory = game_state["player_inventory"]

    if inventory:
        random_index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли: {lost_item}")
    else:
        random_damage = pseudo_random(game_state["steps_taken"], TRAP_DAMAGE_RANGE)
        if random_damage < TRAP_DAMAGE_THRESHOLD:
            print("Ловушка нанесла смертельный урон")
            game_state["game_over"] = True
        else:
            print("Вам удалось избежать опасности")


def random_event(game_state):
    event_chance = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY)

    if event_chance != 0:
        return

    event_type = pseudo_random(game_state["steps_taken"] + 1, EVENT_TYPES_COUNT)

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if event_type == 0:
        print("\nВы нашли монетку на полу")
        room["items"].append("coin")
    elif event_type == 1:
        print("\nВы слышите странный шорох")
        if "sword" in game_state["player_inventory"]:
            print("Вы отпугиваете существо своим мечом")
    elif event_type == 2:
        if (
            current_room_name == "trap_room"
            and "torch" not in game_state["player_inventory"]
        ):
            print("\nОпасность Вы активировали ловушку")
            trigger_trap(game_state)


def describe_current_room(game_state):
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    print(f"\n== {current_room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        items_list = ", ".join(room["items"])
        print(f"\nЗаметные предметы: {items_list}")

    exits_list = ", ".join(room["exits"].keys())
    print(f"Выходы: {exits_list}")

    if room["puzzle"]:
        print("Здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if not room["puzzle"]:
        print("Загадок здесь нет")
        return

    question, correct_answer = room["puzzle"]
    print(f"\n{question}")

    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct_answer_lower = correct_answer.lower()

    answer_variants = {
        "10": ["10", "десять"],
        "шаг шаг шаг": ["шаг шаг шаг"],
        "резонанс": ["резонанс"],
        "елка": ["елка", "ель", "ёлка"]
    }

    is_correct = False
    for variants_list in answer_variants.values():
        if user_answer in [v.lower() for v in variants_list]:
            if correct_answer_lower in [v.lower() for v in variants_list]:
                is_correct = True
                break

    if is_correct:
        print("Верно, загадка решена")
        room["puzzle"] = None

        if current_room_name == "trap_room":
            game_state["player_inventory"].append("rusty_key")
            print("Вы получили: rusty_key")
        elif current_room_name == "hall":
            game_state["player_inventory"].append("treasure_key")
            print("Вы получили: treasure_key")
        elif current_room_name == "library":
            game_state["player_inventory"].append("ancient_scroll")
            print("Вы получили: ancient_scroll")
        elif current_room_name == "dungeon":
            game_state["player_inventory"].append("skeleton_ring")
            print("Вы получили: skeleton_ring")
    else:
        print("✗ Неверно. Попробуйте снова.")
        if current_room_name == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    from labyrinth_game.player_actions import get_input

    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, сундук открыт")
        ROOMS["treasure_room"]["items"].remove("treasure_chest")
        print("\nВ сундуке сокровище, Вы победили")
        return True

    response = get_input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()

    if response == "да":
        code = get_input("Введите код: ").strip()
        room = ROOMS["treasure_room"]
        if room["puzzle"] and code == room["puzzle"][1]:
            print("Правильный код. Сундук открыт")
            ROOMS["treasure_room"]["items"].remove("treasure_chest")
            print("\nВ сундуке сокровище, Вы победили")
            return True
        else:
            print("Неверный код")
            return False
    else:
        print("Вы отступаете от сундука")
        return False


def show_help():
    from labyrinth_game.constants import COMMANDS

    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")