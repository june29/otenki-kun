from m5stack import lcd
import time, machine, urequests, ujson

def render():
  lcd.font(lcd.FONT_Default, transparent=True, fixedwidth=False)
  lcd.text(lcd.RIGHT, 220, "Loading...", lcd.DARKGREY)

  response = urequests.get(url)
  data = ujson.loads(response.text)

  temps = data["temps"]
  rains = data["rains"]
  icon_basename = data["icon_basename"]

  lcd.clear(color=lcd.WHITE)

  lcd.font(lcd.FONT_DejaVu24, transparent=True, fixedwidth=True)
  lcd.text(lcd.CENTER, 20, "%2s [%3s]" % (temps["max"], temps["max_diff"]), lcd.RED)
  lcd.text(lcd.CENTER, 50, "%2s [%3s]" % (temps["min"], temps["min_diff"]), lcd.BLUE)

  lcd.image(110, 85, "/flash/images/%s.jpg" % (icon_basename), 0, lcd.JPG)

  lcd.font(lcd.FONT_DefaultSmall, transparent=True, fixedwidth=True)
  lcd.text(lcd.CENTER, 160, "~06 | ~12 | ~18 | ~24 ", lcd.BLACK)
  lcd.text(lcd.CENTER, 180, "%3s | %3s | %3s | %3s " % (rains["t00_06"], rains["t06_12"], rains["t12_18"], rains["t18_24"]), lcd.BLACK)

  lcd.font(lcd.FONT_Default, transparent=True, fixedwidth=False)
  lcd.text(lcd.CENTER, 220, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), lcd.DARKGREY)

lcd.clear()

rtc = machine.RTC()
rtc.ntp_sync(server="ntp.jst.mfeed.ad.jp", tz="JST-9")
while not rtc.synced():
  time.sleep_ms(100)

url = "https://"

last_updated = None

while True:
  if last_updated is None or buttonC.wasPressed():
    render()
    last_updated = time.time()

  if (last_updated is not None) and ((time.time() - last_updated) > 3600):
    render()
    last_updated = time.time()

  time.sleep_ms(100)
