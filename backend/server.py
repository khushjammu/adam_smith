from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

import os
import roman
import pickle
import pinecone
import openai
from openai.embeddings_utils import get_embedding, distances_from_embeddings, indices_of_nearest_neighbors_from_distances

import books.wealth_of_nations
import books.leviathan

BOOK_INDEX = {
  "wealth_of_nations": books.wealth_of_nations.WealthOfNations(),
  "leviathan": books.leviathan.Leviathan()
}

# w = books.wealth_of_nations.WealthOfNations()

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ['OPENAI_API_KEY']

pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment="us-west1-gcp")
index = pinecone.Index("adam-smith")

prompt = """Using the following text from Adam Smith's Wealth of Nations, answer the following question. If the answer is not contained within the text, say "I don't know." Keep in mind that not all of the text will be relevant to your answers.

Text:
\"\"\"
*text*
\"\"\"

First, identify the relevant parts of the text. Then, answer the question: "*question*" Remember that the question might apply to synonyms in the text.

Answer:"""

@app.route("/test")
def test():
  response = openai.Completion.create(
    model='text-davinci-002',
    prompt='1,2,3,',
    max_tokens=50,
    temperature=0,
    stream=True,  # this time, we set stream=True
  )

  def event_stream(generator):
    for event in generator:
      yield event.choices[0].text

  return Response(event_stream(response), mimetype="text/event-stream")

@app.route("/")
def adam_smith():
  book = request.args.get("book")
  query = request.args.get("query")
  bookNames = eval(request.args.get("books"))

  if book is None or book == '':
    return {
      'status': 1,
      'error': 'no_book',
      'msg': '`book` not supplied'
    }
  elif book not in BOOK_INDEX.keys():
    return {
      'status': 1,
      'error': 'invalid_book',
      'msg': '`book` does not exist'
    }
  elif query is None or query == '':
    return {
      'status': 1,
      'error': 'no_query',
      'msg': '`query` not supplied'
    }
  elif bookNames is None or bookNames == '' or bookNames == []:
    return {
      'status': 1,
      'error': 'no_books',
      'msg': '`books` not supplied'
    }

  w = BOOK_INDEX[book]

  query_embedding = get_embedding(query, engine='text-embedding-ada-002')
  filter_dict = w.construct_filter(bookNames)
  nearest = index.query(
      vector=query_embedding,
      filter=filter_dict,
      top_k=3,
      include_metadata=True,
      namespace=w.namespace
  )
  print("nearest", nearest)

  sources = [] # {"text": "", "info": Chapter x}

  for match in nearest['matches']:
    sources.append(w.convert_match_to_text(match))

  body_text = '\n'.join([a['text'] for a in sources])

  resp = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt.replace('*text*', body_text).replace('*question*', query),
    max_tokens=256,
    temperature=0.0
  )

  return {
    'status': 0,
    'answer': resp['choices'][0]['text'].strip(' '),
    'sources': sources
  }


if __name__ == '__main__':
  app.run(debug=True)
