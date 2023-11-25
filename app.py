import random
import uvicorn
import prometheus_client
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

heads_count = prometheus_client.Counter(
    "heads_count",
    "Number of heads"
)

tails_count = prometheus_client.Counter(
    "tails_count",
    "Number of tails"
)

flips_count = prometheus_client.Counter(
    "flips_count",
    "Number of flips"
)

@app.get("/")
def get_home():
    return {"api_version": "1.0"}

# Total = 100
# Heads = 40 (1 => True)
# Tail = 60 (0 => False)

@app.get("/flip_coin")
async def flip_coin(flip_times: int = None):
    if not flip_times:
        raise HTTPException(
            status_code=422,
            detail="flip_times cannot be None, must provide a Number"
        )
    
    heads = 0
    for _ in range(flip_times):
        if random.randint(0,1):
            heads += 1

    # Subtract Heads count from Total Flips and remainings are Tail Count
    tails = flip_times - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flips_count.inc(flip_times)

    return {
        "heads_count": heads,
        "tails_count": tails,
        }

@app.get("/metrics")
def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain"
    )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1010)