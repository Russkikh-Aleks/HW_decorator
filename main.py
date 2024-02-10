from datetime import datetime
from functools import wraps
import os
import types


def logger(old_function):

    @wraps(old_function)
    def new_function(*args, **kwargs):
        path = 'main.log'
        result = old_function(*args, **kwargs)
        with open(path, 'a', encoding='utf-8') as file:
            string = f"Функция {new_function.__name__} вызвана {datetime.now()} со следующими аргументами: \
{', '.join([str(el) for el in args])} {', '.join([str(el) for el in kwargs.values()])}. Результат: {result}\n"
            file.write(string)

        return result

    return new_function


def logger_2(path):

    def __logger(old_function):

        @wraps(old_function)
        def new_function(*args, **kwargs):

            nonlocal path
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                string = f"Функция {new_function.__name__} вызвана {datetime.now()} со следующими аргументами: \
{', '.join([str(el) for el in args])} {', '.join([str(el) for el in kwargs.values()])}. Результат: {result}\n"

                file.write(string)

            return result

        return new_function

    return __logger


@logger_2('iter_log.log')
def flat_generator_2(list_of_list):
    for el in list_of_list:
        if isinstance(el, list):
            yield from flat_generator_2(el)
        else:
            yield el


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(
            item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_2(path)
        def hello_world():
            return 'Hello World'

        @logger_2(path)
        def summator(a, b=0):
            return a + b

        @logger_2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(
                item) in log_file_content, f'{item} должен быть записан в файл'


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator_2(list_of_lists_2)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_2(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
