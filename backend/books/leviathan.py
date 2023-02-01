import roman
import pickle
from typing import Optional, AbstractSet, Mapping

from .abstract_book import AbstractBook

class Leviathan(AbstractBook):
  def __init__(self):
    self.namespace = "leviathan"
    self.top_level_field = "part"

    self.books = set([1,2,3,4])
    self.num_books = len(self.books)
    
    with open("dumps/leviathan", "rb") as f:
      final_dump = pickle.load(f)

    self.full_text = final_dump

  # def construct_filter(self, bookNames):
  #   return None

  def convert_match_to_text(self, match):
    part_num = int(match['metadata']['part'])
    chapter_num = int(match['metadata']['chapter'])
    paragraph_num = int(match['id'].split(".")[-1])-1

    return {
      "text": self.full_text["PART " + roman.toRoman(part_num)]["CHAPTER " + roman.toRoman(chapter_num)][paragraph_num],
      "info": "Part " + str(part_num) + ". Chapter " + str(chapter_num) + ". Paragraph " + str(paragraph_num+1) + "."
    }
    # if book_num == 0:
    #   # handle intro case:
    #   return {
    #     "text": self.full_text["THE INTRODUCTION"][paragraph_num],
    #     "info": "Introduction. Paragraph " + str(paragraph_num + 1) + "."
    #   }
    # else:
    #   chapter_num_index = 'CHAPTER ' + roman.toRoman(chapter_num) if chapter_num != 0 else str(chapter_num)
    #   return {
    #     "text": self.full_text['BOOK ' + roman.toRoman(book_num)][chapter_num_index][paragraph_num],
    #     "info": "Book " + str(book_num) + ". Chapter " + str(chapter_num) + ". Paragraph " + str(paragraph_num + 1) + "."
    #   }


# {'matches': [{'id': '2.29.24',
#               'metadata': {'chapter': 29.0, 'part': 2.0},
#               'score': 0.85506,
#               'sparseValues': {},
#               'values': []},
#              {'id': '2.21.20',
#               'metadata': {'chapter': 21.0, 'part': 2.0},
#               'score': 0.846754432,
#               'sparseValues': {},
#               'values': []},
#              {'id': '2.19.15',
#               'metadata': {'chapter': 19.0, 'part': 2.0},
#               'score': 0.84430778,
#               'sparseValues': {},
#               'values': []}],
#  'namespace': 'leviathan'}