from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import json
import argparse

class WordCloud:
	""" Description of Service """

	def __init__(self, video_id: str):
		self.video_id = video_id

	def get_transcript(self,video_id):
		""" function to get transcripts """
		try:
			output = YouTubeTranscriptApi.get_transcript(video_id)
			segments = []
			for e in output:
				line = e['text']
				line = line.replace('\n', '')
				line = line.replace('>', '')
				line = line.replace('--', '')
				line = line.replace('♪', '')
				segments.append(line)

			transcript = " ".join(segments)
			return transcript
		except:
			print("An exception occurred")
		return(None)

	def word_cloud(self,document):
		""" function to get the word cloud """
		stop_words = stopwords.words('english')
		tokenizer = RegexpTokenizer(r'\w+')
		word_tokens = list(tokenizer.tokenize(document))
		final_tokens = [w for w in word_tokens if not w in stop_words]
		most_frequent = Counter(final_tokens).most_common(40)
		return most_frequent

	def get(self):
		""" main method """
		video_transcript = self.get_transcript(self.video_id)
		video_transcript = video_transcript.lower()
		return self.word_cloud(video_transcript)

		
