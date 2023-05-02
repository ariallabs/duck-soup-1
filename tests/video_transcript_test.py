import wx
import wx.media
import os

import sqlite3
import whisper

class Video_Transcriptor:
   def __init__(self):
      self.model = whisper.load_model("base", device="cpu", in_memory=True)

   def create_transcript(self, video_path):
      result = self.model.transcribe(video_path)
      text = result["text"]
      return text

class MyFrame(wx.Frame):
   def __init__(self):
      super().__init__(parent=None, title='Read .mov files')
      panel = wx.Panel(self)
      self.video_transcriptor = Video_Transcriptor()

      # Create a text control to display the selected folder
      self.folder_text = wx.TextCtrl(panel, value='', style=wx.TE_READONLY)

      # Create a button to select the folder
      select_folder_button = wx.Button(panel, label='Select Folder')
      select_folder_button.Bind(wx.EVT_BUTTON, self.on_select_folder)

      # Create a list control to display the .mov files in the folder
      self.file_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
      self.file_list.InsertColumn(0, 'File Name')
      self.file_list.InsertColumn(1, 'File Path')
      self.file_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_select_file)

      # Create a media player to display the selected video
      self.media_player = wx.media.MediaCtrl(panel, style=wx.SIMPLE_BORDER)
      self.media_player.Bind(wx.media.EVT_MEDIA_LOADED, self.on_media_loaded)

      # create a textarea to display the transcript multiple lines and editable
      self.transcript_text = wx.TextCtrl(panel, value='', style=wx.TE_MULTILINE)
      self.transcript_text.Bind(wx.EVT_TEXT, self.on_change_text)

      # Create buttons to control the media player
      self.play_button = wx.Button(panel, label='Play')
      self.play_button.Disable()
      self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
      self.pause_button = wx.Button(panel, label='Pause')
      self.pause_button.Disable()
      self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
      self.stop_button = wx.Button(panel, label='Stop')
      self.stop_button.Disable()
      self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)

      # add a save button for the transcript
      self.save_button = wx.Button(panel, label='Save')
      self.save_button.Disable()
      self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

      # create a transcript button
      self.transcript_button = wx.Button(panel, label='Transcript')
      self.transcript_button.Disable()
      self.transcript_button.Bind(wx.EVT_BUTTON, self.on_transcript)

      self.timer = wx.Timer(self)
      self.timer.Start(100)

      # create a top sizer
      top_sizer = wx.BoxSizer(wx.VERTICAL)
      # in the top sizer add a horizontal sizer
      h_sizer = wx.BoxSizer(wx.HORIZONTAL)
      # inside put the self.folder_text and the select_folder_button without overlapping
      h_sizer.Add(self.folder_text, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
      h_sizer.Add(select_folder_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
      # add the horizontal sizer to the top sizer
      top_sizer.Add(h_sizer, flag=wx.EXPAND|wx.ALL, border=10)
      # add another bottom sizer
      bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
      # inside put the self.trasn and the self.media_player
      bottom_sizer.Add(self.transcript_text, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
      bottom_sizer.Add(self.media_player, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
      # add the bottom sizer to the top sizer
      top_sizer.Add(bottom_sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
      # add another horizontal sizer
      h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
      # inside put the self.play_button, self.pause_button, self.stop_button
      h_sizer2.Add(self.play_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
      h_sizer2.Add(self.pause_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

      h_sizer2.Add(self.stop_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
      top_sizer.Add(h_sizer2, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
      top_sizer.Add(self.file_list, flag=wx.EXPAND|wx.ALL, border=10)
      top_sizer.Add(self.save_button, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
      # set the top sizer to the panel
      panel.SetSizer(top_sizer)

   def on_transcript(self, event):
      self.transcript_text_value = self.video_transcriptor.create_transcript(self.video_path)
      self.transcript_text.SetValue(self.transcript_text_value)

   #  UI CONTROLS
   def on_select_folder(self, event):
      # Show a directory dialog to select a folder
      with wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE) as dlg:
         if dlg.ShowModal() == wx.ID_OK:
               # Update the text control with the selected folder
               selected_folder = dlg.GetPath()
               self.folder_text.SetValue(selected_folder)

               # Clear the list control and add the .mov files in the folder
               self.file_list.DeleteAllItems()
               for filename in os.listdir(selected_folder):
                  if filename.endswith('.mov'):
                     filepath = os.path.join(selected_folder, filename)
                     self.file_list.Append((filename, filepath))

   def on_select_file(self, event):
      # Get the selected file path from the list control
      selected_file = self.file_list.GetItemText(event.GetIndex(), 1)
      print('selecting file: ',selected_file)
      # enable the transcript button
      self.transcript_button.Enable()
      self.video_path = selected_file

      # Load the selected video into the media player
      self.media_player.Load(selected_file)
      self.media_player.Play()
      self.on_media_loaded(event)
      try:
         conn = sqlite3.connect('database.db')
         c = conn.cursor()
      except:
         # create the database
         conn = sqlite3.connect('database.db')
         c = conn.cursor()
         c.execute('''CREATE TABLE videos
                  (video_path text, transcript text)''')
         conn.commit()

      # get the transcript from the database
      if c.execute("SELECT transcript FROM videos WHERE video_path = ?", (selected_file,)):
         try:
            transcript = c.fetchone()[0]
            print('transcript found : ', transcript)
            self.transcript_text_value = transcript
         except:
            self.transcript_text_value = 'No transcript found'
      else:
         self.transcript_text_value = 'No transcript found'


      self.transcript_text.SetValue(self.transcript_text_value)
      conn.close()

   def on_media_loaded(self, event):
      # Enable the control buttons
      self.play_button.Enable()
      self.pause_button.Enable()
      self.stop_button.Enable()
      self.save_button.Enable()
      # now you can set the initial size of the media player
      self.media_player.SetInitialSize()
      # and set the size of the frame to the size of the video
      self.SetSize(self.media_player.GetSize())
      self.Center()
      # and start playing the video
      self.media_player.Play()
      
   def on_play(self, event):
      # Play the video
      self.media_player.Play()
      self.media_player.SetInitialSize()
      self.timer.Start(100)
      # and set the size of the frame to the size of the video
      self.SetSize(self.media_player.GetSize())

   def on_pause(self, event):
      # Pause the video
      self.media_player.Pause()

   def on_stop(self, event):
      # Stop the video
      self.media_player.Stop()
      self.timer.Stop()

   def on_save(self, event):
      # this function update the transcript in the database
      conn = sqlite3.connect('database.db')
      c = conn.cursor()

      # if the file already exist in the database
      file = c.execute("SELECT video_path FROM videos WHERE video_path = ?", (self.video_path,))
      if file.fetchone() is None:
         # insert the transcript and the video path in the database
         c.execute("INSERT INTO videos VALUES (?, ?)", (self.video_path, self.transcript_text_value))
      else:
         # update the transcript
         c.execute("UPDATE videos SET transcript = ? WHERE video_path = ?", (self.transcript_text_value, self.video_path))
      conn.commit()
      conn.close()
      print('transcript saved')
      print('video path : ', self.video_path)
      print('transcript : ', self.transcript_text_value)
   
   def on_change_text(self, event):
      self.transcript_text_value = self.transcript_text.GetValue()

if __name__ == '__main__':
   app = wx.App()
   frame = MyFrame()
   frame.Show()
   app.MainLoop()

