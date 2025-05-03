import customtkinter as ctk
import requests

def user_find(username, text_box):
    urls = [
        "https://twitter.com/{}",
        "https://facebook.com/{}",
        "https://instagram.com/{}",
        "https://tiktok.com/@{}",
        "https://youtube.com/@{}",
        "https://linkedin.com/in/{}",
        "https://github.com/{}",
        "https://reddit.com/user/{}",
        "https://pinterest.com/{}",
        "https://snapchat.com/add/{}",
        "https://soundcloud.com/{}",
        "https://medium.com/@{}",
        "https://dribbble.com/{}",
        "https://behance.net/{}",
        "https://vk.com/{}",
        "https://ok.ru/{}",
        "https://tumblr.com/{}",
        "https://twitch.tv/{}",
        "https://mix.com/{}",
        "https://flickr.com/people/{}",
        "https://vimeo.com/{}",
        "https://badoo.com/profile/{}",
        "https://imgur.com/user/{}",
        "https://tripadvisor.com/Profile/{}",
        "https://disqus.com/by/{}",
        "https://ask.fm/{}",
        "https://myspace.com/{}",
        "https://weheartit.com/{}",
        "https://houzz.com/user/{}",
        "https://slideshare.net/{}",
        "https://deviantart.com/{}",
        "https://bitbucket.org/{}",
        "https://replit.com/@{}",
        "https://pastebin.com/u/{}",
        "https://about.me/{}",
        "https://angel.co/u/{}",
        "https://500px.com/p/{}",
        "https://kongregate.com/accounts/{}",
        "https://steamcommunity.com/id/{}",
        "https://roblox.com/user.aspx?username={}",
        "https://forum.freecodecamp.org/u/{}",
        "https://open.spotify.com/user/{}",
        "https://last.fm/user/{}",
        "https://stackoverflow.com/users/{}",
        "https://keybase.io/{}",
        "https://patreon.com/{}",
        "https://coinmarketcap.com/users/{}",
        "https://leetcode.com/{}",
        "https://hub.docker.com/u/{}"
    ]

    for idx, site in enumerate(urls):
        url = site.format(username)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                text_box.insert("end", f"[+] Found: {url}\n")
            elif response.status_code == 404:
                pass  # Можно пропустить, если не нужно выводить not found
            else:
                text_box.insert("end", f"[?] {url} returned status {response.status_code}\n")
        except Exception as e:
            text_box.insert("end", f"[!] Error: {url} -> {e}\n")

        # Когда цикл доходит до последнего элемента списка, выводим сообщение "SEARCH ENDED"
        if idx == len(urls) - 1:
            text_box.insert("end", "SEARCH ENDED\n")
