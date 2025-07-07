import os
import time
from bottle import Bottle,get, post, request,static_file,route, run
from paddleocr import PaddleOCR, draw_ocr

app = Bottle()

prePath="/ocr"

@app.route(prePath+'/hello')
def hello():
    return "Hello World!"

@app.get(prePath+'/')
def ocrRecognition():
    return '''
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pure/2.0.3/pure-min.css" crossorigin="anonymous" />
    <title>OCR识别测试</title>
  </head>
  <body style="padding:10px ">
    <div class="pure-g">
        <form class="pure-form pure-form-aligned"  action="/ocr/ocrRecognitionImg" method="post" enctype="multipart/form-data">
             <div class="pure-control-group">
                <label for="aligned-name">图片</label>
                <input name="file" id="file" type="file" />
                <span class="pure-form-message-inline">选择要上传的图片</span>
            </div>
            <div class="pure-controls">
                <p>图片不要太大，最好在3M以下</p> 
                <input value="识别" class="pure-button pure-button-primary" type="submit" />
            </div>
        </form>
    </div>    
  </body>
</html>      
    '''

@app.post(prePath+'/ocrRecognitionImg') 
def do_ocrRecognitionImg():

   file     = request.files.get('file')
     
   name1, ext1 = os.path.splitext(file.filename)
     
   if ext1 not in ('.png','.jpg','.jpeg'):  return 'File extension not allowed.'
     
   ticks = str(time.time()).replace(",","")

   save_path1="/tmp/"+"ocr_pic1_"+ticks+ext1

   resultFileName="ocr_pic1_"+ticks+"_result"+ext1

   file.save(save_path1)

   # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
   # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
   ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
   #img_path = './imgs/11.jpg'

   result = ocr.ocr(save_path1, cls=True)
   for idx in range(len(result)):
      res = result[idx]
      for line in res:
          print(line)

   # 显示结果
   from PIL import Image
   result = result[0]
   image = Image.open(save_path1).convert('RGB')
   boxes = [line[0] for line in result]
   txts = [line[1][0] for line in result]
   scores = [line[1][1] for line in result]
   im_show = draw_ocr(image, boxes, txts, scores)
   im_show = Image.fromarray(im_show)
   im_show.save("/tmp/"+resultFileName)

   return static_file(resultFileName,root="/tmp")

@app.post(prePath+'/ocrRecognition') 
def do_ocrRecognition():

   file     = request.files.get('file')
     
   name1, ext1 = os.path.splitext(file.filename)
     
   if ext1 not in ('.png','.jpg','.jpeg'):  return 'File extension not allowed.'
     
   ticks = str(time.time()).replace(",","")

   save_path1="/tmp/"+"ocr_pic1_"+ticks+ext1

   file.save(save_path1)

   # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
   # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
   ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

   result = ocr.ocr(save_path1, cls=True)
   
   for idx in range(len(result)):
      res = result[idx]
      for line in res:
          print(line)

   return {"result":result}


@route(prePath+'/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/path/to/your/static/files')


run(app, host='0.0.0.0', port=8080)