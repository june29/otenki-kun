from m5stack import lcd
import time, machine, urequests, ujson

lcd.clear()

rtc = machine.RTC()
rtc.ntp_sync(server="ntp.jst.mfeed.ad.jp", tz="JST-9")
while not rtc.synced():
  time.sleep_ms(100)

url = "https://"
counter = 0

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

while True:
  if counter == 1500:
    counter = 0

  if counter == 0:
    render()

  counter += 1
  time.sleep_ms(1000)

  lcd.rect(0, 220, 80, 20, lcd.WHITE, lcd.WHITE)
  lcd.font(lcd.FONT_Default, transparent=True, fixedwidth=False)
  lcd.text(10, 220, "%04d" % (counter), lcd.DARKGREY)
