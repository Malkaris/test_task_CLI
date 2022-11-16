import requests
from requests.api import get, options, head, post, put, patch, delete
import click
import json


http_methods = (get, options, head, post, put, patch, delete)


def open_file(filename=input('Enter filename: ')):
    with open(filename, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]
        return urls


def check_urls(list_urls=None):
    if list_urls is None:
        list_urls = open_file('urls.txt')
    valid_urls = []
    for index in range(len(list_urls)):
        try:
            requests.get(list_urls[index])
            valid_urls.append(list_urls[index])
        except:
            print(f'{index + 1} строка {list_urls[index]} не является ссылкой')
    return valid_urls


@click.command()
def check_methods_urls(new_list_urls=None, list_methods=http_methods):
    """
    This script checks url methods dict with methods and status codes
    """
    if new_list_urls is None:
        new_list_urls = check_urls()
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


if __name__ == '__main__':
    check_methods_urls()
