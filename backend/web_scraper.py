from html.parser import HTMLParser


book = []
"""
book = [{
  "heading": "",
  "body:" ""
}]
"""

class MyHTMLParser(HTMLParser):
  current_title = ""
  current_stack = []
  in_chapter = False
  in_heading = False
  in_body = False

  def handle_starttag(self, tag, attrs):
    if tag == "div" and ("class", "chapter") in attrs:
      print("entering new chapter")
      self.in_chapter = True
    elif tag == "h2":
      self.in_heading = True
      print("entering heading")
    elif tag == "p":
      self.in_body = True
      print("entering body")

  def handle_endtag(self, tag):
    if tag == "div" and self.in_chapter:
      print("exiting chapter")
      self.in_chapter = False
      book.append((self.current_title, self.current_stack))
      self.current_title = ""
      self.current_stack = []
    elif tag == "h2":
      self.in_heading = False
      print("exiting heading")
    elif tag == "p":
      self.in_body = False
      print("exiting body")

  def handle_data(self, data):
    # if self.in_chapter: print("Encountered some data  :", data)
    if self.in_chapter:
      if self.in_heading:
        self.current_title += data
      if self.in_body:
        self.current_stack.append(data)
    pass

p = MyHTMLParser()

with open("test.html", "r") as f:
  html = f.read()

p.feed(html)

final = {}
current_book = ""


# def insert_into(target_d, book, chapter, text):
#   if book not in final.keys():
#     final[book] = {}

#   final[book][chapter] = text

# for title, body in book:
#   if "book" in title.lower():
#     current_book = title.replace("\n", " ").split('.')[0]

#     # sometimes, there's an introduction which gets dropped
#     if "body" != []:
#       insert_into(final, current_book, "0", body)
#   else:
#     insert_into(final, current_book, title.replace("\n", " ").split('.')[0], body)