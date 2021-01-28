from fastapi import FastAPI

app = FastAPI()

@app.route('/test')
def test():
    return 'hello fastapi'