from fastapi import FastAPI, HTTPException
from datetime import datetime
app = FastAPI()


@app.get('/health')
async def health():
    return {'status': 'ok ya funciona con watchtower'}


@app.get('/status')
async def statue():
    return {'fork': 'ok'}
