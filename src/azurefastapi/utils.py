from fastapi import Response

async def processResponse(response: Response):
    response_obj = {}
    response_obj["headers"] = dict(response.headers)
    response_obj["status"] = response.status_code
    response_obj["media_type"] = response.media_type
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    response_obj["body"] = response_body.decode()
    return (response_obj, Response(content=response_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type))

def loadResponse(response_obj):
    return Response(content=response_obj["body"].encode(), status_code=response_obj["status"], 
        headers=response_obj["headers"], media_type=response_obj["media_type"])