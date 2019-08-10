# -*- Coding: utf-8 -*-

from const import MEMBERS, MEMBERS_EN

class RepositoryParser:
    def __init__(self):
        self.authors = []
        self.joint_works = []
        self.authorID = 0
        self.main_author_id = -1
        self.co_author_id = -1
        self.isSkipMode = False
        self.title = ""

    # Get author list from HTML
    def get_author_list(self, soup):
        titleElem = soup.find("h1")
        self.title = titleElem.get_text()
        # print(self.title)
        divElem = titleElem.parent
        a_list = divElem.find_all("a")
        
        return a_list

    # Convert crawled full name into firstname
    def get_firstname_from_hashmap(self, _author):
        ret_author = None

        if _author in MEMBERS.keys():
            ret_author = MEMBERS[_author]
        elif _author in MEMBERS_EN.keys():
            ret_author = MEMBERS_EN[_author]

        return ret_author

    # When scraping information of main author, update self.main_author_id
    # When not doing, update self.co_author_id
    def update_author_id(self, _is_main_author, _author_id):
        if _is_main_author:
            self.main_author_id = _author_id
        else:
            self.co_author_id = _author_id

    def print_info(self, _i, _is_main_author):
        if self.authors[_i]["id"] == 4:
            if _is_main_author:
                print("Nino main " + str(self.authors[_i]["r"]) + " : " + self.title)
            else:
                print("Nino co " + str(self.authors[_i]["stroke_width"]) + " : " + self.title)

    # Scrape information of an author add it into self.authors
    def add_author(self, _elem_author, _is_main_author):
        author_name = _elem_author.get_text(" ", strip=True)
        author_name = self.get_firstname_from_hashmap(author_name)
        author_id = -1;
        self.isSkipMode = False

        if author_name == None:
            self.isSkipMode = True
            return

        for i in range(len(self.authors)):
            if author_name in self.authors[i].values():
                if _is_main_author:
                    self.authors[i]["r"] += 1
                else:
                    self.authors[i]["stroke_width"] += 1

                #### fix bug ####
                self.print_info(i, _is_main_author)
                
                self.update_author_id(_is_main_author, self.authors[i]["id"])
                return

        self.update_author_id(_is_main_author, self.authorID)

        # Add a new element of author
        # print("主著か共著かで(r=1, s=0)なのか(r=0, s=1)なのかが違う。これは_is_main_authorで決めればOK")

        author_obj = {
            "id": self.authorID, 
            "label": author_name,
            "r": 1 if _is_main_author else 0,
            "stroke_width": 0 if _is_main_author else 1
        }
        self.authors.append(author_obj)
        self.authorID += 1

    # Scrape infomation of authors and add them into authors list
    def add_authors_and_edges(self, _soup):
        categoryElem = _soup.find(class_ = "type_1A0-N")
        if categoryElem.get_text() == "学位論文":
            return

        author_list = self.get_author_list(_soup)

        self.add_author(author_list[0], True)
        if self.isSkipMode:
            return

        for i in range(1, len(author_list)):
            self.add_author(author_list[i], False);
            if self.isSkipMode:
                return

            self.add_edge()

    # Add a edge between main author and co author
    def add_edge(self):
        # print(str(self.co_author_id) +"-->"+ str(self.main_author_id))

        for i in range(len(self.joint_works)):
            values = list(self.joint_works[i].values())

            if (self.main_author_id == values[0] and self.co_author_id == values[1]) or (self.main_author_id == values[1] and self.co_author_id == values[0]):
                self.joint_works[i]["weight"] += 1
                return

        # Add a new element of edge
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