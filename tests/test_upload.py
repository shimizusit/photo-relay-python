import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io
import sys
import os
from pathlib import Path

# テスト対象のモジュールをインポートできるようにパスを追加
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from photo_relay.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def test_image():
    """テスト用の画像を生成するフィクスチャ"""
    image = Image.new("RGB", (100, 100), color="white")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr


def test_upload_endpoint_success(test_client, test_image):
    """画像アップロードエンドポイントの正常系テスト"""
    files = {"image": ("test.png", test_image, "image/png")}
    response = test_client.post(
        "/upload/", files=files, data={"description": "Test image"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "processingTime" in data
    assert isinstance(data["processingTime"], (int, float))


def test_upload_endpoint_no_image(test_client):
    """画像なしでアップロードした場合のテスト"""
    response = test_client.post("/upload/")
    assert response.status_code == 422  # FastAPIのバリデーションエラー
