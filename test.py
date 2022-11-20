from functools import wraps

import requests
from requests.api import get, options, head, post, put, patch, delete
import click
import json
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time: .4f} seconds')
        return result

    return timeit_wrapper


http_methods = (get, options, head, post, put, patch, delete)


def ask_for_input():
    answer = input('choose for input, filename (f) or keyboard (k): ')
    if answer == 'f':
        return open_file()
    elif answer == 'k':
        return ask_urls()
    if answer != 'f' or answer != 'k':
        return ask_for_input()


@timeit
def open_file():
    filename = input('Input path to filename: ')
    while True:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                urls = [line.strip() for line in file]
                return urls
        except:
            filename = input('Erorr, input correct path: ')


def ask_urls():
    list_urls = []
    answer = input('write a url in format (https://urlname): ')
    while answer != 'stop':
        list_urls.append(answer)
        answer = input('write a url or "stop" for ending input: ')
    return list_urls


# print(ask_for_input())

@timeit
def check_urls():
    list_urls = ask_for_input()
    valid_urls = []
    for index in range(len(list_urls)):
        try:
            requests.get(list_urls[index])
            valid_urls.append(list_urls[index])
        except:
            print(f'{index + 1} строка {list_urls[index]} не является ссылкой')
    return valid_urls


@click.command()
@timeit
def check_methods_urls(list_methods=http_methods):
    """
    This script checks url methods dict with methods and status codes
    """
    new_list_urls = check_urls()
    print('In process...')
    data = {
        str(urll): {
            method.__name__.upper():
                method(urll).status_code for method in list_methods if method(urll).status_code != 405}
        for urll in new_list_urls}
    with open('result.json', "w") as result:
        json.dump(data, result, indent=4)
    with open('result.json', "r") as read:
        result_data = json.load(read)
    print(result_data)

@click.command()
@timeit
def check_methods_new(new_list_urls=check_urls()):
    """
       This script checks url methods dict with methods and status codes
       """
    resultnew = {}
    print('In process...')
    for url in new_list_urls:
        res_get = requests.get(url).status_code
        res_post = requests.post(url).status_code
        res_put = requests.put(url).status_code
        res_delete = requests.delete(url).status_code
        res_patch = requests.patch(url).status_code
        res_options = requests.options(url).status_code
        res_head = requests.head(url).status_code
        data = {
            'GET': res_get, 'POST': res_post, 'PUT': res_put, 'DELETE': res_delete, 'PATCH': res_patch,
            'OPTIONS': res_options, 'HEAD': res_head
        }
        resultnew[url] = data
    data = {url: {method: code for method, code in methods.items() if code != 405} for url, methods in resultnew.items()}
    with open('result.json', "w") as result:
        json.dump(data, result, indent=4)
    with open('result.json', "r") as read:
        result_data = json.load(read)
    print(result_data)




#
#
if __name__ == '__main__':
    # check_methods_urls()
    check_methods_new()
