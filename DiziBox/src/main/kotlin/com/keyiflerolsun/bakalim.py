# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli       import konsol
from cloudscraper    import CloudScraper
from parsel          import Selector
from re              import search
from Kekik.Sifreleme import CryptoJS

oturum = CloudScraper()
istek  = oturum.get("https://yabancidizi.tv/dizi/dandadan/sezon-1/bolum-1")
secici = Selector(istek.text)

iframe = secici.css("div#video-area iframe::attr(src)").get()
iframe = iframe.replace("king.php?v=", "king.php?wmode=opaque&v=")

# oturum.cookies.update({
#     "LockUser"      : "true",
#     "isTrustedUser" : "true",
#     "dbxu"          : "1722403730363"
# })
oturum.headers.update({"Referer": "https://yabancidizi.tv/dizi/dandadan/sezon-1/bolum-1"})
istek  = oturum.get(iframe)
secici = Selector(istek.text)
iframe = secici.css("div#Player iframe::attr(src)").get()

oturum.headers.update({"Referer": "https://yabancidizi.tv/"})
istek     = oturum.get(iframe)
cryptData = search(r"CryptoJS\.AES\.decrypt\(\"(.*)\",\"", istek.text).group(1)
cryptPass = search(r"\",\"(.*)\"\);", istek.text).group(1)

decrypted = CryptoJS.decrypt(cryptPass, cryptData)
konsol.print(search(r"file: \'(.*)',", decrypted).group(1))
