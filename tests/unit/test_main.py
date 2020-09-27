from fastapi.testclient import TestClient
import json
import base64
import sys

try:
    sys.path.insert(1, "src/")
except:
    print("Python path can't be set")
from main import app

client = TestClient(app)


def test_root():
    res = open("tests/unit/test_response/root_response.txt", "r").read().strip()
    response = client.get("/")
    assert response.status_code == 200
    assert base64.b64encode(res.encode()) == base64.b64encode(response.content)


def test_keywords():
    response = client.get("/video/2DG3pMcNNlw/keywords")
    assert response.status_code == 200


def test_description():
    res = open("tests/unit/test_response/video_description.txt", "r").read().strip()
    response = client.get("/video/2DG3pMcNNlw/description")
    assert response.status_code == 200
    assert base64.b64encode(res.encode()) == base64.b64encode(response.content)


def test_transcript():
    response = client.get("/transcripts/1ylleTbizgU")
    assert response.status_code == 200


def test_video_details():
    res = open("tests/unit/test_response/video_details.txt", "r").read().strip()
    res_json = json.loads(res)
    response = client.get("/video/2DG3pMcNNlw")
    assert response.status_code == 200
    flag = True
    json_response = response.json()
    for keys, keys_from_file in zip(json_response, res_json):
        if keys == "meta":
            continue
        if keys != keys_from_file or json_response[keys] != res_json[keys_from_file]:
            flag = False
    assert flag


def test_wordcloud():
    response = client.get("/word-cloud/SLsTskih7_I")
    assert response.status_code == 200


def test_sentiments_details():
    response = client.get("/sentiments/2DG3pMcNNlw/20")
    assert response.status_code == 200


def test_comment():
    response = client.get("/comments/2DG3pMcNNlw")
    assert response.status_code == 200


def test_controversial():
    response = client.get("/comments/2DG3pMcNNlw/controversial")
    assert response.status_code == 200


def test_emotions():
    response = client.get("/emotions/2DG3pMcNNlw/score")
    assert response.status_code == 200


def test_lda():
    response = client.get("/lda/2DG3pMcNNlw")
    assert response.status_code == 200


def test_ner():
    response = client.get("/ner/RqcjBLMaWCg")
    res = open("tests/unit/test_response/ner_test.txt", "r").read().strip()
    assert response.status_code == 200
    assert base64.b64encode(res.encode()) == base64.b64encode(response.content)


def test_ner_targeted():
    response = client.get("/ner/2DG3pMcNNlw/targeted")
    assert response.status_code == 200


def test_sentiments_score():
    response = client.get("/sentiments/2DG3pMcNNlw/score")
    assert response.status_code == 200
