import sys
from fastapi import FastAPI,Request,Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.comment import get_comments
from service.transcript import get_transcripts
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
	videoID: str
	kTopComments: int

@app.get('/score/transcripts/{video_id}')
def transcripts(video_id: str):
	transcript_list = jsonable_encoder(get_transcripts(video_id))
	return JSONResponse(content=transcript_list)

@app.get('/score/comments/{video_id}/{kTopComments}')
def comments(video_id: str,kTopComments: int):
	comments_list = get_comments(video_id, kTopComments)
	return JSONResponse(content=comments_list)
@app.get("/video/{video_id}")
def basic_info(video_id: str):
	print(video_id)
	return "response: thumbnails, title, channel name, view, time"
@app.get("/video/{video_id}/description")
def description(video_id: str):
	print(video_id)
	return "descriptions"
@app.get("/video/{video_id}/keywords")
def keywords(video_id: str):
	print(video_id)
	return "Keywords"
