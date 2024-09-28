import os
import json


def find_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json') and f != 'config.json']


def read_config_language(config_path):
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
        return config_data.get('language', None)


def write_config_language(config_path, language):
    with open(config_path, 'r+') as config_file:
        config_data = json.load(config_file)
        config_data['language'] = language
        config_file.seek(0)
        json.dump(config_data, config_file, indent=4)
        config_file.truncate()


def main():
    # 获取用户选择的功能
    print("What do you want to do with language config?")
    print("1. Read current language config")
    print("2. Write new language config")
    action_choice = int(input("Input your choice (1 or 2):"))
    action = 'read' if action_choice == 1 else 'write' if action_choice == 2 else None
    if action is None:
        print("Invalid input, please input 1 or 2.")
        return

    # 构建路径
    locale_path = 'Locales'
    config_path = os.path.join(locale_path, 'config.json')

    if action == 'read':
        language = read_config_language(config_path)
        if language is not None:
            print(f"\nCurrent language setting is {language}")
        else:
            print("\nFailed to find language setting in config.json")
    elif action == 'write':
        json_files = find_json_files(locale_path)
        if not json_files:
            print("\nFailed to find language config files in the directory")
            return
        print("\nChoose a file to change language config:")
        for i, file in enumerate(json_files, 1):
            print(f"{i}. {file}")
        choice = int(input("Input your choice: "))
        if 1 <= choice <= len(json_files):
            selected_file = json_files[choice - 1]
            language = os.path.splitext(selected_file)[0]
            write_config_language(config_path, language)
            print(f"\n{language} has been set as the new language setting")
        else:
            print("\nInvalid input, please input a valid number.")


if __name__ == "__main__":
    main()
