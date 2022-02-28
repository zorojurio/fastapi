from fastapi import FastAPI

from blog import schemas

app = FastAPI()


@app.post('/blogs/')
def create(blog: schemas.Blog):
    return blog
