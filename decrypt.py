from time import time


def main():
    print("Введите своё зашифрованное сообщение:")
    encrypted_message = input()

    # Чтение русского словаря из файла
    with open('allruss.txt', 'r', encoding='windows-1251') as allruss:
        rus_dict: set[str] = set(allruss.read().split())

    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    max_matching_words = 0
    best_decrypted_message = ''
    start_time = time()

    total_possible_words = 0
    for shift in range(len(alphabet)):
        total_possible_words += len(encrypted_message.split())

    # Перебор всех возможных сдвигов для дешифрования
    for shift in range(len(alphabet)):
        decrypted_message = decrypt(encrypted_message, shift)
        num_matching_words = count_matching_words(decrypted_message, rus_dict)
        # Проверяем, улучшилось ли количество совпадений
        if num_matching_words > max_matching_words:
            max_matching_words = num_matching_words
            best_decrypted_message = decrypted_message

    end_time: float = time()
    if best_decrypted_message:
        # Выводим лучшее расшифрованное сообщение
        print(f"Расшифрованное слово: {best_decrypted_message}")
        elapsed_time = (end_time - start_time) * 1000  # Преобразуем секунды в миллисекунды
        analyzed_percentage = (max_matching_words / total_possible_words) * 100

        # Запрашиваем дальнейшие действия
        print("Введите -detailed, -new или -break:")
        user_input = input()
        match user_input:
            case "-detailed":
                if total_possible_words == 1:
                    total_possible_words_str = "1 слово"
                else:
                    total_possible_words_str = f"{total_possible_words} слов"

                print(f"Было вычислено за {int(elapsed_time)} миллисекунд")
                print(f"Было проанализировано {analyzed_percentage:.2f}% возможных слов или {total_possible_words_str}")
                print("Используйте -new или -break для дальнейшего пользования")
                next_step = input()

                match next_step:
                    case "-new":
                        print("Начинаем процесс заново")
                        main()
                    case "-break":
                        print("Программа завершена")
                    case _:
                        print("Неверная команда. Программа завершена.")

            case "-new":
                print("Начинаем процесс заново")
                main()

            case "-break":
                print("Программа завершена")

            case _:
                print("Неверная команда. Программа завершена.")
    else:
        print("Не удалось найти подходящие слова")


def decrypt(message: str, shift: int) -> str:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    result = ''

    for char in message:
        if char.lower() in alphabet:
            index = alphabet.index(char.lower())   # Находим индекс символа
            index = (index - shift) % len(alphabet)    # Применяем сдвиг
            result += alphabet[index] if char.islower() else alphabet[index].upper()  # Добавляем символ в результат
        else:
            result += char  # Не алфавитный символ без изменений

    return result


def count_matching_words(message: str, rus_dict: set[str]) -> int:
    words: list[str] = message.split()  # Разбиваем сообщение на слова
    matching_words = 0
    for word in words:
        if is_russian_word(word, rus_dict):   # Сверяем со словарем
            matching_words += 1
    return matching_words


def is_russian_word(word: str, rus_dict: set[str]) -> bool:
    return any(w.strip('.,?!') in rus_dict for w in [word])


main()
