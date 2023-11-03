from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/health')
async def health():
    return {'status': 'ok funciona haciendo push con watchtower1'}