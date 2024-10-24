# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
import asyncio
from PIL import Image
import io
import sys
import os

# テスト用のパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def test_client():
    """
    FastAPIのテストクライアントを提供するフィクスチャ
    """
    return TestClient(app)

@pytest.fixture
def test_image():
    """
    テスト用の画像を生成するフィクスチャ
    """
    # 100x100の白い画像を作成
    image = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# tests/test_upload.py
import pytest
from fastapi.testclient import TestClient
import json
import base64

def test_upload_endpoint_success(test_client, test_image):
    """
    画像アップロードエンドポイントの正常系テスト
    """
    files = {
        'image': ('test.png', test_image, 'image/png')
    }
    response = test_client.post(
        "/upload/",
        files=files,
        data={"description": "Test image"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "processingTime" in data
    assert isinstance(data["processingTime"], (int, float))

def test_upload_endpoint_no_image(test_client):
    """
    画像なしでアップロードした場合のテスト
    """
    response = test_client.post("/upload/")
    assert response.status_code == 422  # FastAPIのバリデーションエラー

def test_upload_endpoint_invalid_image(test_client):
    """
    無効な画像データでアップロードした場合のテスト
    """
    files = {
        'image': ('test.txt', b'invalid image data', 'text/plain')
    }
    response = test_client.post("/upload/", files=files)
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"

# tests/test_websocket.py
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import asyncio
import json

async def test_websocket_connection():
    """
    WebSocket接続のテスト
    """
    async with app.websocket_route("/ws") as websocket:
        assert websocket.client_state.CONNECTED

async def test_websocket_broadcast(test_client, test_image):
    """
    WebSocketブロードキャストのテスト
    """
    # WebSocket接続を確立
    async with app.websocket_route("/ws") as websocket:
        # 画像をアップロード
        files = {
            'image': ('test.png', test_image, 'image/png')
        }
        response = await test_client.post(
            "/upload/",
            files=files,
            data={"description": "Test broadcast"}
        )
        
        # ブロードキャストメッセージを受信
        data = await websocket.receive_json()
        assert "imageData" in data
        assert "timestamp" in data
        assert "metadata" in data
        assert isinstance(data["imageData"], str)
        
        # Base64デコードが可能か確認
        try:
            base64.b64decode(data["imageData"])
        except Exception:
            pytest.fail("Invalid base64 image data")

# tests/test_error_handling.py
def test_large_file_upload(test_client):
    """
    大きすぎるファイルのアップロード時のエラーハンドリングテスト
    """
    # 11MBの大きな画像データを生成
    large_data = b'0' * (11 * 1024 * 1024)
    files = {
        'image': ('large.png', large_data, 'image/png')
    }
    response = test_client.post("/upload/", files=files)
    assert response.status_code == 413  # Payload Too Large

def test_concurrent_connections(test_client):
    """
    複数の同時WebSocket接続のテスト
    """
    max_connections = 5
    connections = []
    
    # 複数のWebSocket接続を確立
    for _ in range(max_connections):
        with test_client.websocket_connect("/ws") as websocket:
            connections.append(websocket)
            
    # 全ての接続が成功していることを確認
    assert len(connections) == max_connections
    
    # 接続を閉じる
    for conn in connections:
        conn.close()

# tests/test_performance.py
import time
import statistics

def test_processing_time(test_client, test_image):
    """
    画像処理時間のパフォーマンステスト
    """
    processing_times = []
    num_requests = 5
    
    for _ in range(num_requests):
        files = {
            'image': ('test.png', test_image, 'image/png')
        }
        start_time = time.time()
        response = test_client.post("/upload/", files=files)
        end_time = time.time()
        
        assert response.status_code == 200
        processing_times.append(end_time - start_time)
    
    avg_time = statistics.mean(processing_times)
    assert avg_time < 2.0  # 平均処理時間が2秒未満であることを確認

# tests/conftest.py の続き
@pytest.fixture(autouse=True)
def mock_broadcast(monkeypatch):
    """
    ブロードキャスト関数をモック化するフィクスチャ
    """
    async def mock_broadcast_image(*args, **kwargs):
        pass
    
    monkeypatch.setattr("main.broadcast_image", mock_broadcast_image)
