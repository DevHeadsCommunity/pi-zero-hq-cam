import time

from threading import Thread
from picamera2 import Picamera2

class Camera:
  def __init__(self, display, main):
    self.main = main
    self.display = display
    self.picam2 = Picamera2()
    self.small_res_config = self.picam2.create_still_configuration(main={"size": (128, 128)})
    self.full_res_config = self.picam2.create_still_configuration()
    self.picam2.configure(self.small_res_config)
    self.img_base_path = "/home/pi/pi-zero-hq-cam/camera/software/captured-media/"

  def start(self):
    self.picam2.start()

  def change_mode(self, mode):
    if (mode == "full"):
      self.picam2.switch_mode(self.full_res_config)
    else:
      self.picam2.switch_mode(self.small_res_config)

  def live_preview(self):
    self.display.clear_screen()

    while (self.main.live_preview_active):
      if (not self.main.live_preview_pause):
        pil_img = self.picam2.capture_image()
        self.display.display_buffer(pil_img.load())

      # after 10 seconds turn off
      if (time.time() > self.main.live_preview_start + 20 and not self.main.live_preview_pause):
        self.main.live_preview_pause = True
        self.display.clear_screen()
        self.display.draw_text("Camera on")

  def start_live_preview(self):
    Thread(target=self.live_preview).start()

  def take_photo(self):
    img_path = self.img_base_path + str(time.time()).split(".")[0] + ".jpg"
    self.change_mode("full")
    self.picam2.capture_file(img_path)
    self.change_mode("small")
