import webbrowser

browsers = ["firefox", "chromium", "firefox-esr", "chromium-browser", 'mozilla', 'netscape', 'safari', 'google-chrome', 'chrome', 'galeon', 'epiphany', 'skipstone', 'kfmclient', 'konqueror', 'kfm', 'mosaic', 'opera', 'grail', 'links', 'elinks', 'lynx', 'w3m', 'windows-default', 'macosx', "chromium"]
i = 0

while i < len(browsers):
    browser = browsers[i]
    try:
        installed = webbrowser.get(browser)
        installed.open("http://localhost/")
        break
    except:
        i += 1
        continue

if i == len(browsers):
    print("\n\nPython didn't find your browser. You can access the website manually by entering the following URL in wour web browser: http://localhost/\n\n")