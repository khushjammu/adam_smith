import roman
import pickle
from typing import Optional, AbstractSet, Mapping

class Book:
  books: AbstractSet[int]
  num_books: int = None #
  full_text: Mapping[str, str]

  def _is_valid_bookNames(self, bookNames):
    # TODO: add validation to ensure bookNames are...valid lmao
    raise NotImplementedError

    if len(bookNames) > self.num_books:
      return (False, "More books supplied than exist.")
    else:
      books_not_found = []
      for book in bookNames:
        if book not in self.books:
          books_not_found.append(book)

      return (False, "Non-existent books supplied: [" + ",".join(books_not_found) + "]")

  def construct_filter(self, bookNames):
    """
    Constructs filter for pinecone query.

    Simple logic to minimise the number of comparisons. If all books, filter excluded. If
    more books removed than included, use $in. Else, use $nin.
    """

    if len(bookNames) == self.num_books:
      return None
    elif len(bookNames) <= self.num_books / 2:
      return {
        "book": {"$in": bookNames}
      }
    else:
      return {
        "book": {"$nin": list(self.books.difference(set(bookNames)))} # do i need to convert to list
      }

  def convert_match_to_text(self, book_num, chapter_num, paragraph_num):
    """
    Converts single match to a source object.
    """

    raise NotImplementedError

class WealthOfNations(Book):
  def __init__(self):
    self.books = set(range(6))
    self.num_books = len(self.books)
    
    with open("web_dump", "rb") as f:
      final_dump = pickle.load(f)

    for book, book_vals in final_dump.items():
      for chapter, chapter_vals in book_vals.items():
        final_dump[book][chapter] = [c.strip().replace('\n', ' ') for c in chapter_vals]

    self.full_text = final_dump

  def convert_match_to_text(self, book_num, chapter_num, paragraph_num):
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
