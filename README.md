# Photo Relay Python Service

リアルタイム画像処理と配信を行うPythonサービス。画像のアップロードを受け付け、背景除去処理を行い、接続されたクライアントにWebSocketを通じて配信します。

## 機能

- 画像アップロード用REST API
- リアルタイム背景除去処理
- WebSocketによるリアルタイム画像配信
- マルチクライアントサポート
- エラーハンドリングとロギング
- 包括的なテストスイート

## プロジェクト構成

```
photo-relay-python/
├── .vscode/                # VSCode設定
│   ├── settings.json      # エディタ設定
│   ├── launch.json        # デバッグ設定
│   ├── tasks.json         # タスク設定
│   └── extensions.json    # 推奨拡張機能
├── src/
│   └── photo_relay/       # メインのパッケージ
│       ├── __init__.py
│       └── main.py        # アプリケーションコード
├── tests/                 # テストコード
│   ├── __init__.py
│   ├── conftest.py       # テスト共通設定
│   └── test_upload.py    # アップロード機能のテスト
├── docs/                  # ドキュメント
├── requirements.txt       # 本番用依存パッケージ
├── requirements-dev.txt   # 開発用依存パッケージ
└── pyproject.toml        # プロジェクト設定
```

## システム要件

- Python 3.9以上
- pip（Pythonパッケージマネージャー）
- VSCode（推奨エディタ）

## 開発環境のセットアップ

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
# 開発用パッケージを含む全ての依存関係をインストール
pip install -r requirements-dev.txt
```

4. VSCode拡張機能のインストール:
- VSCodeを開く
- 推奨拡張機能タブを開く（Ctrl+Shift+X）
- 表示される推奨拡張機能をインストール

## VSCode開発環境

### 設定済み機能

- Pythonインタープリターの自動設定
- コードフォーマット（Black）の自動適用
- Flake8によるリンティング
- Pytestによるテスト実行
- デバッグ設定
- タスクランナー

### 利用可能なタスク

VSCodeで`Cmd/Ctrl + Shift + P`を押して"Tasks: Run Task"を選択し、以下のタスクを実行できます：

- `Run Tests`: テストを実行しカバレッジレポートを生成
- `Format Code`: Blackでコードをフォーマット
- `Lint Code`: Flake8でコードをチェック
- `Type Check`: mypyで型チェック
- `Run Development Server`: 開発サーバーを起動

### デバッグ設定

`F5`キーで以下のデバッグ設定を選択できます：

- `Python: FastAPI`: FastAPIアプリケーションの実行
- `Python: Current File`: 現在開いているファイルの実行
- `Python: Debug Tests`: テストのデバッグ実行

## テスト

### テストの実行

基本的なテスト実行:
```bash
pytest
```

カバレッジレポート付きでテストを実行:
```bash
pytest --cov=src/photo_relay tests/
```

詳細なテスト結果を表示:
```bash
pytest -v
```

特定のテストファイルのみ実行:
```bash
pytest tests/test_upload.py
```

## 開発ワークフロー

1. 新機能の開発:
```bash
git checkout -b feature/new-feature
```

2. コードの品質管理:
```bash
# コードフォーマット
black .

# 型チェック
mypy src/

# リンター
flake8 src/ tests/
```

3. テストの実行:
```bash
pytest --cov=src/photo_relay tests/
```

4. 開発サーバーの起動:
```bash
uvicorn src.photo_relay.main:app --reload --host 0.0.0.0 --port 8000
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

## 設定

環境変数による設定:

```bash
# 必須の環境変数
export CORS_ORIGINS="http://localhost:3000,http://example.com"

# オプションの環境変数
export LOG_LEVEL="INFO"
export MAX_UPLOAD_SIZE="10"
export WS_MAX_CONNECTIONS="100"
export PROCESSING_TIMEOUT="30"
```

## トラブルシューティング

### よくある問題と解決方法

1. VSCode関連:
   - Pythonインタープリターが見つからない → コマンドパレットから"Python: Select Interpreter"を実行
   - 拡張機能の競合 → 推奨されていない類似の拡張機能を無効化
   - デバッグが開始されない → launch.jsonの設定を確認

2. 開発環境:
   - 依存関係のエラー → `pip install -r requirements-dev.txt`を再実行
   - テストが見つからない → プロジェクト構造とpyproject.tomlを確認
   - フォーマットが適用されない → VSCodeの設定でBlackが有効になっているか確認

3. アプリケーション:
   - WebSocket接続エラー → CORS設定とポート番号を確認
   - 画像処理エラー → 入力画像のフォーマットとサイズを確認
   - パフォーマンス問題 → ワーカー数とメモリ使用量を確認

## 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### コーディング規約

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)に準拠
- 最大行長: 100文字
- ドキュメント文字列: Google形式
- 型ヒント: 必須

## ライセンス

[MITライセンス](LICENSE)

## サポート

- GitHubのIssueで問題を報告
- プルリクエストで改善を提案
- セキュリティ脆弱性の報告は security@example.com へ
