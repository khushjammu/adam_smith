import roman
import pickle
from typing import Optional, AbstractSet, Mapping

from .abstract_book import AbstractBook

class WealthOfNations(AbstractBook):
  def __init__(self):
    self.namespace = ""
    self.top_level_field = "book"

    self.books = set(range(6))
    self.num_books = len(self.books)
    
    with open("web_dump", "rb") as f:
      final_dump = pickle.load(f)

    for book, book_vals in final_dump.items():
      for chapter, chapter_vals in book_vals.items():
        final_dump[book][chapter] = [c.strip().replace('\n', ' ') for c in chapter_vals]

    self.full_text = final_dump

  def convert_match_to_text(self, match):
    book_num = int(match['metadata']['book'])
    chapter_num = int(match['metadata']['chapter'])
    paragraph_num = int(match['id'].split(".")[-1])-1

    if book_num == 0:
      # handle intro case:
      return {
        "text": self.full_text[""]["INTRODUCTION AND PLAN OF THE WORK"][paragraph_num],
        "info": "Introduction. Paragraph " + str(paragraph_num + 1) + "."
      }
    else:
      chapter_num_index = 'CHAPTER ' + roman.toRoman(chapter_num) if chapter_num != 0 else str(chapter_num)
      return {
        "text": self.full_text['BOOK ' + roman.toRoman(book_num)][chapter_num_index][paragraph_num],
        "info": "Book " + str(book_num) + ". Chapter " + str(chapter_num) + ". Paragraph " + str(paragraph_num + 1) + "."
      }