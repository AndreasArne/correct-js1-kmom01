What it does
==================
1. Goes to the students lab1 page and tries to find if it has passed or not.
2. Goes to their sanbox page and looks for all links.
3. Goes to unicorn to see if it validates.
4. If a jsfiddle or codepen link was found goes the the site.
5. Visits the students me.html/redovisning.html/om.html pages.
6. Looks for github link in om.html and goes clicks the link.

Install instructions
=====================

Download https://github.com/mozilla/geckodriver/releases, extract where you want it and make sure the folder you put it in is in your **path**.
You need to have Firefox installed and install modules in requirements.txt. Ex. `python3 -m pip install -r requirements.txt`.

Run the Script
==========================
1. From `corr.sh`, run as `./corr.sh <course> <kmom> <akronym>`. It will run potatoe, validate and python script.
2. Script directly, `python3 js1-kmom01.py <akronym>`. Only corrects their turn in. Does not validate.