from typing import Optional, AbstractSet, Mapping

class AbstractBook:
  books: AbstractSet[int]
  num_books: int = None #
  full_text: Mapping[str, str]
  namespace: str
  top_level_field: str # This would be "book" for Wealth of Nations, "part" for Leviathan etc

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
        self.top_level_field: {"$in": bookNames}
      }
    else:
      return {
        self.top_level_field: {"$nin": list(self.books.difference(set(bookNames)))} # do i need to convert to list
      }

  def convert_match_to_text(self, match: Mapping):
    raise NotImplementedError