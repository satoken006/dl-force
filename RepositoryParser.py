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

    # Scrape infomation of authors and add them into authors list
    def add_authors_and_edges(self, _soup):
        categoryElem = _soup.find(class_ = "type_1A0-N")
        if categoryElem.get_text() == "学位論文":
            return

        date_elems = _soup.find_all(class_ = "halfwidth_1OaB1")
        titleElem = _soup.find("h1")
        author_list = titleElem.parent.find_all("a")
        # title = titleElem.get_text()

        self.add_author(author_list[0], titleElem, True)
        if self.isSkipMode:
            return

        for i in range(1, len(author_list)):
            self.add_author(author_list[i], titleElem, False);
            if self.isSkipMode:
                return

            self.add_edge(date_elems, titleElem)

    # Scrape information of an author add it into self.authors
    def add_author(self, _elem_author, _elem_title, _is_main_author):
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

                self.update_author_id(_is_main_author, self.authors[i]["id"])
                return

        self.update_author_id(_is_main_author, self.authorID)

        # Add a new element of author
        author_obj = {
            "id": self.authorID, 
            "label": author_name,
            "r": 1 if _is_main_author else 0,
            "stroke_width": 0 if _is_main_author else 1
        }
        self.authors.append(author_obj)
        self.authorID += 1

    # Add a edge between main author and co author
    def add_edge(self, _date_elems, _titleElem):
        print("        " + str(self.co_author_id) + "-->" + str(self.main_author_id))
        title = _titleElem.get_text()
        date = ""

        for date_elem in _date_elems:
            p_elems = date_elem.find_all("p")
            if p_elems[0].get_text() == "Date of issue":
                date = p_elems[1].get_text()
                # print("日付を検出: " + date)
                break


        for i in range(len(self.joint_works)):
            values = list(self.joint_works[i].values())

            if (self.main_author_id == values[0] and self.co_author_id == values[1]) or (self.main_author_id == values[1] and self.co_author_id == values[0]):
                self.joint_works[i]["weight"] += 1
                self.joint_works[i]["papers"].append({
                    "date": date,
                    "title": title
                })
                return

        # Add a new element of edge
        joint_work = {
            "source": self.co_author_id,
            "target": self.main_author_id,
            "weight": 1,
            "papers": [
                {
                    "date": date,
                    "title": title
                }
            ]
        }
        self.joint_works.append(joint_work)



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

    # Get result of parsing
    def getResult(self):
        return {
            "nodes": self.authors,
            "links": self.joint_works
        }