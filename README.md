# Photo Relay Python Service

リアルタイム画像処理と配信を行うPythonサービス。画像のアップロードを受け付け、背景除去処理を行い、接続されたクライアントにWebSocketを通じて配信します。

## 機能

- 画像アップロード用REST API
- リアルタイム背景除去処理
- WebSocketによるリアルタイム画像配信
- マルチクライアントサポート
- エラーハンドリングとロギング

## システム要件

- Python 3.9以上
- pip（Pythonパッケージマネージャー）

## インストール

1. リポジトリのクローン:
```bash
git clone https://github.com/your-organization/photo-relay-python.git
cd photo-relay-python
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
.\venv\Scripts\activate  # Windows
```

3. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

## 設定

環境変数でサービスの動作をカスタマイズできます：

```bash
# 必須の環境変数
export CORS_ORIGINS="http://localhost:3000,http://example.com"  # CORSで許可するオリジン

# オプションの環境変数
export LOG_LEVEL="INFO"  # ログレベル（DEBUG, INFO, WARNING, ERROR）
export MAX_UPLOAD_SIZE="10"  # アップロード可能な最大ファイルサイズ（MB）
```

## 起動方法

開発モード:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

本番モード:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API仕様

### REST API

#### POST /upload/
画像をアップロードし、背景除去処理を実行します。

**リクエスト**:
- Content-Type: multipart/form-data
- パラメータ:
  - image: ファイル（必須）
  - description: 文字列（オプション）

**レスポンス**:
```json
{
    "status": "success",
    "processingTime": 1234.56,
    "message": "Image processed and broadcast successfully"
}
```

### WebSocket API

#### WS /ws
画像データのリアルタイム受信用WebSocketエンドポイント。

**受信メッセージフォーマット**:
```json
{
    "imageData": "base64エンコードされた画像データ",
    "timestamp": "2024-10-25T12:34:56.789Z",
    "metadata": {
        "description": "画像の説明",
        "processingTime": 1234.56,
        "originalFilename": "example.jpg"
    }
}
```

## エラーハンドリング

サービスは以下の場合にエラーレスポンスを返します：

- 無効なファイル形式
- ファイルサイズ超過
- 画像処理エラー
- WebSocket接続エラー

エラーレスポンス例:
```json
{
    "status": "error",
    "message": "エラーの詳細メッセージ"
}
```

## ログ

ログは標準出力に出力され、以下の情報が含まれます：

- クライアントの接続/切断
- 画像処理の開始/完了
- エラーと例外
- パフォーマンスメトリクス

## モニタリング

サービスの状態は以下のメトリクスで監視できます：

- アクティブなWebSocket接続数
- 画像処理時間
- エラーレート
- メモリ使用量

## 開発者向け情報

### コードスタイル

このプロジェクトは[PEP 8](https://www.python.org/dev/peps/pep-0008/)に従っています。コードのフォーマットには`black`を使用してください：

```bash
black .
```

### テスト

テストの実行:
```bash
pytest tests/
```

### 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

[MITライセンス](LICENSE)

## サポート

問題や質問がある場合は、GitHubのIssueを作成してください。
