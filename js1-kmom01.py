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
from result import Result

user = argv.pop()
LAB = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/kmom01/lab1/answer.html".format(user=user)
SANDBOX = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/kmom01/sandbox/".format(user=user)
REDOVISA = "http://www.student.bth.se/~{user}/dbwebb-kurser/javascript1/me/redovisa/".format(user=user)
result = Result()

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
    print(bcolors.BOLD, "Find links ", bcolors.ENDC)
    # try:
    for name in names:
        for l in links:
            href = l.get_attribute("href")
            if name in href:
                print("Found :", name)
                print(href)
                res_links[name] = href if name in ("jsfiddle", "codepen") else l
    # except exceptions.StaleElementReferenceException:
        # pass
    return res_links

def check_lab(ff):
    try:
        pass_span = ff.find_element_by_class_name("pass")
        print(bcolors.OKGREEN, pass_span.text, bcolors.ENDC)
        result.lab = "Labben är godkänd."
    except exceptions.NoSuchElementException:
        try:
            pass_span = ff.find_element_by_class_name("passdistinct")
            result.lab = "Bra jobbat med extra uppgifterna i labben."
            print(bcolors.OKGREEN, pass_span.text, bcolors.ENDC)
        except:
            sleep(4)
            result.lab  = "Labben är inte godkänd, kompletera den."
            print(bcolors.FAIL, "Lab is not done!", bcolors.ENDC)

def check_unicorn(ff, links):
    
    if "unicorn" in links:
        link = links["unicorn"]
        link.click()
        try:
            pass_unicorn = ff.find_element_by_class_name("invalid")
            sleep(4)
            print(bcolors.FAIL, "Unicorn does not Validate!", bcolors.ENDC)
            result.unicorn = "Unicorn validerar inte."
        except exceptions.NoSuchElementException:
            try:
                pass_unicorn = ff.find_element_by_class_name("valid")
                result.unicorn = "Unicorn validerar."
                print(bcolors.OKGREEN, "Unicorn Validates!", bcolors.ENDC)
            except exceptions.NoSuchElementException:
                result.unicorn = "Du har fel länk till Unicorn, det ska vara http://validator.w3.org/unicorn/check?ucn_uri=referer&ucn_task=conformance."
                print(bcolors.WARNING, "Länken till unicorn är troligen fel. Inget validerades, rätt länk är: http://validator.w3.org/unicorn/check?ucn_uri=referer&ucn_task=conformance")

        sleep(2)
        ff.execute_script("window.history.go(-1)")
    else:
            print(bcolors.FAIL, "Missing unicorn link!", bcolors.ENDC)
            result.unicorn = "Du har ingen länk till Unicorn, det ska vara http://validator.w3.org/unicorn/check?ucn_uri=referer&ucn_task=conformance."



def check_fiddle(ff, links):
    try:
        link = links["jsfiddle"]
    except KeyError:
        try:
            link = links["codepen"]
        except:
            link = False
            result.jsfiddle += "Du har ingen länk till jsfiddle/codepen. "
    if link:
        ff.get(link)
        sleep(2)
        print(bcolors.OKGREEN, "Found jsfiddle/codepen!", bcolors.ENDC)
        if link in ("https://jsfiddle.net", "https://jsfiddle.net/", "http://jsfiddle.net", "jsfiddle.net"):
            print(bcolors.WARNING, "Link not personal!", bcolors.ENDC)
        elif link in ("https://codepen.io", "https://codepen.io/", "http://codepen.io", "codepen.io"):
            print(bcolors.WARNING, "Link not personal!", bcolors.ENDC)

        ff.execute_script("window.history.go(-1)")


def check_sandbox(ff):
    links = ff.find_elements_by_tag_name("a")
    links_to_find = ("unicorn", "jsfiddle", "codepen", "validator.w3.org/check", "jigsaw.w3")
    links = find_links(links_to_find, links)
    if len(links) >= 4:
        result.links = "Alla länkar finns på sandbox sidan."
        print(bcolors.OKGREEN, "Found all 4 links", bcolors.ENDC)
    else:
        print(bcolors.FAIL, "Missing link(s)!", bcolors.ENDC)
        print("Following links shoud exist: ", links_to_find)
        print("JSfiddle or codepen, both isn't needed.")
        result.links = "Du saknar länkar på sandbox sidan."

    check_unicorn(ff, links)
    check_fiddle(ff, links)

def check_if_page_loaded(text, page):
    if "The requested URL /~{user}/dbwebb-kurser/javascript1/me/redovisa/{page} was not found on this server.".format(user=user, page=page) in text:
        print(bcolors.FAIL, "File", page, "is missing!", bcolors.ENDC)
        result.redovisa.append("Sidan {} finns inte under redovisa.".format(page))


def check_redovisa(ff):
    ff.get(REDOVISA + "me.html")
    check_if_page_loaded(ff.page_source, "me.html")
    sleep(2)
    ff.get(REDOVISA + "redovisning.html")
    check_if_page_loaded(ff.page_source, "redovisning.html")
    sleep(1.5)
    ff.get(REDOVISA + "om.html")
    check_if_page_loaded(ff.page_source, "om.html")
    sleep(1.5)
    if "github.com" in ff.page_source or "Github.com" in ff.page_source:
        print(bcolors.OKGREEN, "Has github link", bcolors.ENDC)
        try:
            links = ff.find_elements_by_tag_name("a")
            links = find_links(("github", "Github", "GitHub"), links)
            key = [k for k in links.keys()][0]
            links[key].click()
            sleep(1)
        except exceptions.NoSuchElementException:
            print(bcolors.OKBLUE, "Github is not a clickable link", bcolors.ENDC)
    else:
        print(bcolors.FAIL, "Github link is missing!", bcolors.ENDC)
        result.github = "Du har inte någon länk till kursens github sida i om.html."


ff = webdriver.Firefox()

print(bcolors.HEADER, "Test lab", bcolors.ENDC)
ff.get(LAB)
check_lab(ff)

print(bcolors.HEADER, "Test Sandbox", bcolors.ENDC)
ff.get(SANDBOX)
sleep(2)
check_sandbox(ff)

print(bcolors.HEADER, "Test me-sida", bcolors.ENDC)
check_redovisa(ff)

ff.quit()

result.copy_text()
print("\nSammanfattning av bedömning")
print("=========================")
print(result)
print("=========================")
print("Texen är 'kopierad' till clipboard.")
print(bcolors.WARNING + "SVARA INTE DIREKT MED TEXTEN! FIXA TILL DEN SÅ DEN VEKLIGEN STÄMMER!", bcolors.ENDC)
