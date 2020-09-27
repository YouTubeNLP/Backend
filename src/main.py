import sys

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from googleapiclient.discovery import build

from v1.service import Comment, Transcript, Video, Ner, WordCloud , Sentiment
from settings import settings

app = FastAPI()

origins = [
    "https://youtubenlp.com",
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

yt_api_config = build(
    serviceName="youtube", version="v3", developerKey=settings.api_key
)


class VideoException(Exception):
    """ Handles exceptions for invalid video_id """

    def __init__(self, video_id: str):
        self.video_id = video_id


@app.exception_handler(VideoException)
async def video_exception_handler(request: Request, exc: VideoException):
    return JSONResponse(
        status_code=400,
        content={"status": 400, "error": f"{exc.video_id} is an invalid video url"},
    )


@app.get("/video/{video_id}")
async def video_details(video_id: str):
    video = Video(yt_api_config, video_id)
    try:
        details = jsonable_encoder(video.get_details())
    except:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=details)


@app.get("/video/{video_id}/description")
async def video_description(video_id: str):
    video = Video(yt_api_config, video_id)
    try:
        description = jsonable_encoder(video.get_description())
    except:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=description)


@app.get("/video/{video_id}/keywords")
async def video_keywords(video_id: str):
    video = Video(yt_api_config, video_id)
    try:
        keywords = jsonable_encoder(video.get_keywords())
    except:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=keywords)


@app.get("/transcripts/{video_id}")
async def transcripts(video_id: str):
    transcript = Transcript(video_id)
    transcripts = jsonable_encoder(transcript.get_list())
    # wrong video_url is handled by get_list
    if transcripts is None:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=transcripts)


@app.get("/sentiments/{video_id}/score")
async def sentiments(video_id: str):
    pass

@app.get("/sentiments/{video_id}/{number_max_comments_for_analysis}")
async def sentiments_details(video_id: str,number_max_comments_for_analysis: int):
    sentiments = Sentiment(video_id,number_max_comments_for_analysis,yt_api_config)
    sentiment = jsonable_encoder(sentiments.get())
    if sentiment is None:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=sentiment)



@app.get("/comments/{video_id}/controversial")
async def controversial(video_id: str):
    pass


@app.get("/comments/{video_id}")
async def comments(video_id: str):
    comment = Comment(yt_api_config, video_id)
    comments = jsonable_encoder(comment.get_all_comments())

    if comments is None:
        raise VideoException(video_id=video_id)

    return JSONResponse(content=comments)


@app.get("/emotions/{video_id}/score")
async def emotions(video_id: str):
    pass


@app.get("/ner/{video_id}")
async def ner(video_id: str):
    video_ner = Ner(video_id)
    try:
        ners = {"video_id": video_id, "entity": []}
        ners_list = video_ner.get_ner()
        label_list = []
        j = 1
        for (_, label) in ners_list:
            Available = False
            for i in range(len(label_list)):
                if label == label_list[i]:
                    Available = True
                    break
            if not Available:
                label_list.append(label)
                ners["entity"].append({"label" + str(j): label, "text": []})
                j = j + 1
        for (text, label) in ners_list:
            label_num = 0
            for k in range(len(label_list)):
                if label_list[k] == label:
                    label_num = k + 1
                    break
            text_Available = False
            for a in range(len(ners["entity"][label_num - 1]["text"])):
                if text == ners["entity"][label_num - 1]["text"][a]:
                    text_Available = True
                    break
            if not text_Available:
                ners["entity"][label_num - 1]["text"].append(text)

    except:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=ners)


@app.get("/ner/{video_id}/targeted")
async def ner_targeted(video_id: str):
    pass


@app.get("/lda/{video_id}")
async def lda(video_id: str):
    pass


@app.get("/word-cloud/{video_id}")
async def wordcloud(video_id: str):
    wc = WordCloud(video_id)
    try:
        data = {"video_id": video_id, "cloud": []}
        word_list = wc.get()
        for (word, frequency) in word_list:
            data["cloud"].append({"word": word, "frequency": frequency})
    except:
        raise VideoException(video_id=video_id)
    return JSONResponse(content=data)


@app.get("/")
async def root(request: Request):
    """
    Returns an object with live endpoints details.

    To quickly look into the current live services from backend.

    Q. We already have /docs, /redoc, README.md and the swagger spec. So why is this required?
    A. /docs, /redoc, README.md and swagger spec contains the 'mock' spec and won't tell the
       services which are live at the moment.
    """
    base_url = request.url
    return {
        "api_specification": {
            "prod": {
                "description": "Returns generated Specification",
                "endpoint": [f"{base_url}docs", f"{base_url}redoc"],
            },
            "dev": {
                "description": "Returns standard API reference",
                "endpoint": "https://app.swaggerhub.com/apis-docs/youtubenlp/backend/0.0.1",
            },
        },
        "transcript_service": {
            "description": "Returns list of transcripts from video",
            "endpoint": f"{base_url}transcripts/{{video_id}}",
        },
        "comment_service": {
            "description": "Returns list of comments from video",
            "endpoint": f"{base_url}comments/{{video_id}}?q={{k_top_comments}}",
        },
        "video_service": {
            "description": "Returns various video information",
            "details": {
                "description": "Returns various details related to video",
                "endpoint": f"{base_url}video/{{video_id}}",
            },
            "description": {
                "description": "Returns the description text of the video",
                "endpoint": f"{base_url}video/{{video_id}}{{/description}}",
            },
            "keywords": {
                "description": "Returns a list of keywords related to video",
                "endpoint": f"{base_url}video/{{video_id}}{{/keywords}}",
            },
            "Ner_service": {
                "description": "Returns name entity recognition  (NER) (also known as entity identification, entity chunking and entity extraction)",
                "endpoint": f"{base_url}ner/{{video_id}}",
            },
            "Word-Cloud": {
                "description": "Return Words frequency",
                "endpoint": f"{base_url}word-cloud/{{video_id}}",
            },
	        "Comment-Sentiment-Analysis": {
                "description": "Return comment sentiments analysis",
                "endpoint": f"{base_url}sentiment/{{video_id}}{{/number_of_comments_for_analysis}}",
            },
        },
    }
