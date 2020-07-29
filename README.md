# Backend


## Prerequisites
- Docker
- Git

```bash
# Setup
$ https://github.com/YouTubeNLP/Backend.git
$ cd Backend/
$ git switch -c remotes/origin/improvement/new-endpoints-and-cors
```

## Setup

```bash
# Create service container
$ docker build --tag fastapi_ynlp .
$ docker run --detach --name fastapi_backend --publish 80:80 fastapi_ynlp
 ```
## Example

```bash
# Try a post request on the comments endpoint.
# Returns the top k comments for video specified in data.json.
$  curl "http://localhost/score/comments" --request POST --header "Content-Type: application/json" --data @data.json
```

```bash
# Try a post request on the transcript endpoint.
# Returns video transcript for specified video.
$ curl "http://localhost/score/transcripts" --request POST --header "Content-Type: application/json" --data @data.json
```
## API Reference
https://app.swaggerhub.com/apis-docs/youtubenlp/backend/0.0.1
<!-- <table>
	<tr>
		<th>Method</th>
		<th>Status</th>
		<th>Url</th>
		<th>Response</th>
	</tr>
	<tr>
		<td>POST</td>
		<td>201</td>
		<td>http://127.0.0.1:8080/score/comments</td>
		<td>
			
{
	
}	
		</td>
	</tr>
	<tr>
		<td>POST</td>
		<td>201</td>
		<td>http://127.0.0.1:8080/score/transcript</td>
		<td>	
{
	
}	
		</td>
	</tr>
</table> -->
