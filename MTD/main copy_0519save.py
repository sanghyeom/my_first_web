from fastapi import FastAPI

app = FastAPI()

@app.get("/")
#async def root():
def root():
    return{"messege":"hello"}

@app.get("/home")
def home():
    return{"messege":"home"}

@app.get("/home/{name}")
def read_name(name:str):
    return{'name':name}

@app.get("/home_err/{name}")
def read_name_err(name:int):
    return{'name':name}