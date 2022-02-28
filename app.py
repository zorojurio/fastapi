from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/blogs")
def blogs(published: bool = True, limit: int = 10, sort: Optional[str] = None):
    print(published)
    data = {
        'blogs': 'these are the blogs',
        'published': published,
        'limit': limit
    }
    if sort is not None:
        data['sort'] = sort
    return data


@app.get('/blogs/published')
def published_blogs():
    return {'published': True}


@app.get("/blogs/{blog_id}")
def detail_blog(blog_id: int):
    return {'id': blog_id}


@app.get('/blogs/{blog_id}/comments')
def comments(blog_id: int, limit=10):
    comments_limit = [x for x in range(limit)]
    data = {
        'blog id': blog_id,
        'comments': comments_limit
    }
    return data


class Blog(BaseModel):
    title: str
    description: str
    published: Optional[bool] = False


@app.post('/create')
def create_blog(blog: Blog):
    print("creating")
    return {"created": True, 'data': blog}


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
