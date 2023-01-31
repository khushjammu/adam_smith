from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

import os
import roman
import pickle
import pinecone
import openai
from openai.embeddings_utils import get_embedding, distances_from_embeddings, indices_of_nearest_neighbors_from_distances

import books.wealth_of_nations

w = books.wealth_of_nations.WealthOfNations()

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
  query = request.args.get("query")
  bookNames = eval(request.args.get("books"))

  if query is None or query == '':
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

  query_embedding = get_embedding(query, engine='text-embedding-ada-002')
  filter_dict = w.construct_filter(bookNames)

  nearest = index.query(
      vector=query_embedding,
      filter=filter_dict,
      top_k=3,
      include_metadata=True
  )

  sources = [] # {"text": "", "info": Chapter x}

  for match in nearest['matches']:
    book_num = int(match['metadata']['book'])
    chapter_num = int(match['metadata']['chapter'])
    paragraph_num = int(match['id'].split(".")[-1])-1

    sources.append(w.convert_match_to_text(book_num, chapter_num, paragraph_num))

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
