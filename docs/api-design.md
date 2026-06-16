# API 設計書

CareerSync AI — FastAPI バックエンド API 仕様

---

## 概要

| 項目 | 内容 |
|---|---|
| ベース URL | `http://localhost:8000` |
| インタラクティブ仕様書 | `http://localhost:8000/docs` |
| フォーマット | JSON（`Content-Type: application/json`） |
| 認証 | なし（個人専用ローカルアプリ） |

---

## エラーレスポンス共通フォーマット

```json
{
  "detail": "エラーメッセージ（日本語）"
}
```

| ステータスコード | 意味 |
|---|---|
| 400 | 不正なリクエスト（更新フィールドなしなど） |
| 404 | リソースが見つからない |
| 409 | 競合（URL 重複など） |

---

## システム

### `GET /health` — ヘルスチェック

サーバー稼働確認。CI やモニタリングツールが定期的に叩く。

**レスポンス例（200）**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## 企業管理 API

### `GET /api/companies` — 企業一覧取得

**クエリパラメータ**

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `status` | string | なし | 選考ステータスでフィルター |
| `sort_by` | string | `created_at` | ソート対象カラム |
| `order` | string | `desc` | `asc` または `desc` |

`sort_by` で指定できるカラム:
`id`, `name`, `created_at`, `status`, `hiring_probability_score`, `tech_growth_score`, `career_growth_score`, `expected_first_salary`, `commute_time_car`

**レスポンス例（200）**
```json
[
  {
    "id": 1,
    "name": "株式会社サンプル",
    "url": "https://sample.co.jp",
    "status": "書類応募",
    "hiring_probability_score": 7,
    "scores": "{\"growth\": 8, \"stability\": 6, ...}",
    "created_at": "2026-06-16 10:00:00"
  }
]
```

---

### `POST /api/companies` — 企業登録

**リクエストボディ**

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `url` | string | ✅ | 企業URL（重複不可） |
| `name` | string | | 企業名 |
| `job_url` | string | | 求人票URL |
| `source` | string | | 求人媒体（リクナビなど） |
| `notes` | string | | メモ |

**レスポンス（201）**: 作成した企業オブジェクト

**エラー**
- `409 Conflict`: URL 重複

---

### `GET /api/companies/{id}` — 企業詳細取得

**パスパラメータ**

| パラメータ | 説明 |
|---|---|
| `id` | 企業ID（整数） |

**レスポンス（200）**: 企業オブジェクト（全フィールド）

**エラー**
- `404 Not Found`: 企業が存在しない

---

### `PATCH /api/companies/{id}` — 企業情報更新

部分更新（PUT ではなく PATCH）。`null` または省略したフィールドは変更されない。

フェーズ3でAIが分析結果（`scores`, `summary`, `strengths_weaknesses` など）を書き込む際もこのエンドポイントを使う。

**リクエストボディ（抜粋）**

```json
{
  "status": "1次面接",
  "notes": "技術面接あり。Python/FastAPI 重視とのこと。",
  "hiring_probability_score": 8
}
```

**レスポンス（200）**: 更新後の企業オブジェクト

---

### `DELETE /api/companies/{id}` — 企業削除

企業削除時、紐付いたスケジュールは `ON DELETE CASCADE` で自動削除される。

**レスポンス（204）**: なし

---

## スケジュール管理 API

### `GET /api/schedules` — スケジュール一覧取得

**クエリパラメータ**

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `company_id` | integer | なし | 特定企業の面接のみ取得 |
| `upcoming` | boolean | `false` | 未来の予定のみ返す |

**レスポンス例（200）**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "company_name": "株式会社サンプル",
    "event_title": "1次面接",
    "start_time": "2026-06-20T14:00:00",
    "interview_format": "オンライン",
    "result": null
  }
]
```

---

### `POST /api/schedules` — スケジュール登録

**リクエストボディ**

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `company_id` | integer | ✅ | 企業ID |
| `event_title` | string | ✅ | 例: 1次面接 |
| `start_time` | string | ✅ | ISO 8601形式（例: `2026-06-20T14:00:00`） |
| `interview_format` | string | | 対面 / オンライン |
| `interviewer` | string | | 面接官名・部署 |
| `interview_notes` | string | | 事前メモ |

**レスポンス（201）**: 作成したスケジュールオブジェクト

**エラー**
- `404 Not Found`: 企業IDが存在しない

---

### `PATCH /api/schedules/{id}` — スケジュール更新（結果記録）

面接後に結果（通過/不合格/待機中）を記録する際に使用する。

**リクエスト例**
```json
{
  "result": "通過",
  "interview_notes": "技術的な質問が中心。コードレビューの経験を聞かれた。"
}
```

**レスポンス（200）**: 更新後のスケジュールオブジェクト

---

### `DELETE /api/schedules/{id}` — スケジュール削除

**レスポンス（204）**: なし

---

## ユーザープロフィール API

### `GET /api/profile` — プロフィール取得

ユーザー自身の情報（1行固定）を返す。
`current_skills` と `ng_keywords` はJSONデコードされた配列として返される。

**レスポンス例（200）**
```json
{
  "id": 1,
  "home_address": "福島県郡山市字原中",
  "commute_mode": "car",
  "current_salary": 600,
  "experience_years": 0,
  "current_skills": null,
  "desired_role": "バックエンドエンジニア（自社開発・受託）",
  "ng_keywords": ["SES", "コールセンター", "携帯販売", "テレアポ"]
}
```

---

### `PATCH /api/profile` — プロフィール更新

**リクエスト例**
```json
{
  "experience_years": 1,
  "current_skills": "[\"Python\", \"FastAPI\", \"SQLite\"]",
  "desired_role": "バックエンドエンジニア"
}
```

**レスポンス（200）**: 更新後のプロフィールオブジェクト

---

## 選考ステータスの遷移

```
検討中 → 書類応募 → 1次面接 → 2次面接 → 最終面接 → 内定 → 辞退
```

`PATCH /api/companies/{id}` の `status` フィールドで更新する。

---

## 今後追加予定のエンドポイント（フェーズ3以降）

| エンドポイント | 内容 |
|---|---|
| `POST /api/companies/{id}/analyze` | Gemini AI で企業分析を実行 |
| `GET /api/companies/compare` | 複数企業のレーダーチャート比較データ |
| `POST /api/schedules/{id}/sync-calendar` | Googleカレンダーに同期 |
