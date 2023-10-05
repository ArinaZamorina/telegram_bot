def print_history(command_dict):
    string_for_print = [
        f'Команда: {command_dict.get("COMMAND")}\n\nВремя вызова команды: {command_dict.get("TIME")}\n\n'
        f"Отели: " + ', '.join(command_dict["HOTELS_DICT"].keys())]

    return string_for_print
