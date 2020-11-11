from pathlib import Path
from google.cloud import vision
import re
p = Path(__file__).parent / 'picture7.jpg'
client = vision.ImageAnnotatorClient()
with p.open('rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content) 
response = client.text_detection(image=image)


def measure():
  for i, text in enumerate(response.text_annotations):
    if text.description == "合計" or text.description == "合":
      WordUpperHeight = text.bounding_poly.vertices[0].y
      WordLowerHeight = text.bounding_poly.vertices[3].y
      WordHeight = (WordUpperHeight + WordLowerHeight) / 2
      return(WordHeight)


KeyWordHeight = measure()
print(KeyWordHeight)
for i, text in enumerate(response.text_annotations):
    if text.description[0] == "¥":
      TargetLowerHeight = text.bounding_poly.vertices[3].y
      if TargetLowerHeight >= KeyWordHeight:
        n = text.description
        if n[-1] == ",":
            print("四桁以上")
            num = n + response.text_annotations[i+1].description
            result = re.sub('[^0-9]','', num)
            print("加工前" + num)
            print("加工後"+ result)
        else:
            result = re.sub('[^0-9]','', n)
            print("加工前" + n)
            print("加工後"+ result)
        break

    elif text.description[0] =="￥" or text.description[0] =="羊" or text.description[0] =="半" or text.description[0] =="ギ":
      TargetLowerHeight = text.bounding_poly.vertices[3].y
      if TargetLowerHeight >= KeyWordHeight:
        n = response.text_annotations[i+1].description
        if n[-1] == ",":
            print("四桁以上")
            num = n + response.text_annotations[i+2].description
            result = re.sub('[^0-9]','', num)
            print("加工前" + num)
            print("加工後"+ result)
        else:
            result = re.sub('[^0-9]','', n)
            print("加工前" + n)
            print("加工後"+ result)
        break
    
    

    