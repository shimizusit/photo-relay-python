from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import uvicorn
import asyncio
import json
import base64
from datetime import datetime
from PIL import Image
import io
import logging
from typing import Dict, Set

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Photo Relay Service")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンに制限すべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket接続を追跡するための集合
connected_clients: Set[WebSocket] = set()

async def broadcast_image(image_data: bytes, metadata: Dict):
    """
    全ての接続済みクライアントに画像データをブロードキャストする
    """
    if not connected_clients:
        logger.warning("No connected clients to broadcast to")
        return

    # base64エンコードされた画像データを含むメッセージを作成
    message = {
        "imageData": base64.b64encode(image_data).decode('utf-8'),
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata
    }
    
    # 全クライアントにメッセージを送信
    disconnected_clients = set()
    for client in connected_clients:
        try:
            await client.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send to client: {e}")
            disconnected_clients.add(client)
    
    # 切断されたクライアントを除去
    connected_clients.difference_update(disconnected_clients)

@app.post("/upload/")
async def upload_photo(image: UploadFile, description: str = None):
    """
    画像をアップロードし、背景を除去して、WebSocketクライアントにブロードキャストする
    """
    try:
        start_time = datetime.utcnow()
        
        # 画像を読み込み
        content = await image.read()
        input_image = Image.open(io.BytesIO(content))
        
        # 背景除去を実行
        output_image = remove(input_image)
        
        # 処理済み画像をバイトストリームに変換
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        processed_image_data = output_buffer.getvalue()
        
        # 処理時間を計算
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # メタデータを作成
        metadata = {
            "description": description,
            "processingTime": processing_time,
            "originalFilename": image.filename
        }
        
        # 処理済み画像をブロードキャスト
        await broadcast_image(processed_image_data, metadata)
        
        return {
            "status": "success",
            "processingTime": processing_time,
            "message": "Image processed and broadcast successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket接続を処理する
    """
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        while True:
            # クライアントとの接続を維持
            await websocket.receive_text()
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        connected_clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(connected_clients)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
