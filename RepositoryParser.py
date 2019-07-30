# -*- Coding: utf-8 -*-

from const import MEMBERS, MEMBERS_EN

class RepositoryParser:
    def __init__(self):
        self.authorID = 0
        self.authors = []
        self.joint_works = []

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

    def append_edge(self, _soup):
        author_list = self.get_author_list(_soup)
        main_author = author_list[0].get_text(" ", strip=True)
        main_author = self.get_nickname_from_hashmap(main_author)
        main_author_id = -1;

        if main_author == None:
            return

        author_exists = False

        for i in range(len(self.authors)):
            if main_author in self.authors[i].values():
                self.authors[i]["r"] += 1
                main_author_id = self.authors[i]["id"]
                author_exists = True
                break

        if not author_exists:
            author = {
                "id": self.authorID, 
                "label": main_author,
                "r": 1
            }
            self.authors.append(author)
            self.authorID += 1

        for i in range(1, len(author_list)):
            co_author = author_list[i].get_text(" ", strip=True)
            co_author = self.get_nickname_from_hashmap(main_author)
            co_author_id = -1;

            if  co_author == None:
                return

            co_author_exists = False

            for i in range(len(self.authors)):
                if co_author in self.authors[i].values():
                    # self.authors[i]["r"] += 1
                    co_author_id = self.authors[i]["id"]
                    co_author_exists = True
                    break

            if not co_author_exists:
                co_author = {
                    "id": self.authorID, 
                    "label": co_author,
                    "r": 1
                }
                self.authors.append(co_author)
                self.authorID += 1

        # for i in range(1, len(author_list)):
        #     co_author = author_list[i].get_text(" ", strip=True)
        #     co_author = self.get_nickname_from_hashmap(co_author)
        #     co_author_id = -1

        #     if co_author == None or co_author == "PDF":
        #         return

        #     for i in range(len(self.authors)):
        #         if co_author in self.authors[i].values():
        #             co_author_id = self.authors[i]["id"]

        #     print(co_author + " --> " + main_author)

        #     joint_works_exists = False

        #     for i in range(len(self.joint_works)):
        #         values = list(self.joint_works[i].values())

        #         if (main_author_id == values[0] and co_author_id == values[1]) or (main_author_id == values[1] and co_author_id == values[0]):
        #             # weight + 1 to current LINK
        #             self.joint_works[i]["weight"] += 1
        #             joint_works_exists = True
        #             break

        #     if not joint_works_exists:
        #         # add new element LINK
        #         joint_work = {
        #             "source": co_author_id,
        #             "target": main_author_id,
        #             "weight": 1
        #         }
        #         self.joint_works.append(joint_work)

        #     print(self.authors)
        #     print(self.joint_works)

    # Get result of parsing
    def getResult(self):
        resultJSON = {
            "nodes": self.authors,
            "links": self.joint_works
        }

        return resultJSON

