# -*- Coding: utf-8 -*-

from const import MEMBERS, MEMBERS_EN

class RepositoryParser:
    def __init__(self):
        print()

    # Get author list from HTML
    def get_author_list(self, soup):
        titleElem = soup.find("h1")
        title = titleElem.get_text()
        print(title)
        divElem = titleElem.parent
        a_list = divElem.find_all("a")
        
        return a_list

    def get_nickname_from_hashmap(self, _author):
        ret_author = None

        if _author in MEMBERS.keys():
            ret_author = MEMBERS[_author]
        elif _author in MEMBERS_EN.keys():
            ret_author = MEMBERS_EN[_author]

        return ret_author

    def append_edge(self, _soup, _list):
        author_list = self.get_author_list(_soup)
        main_author = author_list[0].get_text(" ", strip=True)
        main_author = self.get_nickname_from_hashmap(main_author)

        if main_author == None:
            return

        for i in range(1, len(author_list)):
            co_author = author_list[i].get_text(" ", strip=True)
            co_author = self.get_nickname_from_hashmap(co_author)

            if co_author == None or co_author == "PDF":
                return

            print(co_author + " --> " + main_author)
            _list.append([co_author, main_author])
