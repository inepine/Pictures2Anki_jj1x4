from fastapi import FastAPI
import one_jpg

app = FastAPI()

# 获取anki同步请求
@app.get("/anki_sync")
async def anki_sync():
    print("Remote Anki_Sync Get J!!!!")
    one_jpg.process_all_onedrive_pictures()
    return {"message": "GET request received"}

# 获取qa anki同步请求
@app.get("/anki_sync_qa")
async def anki_sync_qa():
    print("Remote Anki_Sync Get Qa!!!!")
    return {"message": "GET request received"}

# 如果是程序执行的文件，则运行uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
