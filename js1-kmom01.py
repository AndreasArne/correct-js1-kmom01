#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Correct javascript1 kmom01 with selenium
"""
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from sys import argv
from time import sleep

user = argv.pop()
LAB = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/kmom01/lab1/answer.html".format(user=user)
SANDBOX = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/kmom01/sandbox/".format(user=user)
REDOVISA = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/redovisa/".format(user=user)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def close_tab():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

def open_tab(href):
    ff.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    ff.get(href)

def find_links(names, links):
    res_links = {}
    print(bcolors.HEADER + "Find links ", "\n----------", bcolors.ENDC)
    # try:
    for name in names:
        for l in links:
            href = l.get_attribute("href")
            if name in href:
                print(bcolors.UNDERLINE + "Found :", name, bcolors.ENDC)
                print(bcolors.BOLD, href, bcolors.ENDC)
                res_links[name] = href if name in ("jsfiddle", "codepen") else l
    # except exceptions.StaleElementReferenceException:
        # pass
    return res_links

def check_lab(ff):
    try:
        pass_span = ff.find_element_by_class_name("pass")
        print(bcolors.OKGREEN, pass_span.text, bcolors.ENDC)
    except exceptions.NoSuchElementException:
        pass_span = ff.find_element_by_class_name("passdistinct")
        try:
            print(bcolors.OKGREEN, pass_span.text, bcolors.ENDC)
        except:
            print(bcolors.FAIL, pass_span.text, bcolors.ENDC)

def check_unicorn(ff, links):
    link = links["unicorn"]
    if link:
        link.click()
        try:
            pass_unicorn = ff.find_element_by_class_name("invalid")
            sleep(4)
            print(bcolors.FAIL + "Unicorn does not Validate!", bcolors.ENDC)
        except exceptions.NoSuchElementException:
            try:
                pass_unicorn = ff.find_element_by_class_name("valid")
                print(bcolors.OKGREEN + "Unicorn Validates!", bcolors.ENDC)
            except exceptions.NoSuchElementException:
                print(bcolors.WARNING, "Länken till unicorn är troligen fel. Inget validerades, rätt länk är: http://validator.w3.org/unicorn/check?ucn_uri=referer&ucn_task=conformance")

        sleep(2)
        ff.execute_script("window.history.go(-1)")

def check_fiddle(ff, links):
    try:
        link = links["jsfiddle"]
    except KeyError:
        try:
            link = links["codepen"]
        except:
            link = False
    if link:
        ff.get(link)
        sleep(2)
        print(bcolors.OKGREEN + "Found jsfiddle/codepen!", bcolors.ENDC)
        if link in ("https://jsfiddle.net", "https://jsfiddle.net/", "http://jsfiddle.net", "jsfiddle.net"):
            print(bcolors.WARNING + "Link not personal!", bcolors.ENDC)
        ff.execute_script("window.history.go(-1)")


def check_sandbox(ff):
    links = ff.find_elements_by_tag_name("a")
    links_to_find = ("unicorn", "jsfiddle", "codepen", "validator.w3.org/check", "jigsaw.w3")
    links = find_links(links_to_find, links)
    if len(links) == 4:
        print(bcolors.OKGREEN + "Found all 4 links", bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Missing link!", bcolors.ENDC)
        print("Following links shoud exist: ", links_to_find)
        print("JSfiddle or codepen, both isn't needed.")

    check_unicorn(ff, links)
    check_fiddle(ff, links)

def check_redovisa(ff):
    ff.get(REDOVISA + "me.html")
    sleep(2)
    ff.get(REDOVISA + "redovisning.html")
    sleep(1.5)
    ff.get(REDOVISA + "om.html")
    sleep(1.5)
    if "github.com" in ff.page_source or "Github.com" in ff.page_source:
        print(bcolors.OKGREEN +"Has github link", bcolors.ENDC)
        try:
            links = ff.find_elements_by_tag_name("a")
            links = find_links(("github", "Github", "GitHub"), links)
            key = [k for k in links.keys()][0]
            links[key].click()
            sleep(1)
        except exceptions.NoSuchElementException:
            print(bcolors.OKBLUE, "Github is not a clickable link", bcolors.ENDC)



ff = webdriver.Firefox()
ff.get(LAB)
check_lab(ff)

ff.get(SANDBOX)
sleep(2)
check_sandbox(ff)

check_redovisa(ff)

ff.quit()
