"""
Opens the page for a monster on DnD Beyond, if the filename follows the appropriate structure.
The name of the monster must be enclosed in single quotation marks, and the name must
exactly match the names used in the urls on DnD Beyond.
E.g
'aarakocra'.jpg will open https://www.dndbeyond/monsters/aarakocra
lorem-ipsum-'adult-blue-dragon'-lorem.jpg will open https://www.dndbeyond/monsters/adult-blue-dragon
"""

import webbrowser
import sys

BASE_URL = "https://www.dndbeyond.com/monsters/"

def get_url(filename):
    """
    Returns the appropriate url when supplied with a string that contains the proper
    monster name enclosed in single quotation marks.
    """
    name = filename.split("'")[1]
    return BASE_URL + name

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.argv.pop(0)
        for filename in sys.argv:
            webbrowser.open_new_tab(get_url(filename))
