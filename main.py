import requests
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request

app = FastAPI()

@app.get("/my-first-api")
def hello(name = None):
    if name is None:
        text = 'Hello!'
    else:
        text = 'Hello ' + name + '!'
    return text

@app.get("/get-iris")
def get_iris():
    import pandas as pd
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)
    return iris
  
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request



@app.get("/plot-iris")
async def plot_iris(request: Request):
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)

    plt.scatter(iris['sepal_length'], iris['sepal_width'])
    plt.savefig('iris.png')
    plt.close()

    file_path = 'iris.png'
    return StreamingResponse(open(file_path, 'rb'), media_type="image/png")




#main.py abrir en terminal integrado para ir la carpeta

#uvicorn main:app --reload ejecutar en la terminal
#http://127.0.0.1:8000/my-first-api
#http://127.0.0.1:8000/my-first-api?name=edu
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/get-iris
#http://127.0.0.1:8000/plot-iris








