"""
Playwrightを使ってCareerSync AIのスクリーンショット・操作デモGIFを自動生成するスクリプト。

事前準備:
    1. uvicorn main:app --reload --port 8000 でサーバーを起動しておく
    2. python docs/scripts/seed_demo_data.py でデモデータを投入しておく
    3. pip install playwright Pillow imageio[ffmpeg]
    4. playwright install chromium

実行方法（プロジェクトルートから）:
    python docs/scripts/capture_screenshots.py

生成先: docs/images/
"""

import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("[エラー] Playwright がインストールされていません。")
    print("  pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    from PIL import Image
    import imageio
except ImportError:
    print("[エラー] Pillow / imageio がインストールされていません。")
    print("  pip install Pillow imageio")
    sys.exit(1)

BASE_URL = "http://localhost:8000"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "docs" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 1280, "height": 720}

# GIF用フレームを収集するリスト
gif_frames: list[Image.Image] = []


def capture(page, filename: str, wait_ms: int = 1000, for_gif: bool = True) -> Path:
    """スクリーンショットを撮影してファイルに保存する。GIF用に frames にも追加する。"""
    page.wait_for_timeout(wait_ms)
    path = OUTPUT_DIR / filename
    page.screenshot(path=str(path), full_page=False)
    print(f"  [撮影] {filename}")

    if for_gif:
        img = Image.open(path).convert("RGB")
        gif_frames.append(img)

    return path


def main():
    print("=== CareerSync AI スクリーンショット自動生成 ===\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()

        # ページ読み込み
        try:
            page.goto(BASE_URL, wait_until="networkidle", timeout=10_000)
        except PlaywrightTimeout:
            print(f"[エラー] {BASE_URL} に接続できません。")
            print("  uvicorn main:app --reload --port 8000 を先に起動してください。")
            browser.close()
            sys.exit(1)

        # ── 1. ダッシュボード全体（企業リスト） ──────────────────────
        print("\n[Scene 1] ダッシュボード全体")
        page.wait_for_selector(".company-card", timeout=8_000)
        capture(page, "01_dashboard.png", wait_ms=1200)

        # ── 2. 企業詳細（レーダーチャート） ───────────────────────────
        print("\n[Scene 2] 企業詳細・レーダーチャート")
        page.locator(".company-card").first.click()
        # レーダーチャートのcanvasが描画されるまで待つ
        page.wait_for_selector("canvas", timeout=6_000)
        capture(page, "02_detail_radar.png", wait_ms=1500)

        # ── 3. 別の企業を選択（ステータス違い） ───────────────────────
        print("\n[Scene 3] 別の企業選択")
        cards = page.locator(".company-card")
        if cards.count() >= 2:
            cards.nth(1).click()
            page.wait_for_timeout(1000)
            capture(page, "03_detail_another.png", wait_ms=800)

        # ── 4. 企業追加モーダル ───────────────────────────────────────
        print("\n[Scene 4] 企業追加モーダル")
        page.locator("#btn-add-company").click()
        page.wait_for_selector("#modal-add", state="visible", timeout=4_000)
        capture(page, "04_modal_add_company.png", wait_ms=600, for_gif=True)
        # 閉じるボタンでモーダルをクローズ
        page.locator("#btn-close-modal").click()
        page.wait_for_selector("#modal-add", state="hidden", timeout=4_000)
        page.wait_for_timeout(400)

        # ── 5. スクショからスケジュール登録モーダル ───────────────────
        print("\n[Scene 5] スクショからスケジュール登録モーダル")
        page.locator("#btn-add-schedule-image").click()
        page.wait_for_selector("#modal-schedule-image", state="visible", timeout=4_000)
        capture(page, "05_modal_schedule_image.png", wait_ms=600, for_gif=True)
        page.locator("#btn-close-schedule-modal").click()
        page.wait_for_timeout(400)

        browser.close()

    # ── GIF生成 ──────────────────────────────────────────────────────
    print("\n[GIF] 操作デモGIFを生成中...")

    if len(gif_frames) >= 2:
        gif_path = OUTPUT_DIR / "demo.gif"

        # 各フレームを2秒表示（fps=0.5）
        frame_arrays = [frame for frame in gif_frames]
        imageio.mimsave(
            str(gif_path),
            frame_arrays,
            duration=2.0,  # 各フレーム2秒
            loop=0,        # 無限ループ
        )
        print(f"  [完了] demo.gif ({len(gif_frames)}フレーム)")
    else:
        print("  [スキップ] フレームが不足しています")

    print(f"\n=== 完了 ===")
    print(f"生成先: {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.png")):
        size_kb = f.stat().st_size // 1024
        print(f"  {f.name} ({size_kb} KB)")
    gif = OUTPUT_DIR / "demo.gif"
    if gif.exists():
        size_kb = gif.stat().st_size // 1024
        print(f"  demo.gif ({size_kb} KB)")


if __name__ == "__main__":
    main()
