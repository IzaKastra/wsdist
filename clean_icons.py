import numpy as np
import os

# Download missing icons, remove unused icons.


data = np.loadtxt("item_list.txt", unpack=True, delimiter=";",dtype=str)

# Delete icons that aren't being used
existing = [k for k in os.listdir("icons32/") if ".png" in k]
for k in existing:
  if k.split(".")[0] not in data[0]:
    if k != "65536.png":
#      print(f"Deleting useless image: icons32/{k}")
      os.remove(f"icons32/{k}")

# Download missing icons from https://static.ffxiah.com/images/icon/{k}
import urllib.request

existing = [k for k in os.listdir("icons32/") if ".png" in k]
for i,k in enumerate(data[0]):
  if k+".png" not in existing:
    url = f"https://static.ffxiah.com/images/icon/{k}.png"
    imgname = f"icons32/{k}.png"
    print(f"Downloading {k}.png ({data[1][i]})")
    urllib.request.urlretrieve(url,imgname)
