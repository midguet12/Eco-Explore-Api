from fastapi import FastAPI, HTTPException
from datetime import datetime
app = FastAPI()


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.get('/status')
async def statue():
    return {'fork': 'ok'}
