from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from hospital.app.hospitals.api import router as hospitals_router


app = FastAPI()
app.include_router(hospitals_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8082, reload=True)