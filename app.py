# Import all the necessary dependencies

from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize
from langdetect import detect


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/summarize', methods=['GET'])
def summary_api():
 

  url = request.args.get('url', '')  # Get the URL parameter
  language = request.args.get('language', '')  # Get the language parameter
  max_length = int(request.args.get('max_length', 150))  # Default max length if not provided

  print(f"Received URL: {url}, Max Length: {max_length}")

  if '=' in url:
    video_id = url.split('=')[1]
  else:
    # Handle the case where the URL doesn't have an '='
    return "Invalid URL format", 400

  try:

    transcript = get_transcript(video_id)

  except:

    return "No subtitles available for this video", 404



  # Extractive summarization using LSA or Frequency-based method

  if len(transcript.split()) > 3000:

    summary = extractive_summarization(transcript)

  else:

    summary = abstractive_summarization(transcript, max_length)



  return summary, 200



def is_transcript_english(transcript):

  """

  Detect if the transcript is primarily in English.

  

  :param transcript: The transcript text to be analyzed.

  :return: True if the transcript is primarily in English, False otherwise.

  """

  try:

    language = detect(transcript)

    return language == 'en'

  except:

    return False



def get_transcript(video_id):

 
  try:

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    print(transcript_list)
    transcript = ' '.join([d['text'] for d in transcript_list])
    print(transcript)
    return transcript

  except Exception as e:

    raise e



def abstractive_summarization(transcript, max_length):

  """

  Summarizes the given transcript using an abstractive summarization model.

  

  The function employs an NLP pipeline for summarization and applies it to chunks

  of the input transcript. The chunks are processed independently and concatenated

  to form the final summary.

  

  Parameters:

  - transcript (str): The transcript text to be summarized.

  - max_length (int): The maximum length of the summary. It controls how concise

            the summary should be.



  Returns:

  - summary (str): The summarized text.

  """

  summarizer = pipeline('summarization')
  print(summarizer)
  summary = ''

  for i in range(0, (len(transcript) // 1000) + 1):

    summary_text = summarizer(transcript[i * 1000: (i+1) * 1000], max_length=max_length)[0]['summary_text']

    summary = summary + summary_text + ' '
  print("summary",summary)
  return summary



def extractive_summarization(transcript):

  """

  Summarizes the input transcript using the Extractive Summarization technique.

  Latent Semantic Analysis (LSA) is used for dimensionality reduction and the sentences are ranked

  based on their singular values. The top-ranked sentences are selected to form the summary.

  

  Parameters:

  - transcript (str): The transcript text to be summarized.

  

  Returns:

  - summary (str): The summarized text.

  """

  sentences = sent_tokenize(transcript)
  print("sentences",sentences)
  

  # Vectorize sentences

  vectorizer = CountVectorizer(stop_words='english')
  print("vectorizer",vectorizer)
  X = vectorizer.fit_transform(sentences)
  print("X",X)
  

  # Perform Truncated SVD for dimensionality reduction

  svd = TruncatedSVD(n_components=1, random_state=42)

  svd.fit(X)

  components = svd.transform(X)
  print("components",components)
  

  # Rank sentences based on the first singular vector

  ranked_sentences = [item[0] for item in sorted(enumerate(components), key=lambda item: -item[1])]
  print("ranked_sentences",ranked_sentences)
  

  # Select top sentences for summary

  num_sentences = int(0.4 * len(sentences)) # 40% of the original sentences
  print("num_sentences",num_sentences)
  selected_sentences = sorted(ranked_sentences[:num_sentences])
  print("selected_sentences",selected_sentences)
  

  # Compile the final summary

  summary = " ".join([sentences[idx] for idx in selected_sentences])
  print("Finalsummary",summary)
  return summary



if __name__ == '__main__':
    app.run(debug=True)
