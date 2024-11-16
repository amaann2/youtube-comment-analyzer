import os 
import uvicorn
from dotenv import load_dotenv

def server():
    load_dotenv()

    host = str(os.getenv('HOST'))
    port = int(os.getenv('PORT'))

    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    server()
