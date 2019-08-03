# -*- Coding: utf-8 -*-

from const import MEMBERS, MEMBERS_EN

class RepositoryParser:
    def __init__(self):
        self.authorID = 0
        self.authors = []
        self.joint_works = []

        self.main_author_id = -1;
        self.co_author_id = -1;

        self.isSkipMode = False

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

    def add_author(self, _elem_author, _is_main_author):
        author_name = _elem_author.get_text(" ", strip=True)
        author_name = self.get_nickname_from_hashmap(author_name)
        author_id = -1;
        author_exists = False
        self.isSkipMode = False

        if author_name == None:
            self.isSkipMode = True
            return

        for i in range(len(self.authors)):
            if author_name in self.authors[i].values():
                if _is_main_author:
                    self.authors[i]["r"] += 1
                
                if _is_main_author:
                    self.main_author_id = self.authors[i]["id"]
                else:
                    self.co_author_id = self.authors[i]["id"]

                author_exists = True
                break

        if not author_exists:
            if _is_main_author:
                self.main_author_id = self.authorID
            else:
                self.co_author_id = self.authorID

            author_obj = {
                "id": self.authorID, 
                "label": author_name,
                "r": 1
            }
            self.authors.append(author_obj)
            self.authorID += 1

    # TODO: rename function
    # TODO: split into several functions
    ### functionalize the part of "adding an author"
    def append_edge(self, _soup):
        author_list = self.get_author_list(_soup)

        self.add_author(author_list[0], True)

        if self.isSkipMode:
            return

        # print("author list:")
        # print(author_list)

        for i in range(1, len(author_list)):
            self.add_author(author_list[i], False);

            if self.isSkipMode:
                return

            print(str(self.co_author_id) +"-->"+ str(self.main_author_id))

            ### add a edge between main author and co_author ###
            joint_works_exists = False

            for i in range(len(self.joint_works)):
                values = list(self.joint_works[i].values())

                if (self.main_author_id == values[0] and self.co_author_id == values[1]) or (self.main_author_id == values[1] and self.co_author_id == values[0]):
                    # weight +1 at current LINK
                    self.joint_works[i]["weight"] += 1
                    joint_works_exists = True
                    break

            if not joint_works_exists:
                # add new element LINK
                joint_work = {
                    "source": self.co_author_id,
                    "target": self.main_author_id,
                    "weight": 1
                }
                self.joint_works.append(joint_work)

    # Get result of parsing
    def getResult(self):
        return {
            "nodes": self.authors,
            "links": self.joint_works
        }