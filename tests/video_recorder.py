import wx
import cv2

class VideoRecorder(wx.Frame):
    def __init__(self, parent, title):
        super(VideoRecorder, self).__init__(parent, title=title, size=(400, 400))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.start_button = wx.Button(self.panel, label="Start Recording")
        self.stop_button = wx.Button(self.panel, label="Stop Recording")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_recording)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_recording)
        self.is_recording = False
        self.capture = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None
        self.fps = 20.0
        self.width = 640
        self.height = 480
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.start_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 10)
        self.sizer.Add(self.stop_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 10)
        self.panel.SetSizer(self.sizer)

    def on_start_recording(self, event):
      self.is_recording = True
      # 
      fourcc = cv2.VideoWriter_fourcc(*'MJPG')
      self.out = cv2.VideoWriter('output.avi', fourcc, self.fps, (self.width, self.height))
      while(self.is_recording):
         ret, frame = self.capture.read()
         if ret:
            self.out.write(frame)
         else:
            break
         cv2.imshow('frame', frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    def on_stop_recording(self, event):
        self.is_recording = False
        self.capture.release()
        self.out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = wx.App()
    frame = VideoRecorder(None, "Video Recorder")
    frame.Show()
    app.MainLoop()
