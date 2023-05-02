import openai
import os

import subprocess
import tempfile
import pyaudio

class Video_Transcriptor:
   def __init__(self, openai_k):
      openai.api_key = openai_k

   def create_transcript(self, video_path):
      with tempfile.TemporaryDirectory() as tmpdir:
          # use ffmpeg to extract the audio stream from the video file
          audio_path = os.path.join(tmpdir, 'audio.wav')
          cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path]
          subprocess.check_call(cmd)

          # use OpenAI API to transcribe the audio stream and get the transcript
          transcript = openai.Audio.transcribe("whisper-1", open(audio_path, "rb"))

      return transcript['text']


def get_transcript():
   
   transcript = v.create_transcript(video_path)
   return transcript

import wx
video_path = 'movie.mov'
openai_k = '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'
v = Video_Transcriptor(openai_k)
app = wx.App()

frame = wx.Frame(None, title="Transcript", size=(500, 500))
panel = wx.Panel(frame)

text = wx.TextCtrl(panel, pos=(3, 3), size=(490, 490), style=wx.TE_MULTILINE)
text.SetValue(get_transcript())

frame.Show()
if __name__ == "__main__":
   app.MainLoop()
