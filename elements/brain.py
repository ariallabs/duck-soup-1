
import openai
import os
import tempfile
import subprocess

#from transformers import pipeline

class NLP_opeanai:
    def __init__(self, name, openaikey):
        self.name = name
        self._log_in(openaikey)
    
    def _log_in(self, openai_key):
        try:
          openai.api_key = openai_key
        except:
          ValueError("Invalid OpenAI API key")
    
    def _get_response(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")
    
    def summarize(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        prompt = f"Summarize this: {prompt}"
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")

    def generate_text(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        prompt = f"{prompt}"
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")

    def answer_question(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")

    def create_transcript(self, video_path):
      with tempfile.TemporaryDirectory() as tmpdir:
          # use ffmpeg to extract the audio stream from the video file
          audio_path = os.path.join(tmpdir, 'audio.wav')
          cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path]
          subprocess.check_call(cmd)

          # use OpenAI API to transcribe the audio stream and get the transcript
          transcript = openai.Audio.transcribe("whisper-1", open(audio_path, "rb"))

      return transcript['text']

