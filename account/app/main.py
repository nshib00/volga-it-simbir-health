from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from account.app.users.api import router as users_router
from account.app.auth.api import router as auth_router


app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8081, reload=True)