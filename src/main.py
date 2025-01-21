from fastapi import FastAPI, HTTPException, Depends, Request, Response, status
from pydantic import BaseModel
from decouple import config
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import JSONResponse
import helpers
from helpers.ratelimiting import lifespan as my_ratelimit_lifespan

REDIS_URL = config("REDIS_URL")
API_KEY_HEADER = "X-API-key"
API_ACCESS_KEY = config("API_ACCESS_KEY")

app = FastAPI(lifespan=my_ratelimit_lifespan)

@app.middleware("http")
async def custom_api_key_middleware(request:Request, call_next):
    request_key_header = request.headers.get(API_ACCESS_KEY)
    if f'{request_key_header}' != API_ACCESS_KEY:
        return JSONResponse(status_code=403, content={"detail":"Invalid key, try again."})
    response = await call_next(request)
    return response

class ImageGenerationRequest(BaseModel):
    prompt: str

@app.post('/generate', 
          dependencies=[
              Depends(RateLimiter(times=2, seconds=5)),
              Depends(RateLimiter(times=10, minutes=1))
              ])
def create_image(data: ImageGenerationRequest):
    try:
        pred_result = helpers.generate_image(data.prompt)
        return {pred_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/predictions', dependencies=[Depends(RateLimiter(times=1000, seconds=20))])
def list_prediction_view():
    results = helpers.list_prediction_results()
    return results