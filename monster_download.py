import time
import datetime
import os

import requests
import bs4

from white_to_transparent import replace_white

BASE_URL = "https://www.dndbeyond.com"

class Monster:
    def __init__(self, img_url, combat_rating, size, environment, name, monster_type):
        self.img_url = img_url
        self.combat_rating = combat_rating
        self.size = size
        self.environment = environment
        self.name = name
        self.monster_type = monster_type

    def make_save_name(self, png=False):
        if png:
            return f"{str(self.combat_rating)}-{self.name}-{self.size}-{self.environment}.png"
        return (
            f"{str(self.combat_rating)}-{self.name}-"
            f"{self.size}-{self.environment}.{self.img_url.split('.')[-1]}"
            )


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"}
unique = 0
non_unique = 0
sub_url = "/monsters" # TODO update to proper url after testing
pages = 1 # starting on page 1, not page 0
session = requests.Session() # session will keep cookies, which is necessary on some sites
invalid = []
start = time.time()

while True:
    res = session.get(BASE_URL + sub_url, headers=headers)
    res.raise_for_status()

    monster_soup = bs4.BeautifulSoup(res.text, "html.parser")

    monsters = monster_soup.select(".info")

    for monster in monsters:

        if not monster.div.a:
            non_unique += 1
            continue
        unique += 1
        cr = monster.find(class_="monster-challenge").span.string.split("/")
        if len(cr) > 1:
            cr = int(cr[0]) / int(cr[1])
        else:
            cr = int(cr[0])
        name = f"'{monster['data-slug']}'"
        size = monster.find(class_="monster-size").span.string
        env = (
            monster.find(class_="monster-environment").span.string
            if monster.find(class_="monster-environment").span else None
        )
        img_url = monster.div.a["href"]
        if not img_url:
            print(f"No valid url found for {name}")
            invalid.append(name)
            continue
        monster_type = monster.find(class_="monster-type").span.string

        mon = Monster(img_url, cr, size, env, name, monster_type)

        image_res = requests.get(img_url)

        if not os.path.isdir(mon.monster_type):
            os.mkdir(mon.monster_type)
        os.chdir(mon.monster_type)

        if not os.path.isdir("originals"):
            os.mkdir("originals")
        os.chdir("originals")

        with open(mon.make_save_name(), "wb") as file:
            for chunk in image_res.iter_content(100000):
                file.write(chunk)
        print(f"{name} downloaded...", flush=True)

        img = replace_white(mon.make_save_name(), 98)
        os.chdir(os.pardir)
        img.save(mon.make_save_name(png=True))
        print(f"{name} made transparent...")

        os.chdir(os.pardir)

    # with open("arkar.html", "wb") as file:
    #     for chunk in res.iter_content(100000):
    #         file.write(chunk)
    print(f"Page {pages} done. Starting next page...", flush=True)
    # TODO remove this after testing
    # if pages >= 1:
    #     break
    if monster_soup.select(".b-pagination-item-next a"):
        sub_url = monster_soup.select(".b-pagination-item-next a")[0].attrs["href"]
    else:
        break
    pages += 1
    time.sleep(1)

end = time.time()

print(f"\nTime elapsed: {str(datetime.timedelta(seconds=round(end - start)))}")
print(f"Unique monsters downloaded: {unique}")
print(f"Skipped monsters (non-unique art): {non_unique}")
print(f"Total pages: {pages}")
if invalid:
    print(f"Unable to find a proper image url for the following monsters:\n{invalid}")
input("All done. Press enter to exit script.")
