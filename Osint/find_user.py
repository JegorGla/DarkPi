import asyncio
import aiohttp
import customtkinter as ctk

# Варианты формирования юзернейма
def generate_username_variants(username):
    base = username.lower().strip()
    parts = base.split(' ')
    variants = set()
    if len(parts) == 1:
        variants.add(base)
    else:
        # пример: john doe -> john.doe, john_doe, johndoe, john-doe, jdoe
        variants.add(''.join(parts))                 # johndoe
        variants.add('.'.join(parts))                # john.doe
        variants.add('_'.join(parts))                # john_doe
        variants.add('-'.join(parts))                # john-doe
        variants.add(parts[0][0] + parts[1])         # jdoe
        variants.add(parts[0] + parts[1][0])         # johnd
    return variants

URLS = [
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

NOT_FOUND_MARKERS = [
    'not found', 'page does not exist', 'profile not found', "цей контент наразі недоступний",
    'this page isn\'t available', '404', 'user not found',
    'sorry, this page isn’t available', 'we can’t find that page',
    "this account may have been banned or the username is incorrect.",
    "sorry", "this page is no longer available"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/114.0.0.0 Safari/537.36"
}

async def check_profile(session, url, text_box):
    try:
        async with session.get(url, timeout=10) as response:
            text = await response.text()
            if response.status == 200:
                lower_text = text.lower()
                if any(marker in lower_text for marker in NOT_FOUND_MARKERS):
                    return None
                else:
                    text_box.insert("end", f"[+] Found: {url}\n")
                    return url
            elif response.status == 404:
                return None
            else:
                text_box.insert("end", f"[?] {url} returned status {response.status}\n")
                return None
    except Exception as e:
        text_box.insert("end", f"[!] Error: {url} -> {e}\n")
        return None

async def user_find(username, text_box):
    variants = generate_username_variants(username)
    found_profiles = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = []
        for variant in variants:
            for site in URLS:
                url = site.format(variant)
                tasks.append(check_profile(session, url, text_box))
        results = await asyncio.gather(*tasks)
    
    for res in results:
        if res:
            found_profiles.append(res)

    text_box.insert("end", f"SEARCH ENDED: found {len(found_profiles)} profiles\n")

# Вызов из синхронного кода CustomTkinter
def run_search(username, text_box):
    asyncio.run(user_find(username, text_box))