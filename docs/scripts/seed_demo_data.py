"""
スクリーンショット撮影用のデモデータをDBに投入するスクリプト。

Gemini APIを呼び出さずにリアルな表示状態を再現する。
既存データがある場合は重複しないよう INSERT OR IGNORE で挿入する。

実行方法（プロジェクトルートから）:
    python docs/scripts/seed_demo_data.py
"""

import json
import sys
from pathlib import Path

# プロジェクトルートをパスに追加（database モジュールをインポートするため）
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from database.connection import get_connection
from database.models import init_db


DEMO_COMPANIES = [
    {
        "name": "株式会社ラクス",
        "url": "https://www.rakus.co.jp/demo-seed-1",
        "job_url": "https://www.rakus.co.jp/recruit/",
        "industry": "SaaS・クラウドサービス",
        "employees": "1,500名",
        "founded_year": 2000,
        "listing_status": "東証プライム",
        "development_type": "自社開発",
        "location": "東京都新宿区",
        "commute_time_car": None,
        "commute_time_shinkansen": 90,
        "commute_allowance": "支給（上限あり）",
        "work_style": "ハイブリッド（週2〜3日リモート）",
        "overtime_hours": 20,
        "paid_leave_rate": 75,
        "transfer": "なし",
        "salary": "400〜700万円",
        "expected_first_salary": 440,
        "salary_upper": 700,
        "years_to_recover": 0.0,
        "inexperienced_ok": 1,
        "training_program": "3ヶ月の研修プログラムあり。未経験者向けOJT完備",
        "hiring_probability_score": 72,
        "job_description": "バックエンドエンジニアとして、クラウド経費精算・勤怠管理SaaSの開発を担当。Java/Spring Boot + PostgreSQL環境。未経験者歓迎。",
        "skill_stack": '["Java", "Spring Boot", "PostgreSQL", "AWS", "Git"]',
        "tech_growth_score": 8,
        "career_growth_score": 7,
        "career_path": "エンジニア → シニアエンジニア → テックリード → エンジニアリングマネージャー",
        "benefits": "フレックス・リモートワーク・健康保険・退職金制度・資格取得支援",
        "summary": "中小企業向けSaaSを複数展開する東証プライム上場企業。楽楽精算・楽楽勤怠など業界シェアNo.1製品を保有。未経験エンジニアの育成実績が豊富で、研修制度が充実している。",
        "strengths_weaknesses": json.dumps({
            "strengths": ["上場企業の安定性", "未経験者育成実績が豊富", "業界シェアNo.1製品を複数保有", "フルリモート可能な案件あり"],
            "weaknesses": ["給与水準はやや保守的", "大企業のため意思決定に時間がかかることも", "東京本社のため郡山からの新幹線通勤が必要"]
        }, ensure_ascii=False),
        "interview_strategy": json.dumps([
            {"question": "なぜSaaS企業を志望したのですか？", "answer": "ユーザーが日常的に使うプロダクトを作り続けられる環境に魅力を感じています。楽楽精算のような業務効率化ツールは多くの企業の課題を解決しており、社会的インパクトを感じながら働けると考えています。"},
            {"question": "未経験からエンジニアを目指した理由を教えてください。", "answer": "RaiseTechでJava/Spring Bootを学ぶ中で、コードが動く瞬間の達成感とロジックを組み立てる思考プロセスに強い適性を感じました。ITで業務課題を解決する仕事に将来性を感じ転職を決意しました。"},
            {"question": "入社後はどのように成長していきたいですか？", "answer": "まずは3ヶ月の研修でチームの開発フローを習得し、6ヶ月以内に独力でタスクを完遂できるレベルを目指します。1年後にはチームに貢献できるシニアエンジニアの基礎を固めたいと考えています。"}
        ], ensure_ascii=False),
        "scores": json.dumps({"growth": 8, "stability": 9, "culture_fit": 7, "work_life_balance": 7, "compensation": 6}, ensure_ascii=False),
        "status": "1次面接",
        "source": "Green",
        "notes": "未経験歓迎・研修充実。新幹線通勤手当が出るか確認必要。",
        "motivation": "業界トップSaaS、安定性と成長性のバランスが良い",
    },
    {
        "name": "株式会社ヌーラボ",
        "url": "https://nulab.com/demo-seed-2",
        "job_url": "https://nulab.com/ja/about/jobs/",
        "industry": "コラボレーションツール・SaaS",
        "employees": "300名",
        "founded_year": 2004,
        "listing_status": "未上場",
        "development_type": "自社開発",
        "location": "福岡市中央区（フルリモート可）",
        "commute_time_car": None,
        "commute_time_shinkansen": None,
        "commute_allowance": "フルリモートのため不要",
        "work_style": "フルリモート（月1回程度の出社あり）",
        "overtime_hours": 10,
        "paid_leave_rate": 90,
        "transfer": "なし",
        "salary": "450〜750万円",
        "expected_first_salary": 470,
        "salary_upper": 750,
        "years_to_recover": 0.0,
        "inexperienced_ok": 0,
        "training_program": "OJTあり。メンター制度で丁寧にサポート",
        "hiring_probability_score": 45,
        "job_description": "Backlog・Cacoo・Typetalkなど自社プロダクトのバックエンド開発。Scala/Kotlin + AWSで大規模SaaSを開発。",
        "skill_stack": '["Scala", "Kotlin", "AWS", "PostgreSQL", "Docker", "Kubernetes"]',
        "tech_growth_score": 9,
        "career_growth_score": 8,
        "career_path": "ソフトウェアエンジニア → シニア → リード → プリンシパル",
        "benefits": "フルリモート・フレックス・書籍購入支援・カンファレンス参加支援・副業OK",
        "summary": "「Backlog」「Cacoo」などプロジェクト管理・ビジュアルコラボレーションツールを世界80カ国以上で展開する福岡発のSaaS企業。エンジニアファーストの文化と高い技術水準が特徴。フルリモート勤務が確立されており、郡山からでも働ける。",
        "strengths_weaknesses": json.dumps({
            "strengths": ["フルリモートで郡山から勤務可能", "高い技術水準とエンジニアファースト文化", "副業・カンファレンス参加支援など福利厚生充実", "WLBが非常に良い（残業少）"],
            "weaknesses": ["未経験者採用は少ない（即戦力重視）", "未上場のためストックオプション価値は不確定", "競争率が高い"]
        }, ensure_ascii=False),
        "interview_strategy": json.dumps([
            {"question": "なぜヌーラボを志望しましたか？", "answer": "Backlogを実際に使っており、チームの生産性を劇的に高めるプロダクト力に感銘を受けました。また、エンジニアの技術的成長を重視する文化と、フルリモートで働ける環境が自分のキャリアビジョンと完全に一致しています。"},
            {"question": "Scalaの経験はありますか？", "answer": "直接の経験はありませんが、RaiseTechでJava/Spring Bootを学んでおり、関数型プログラミングの概念も独学で学習中です。ScalaはJVM上で動作するため、Javaの経験を活かしながら習得できると考えています。"},
            {"question": "リモートワークで工夫していることはありますか？", "answer": "タスク管理にBacklogを個人利用しており、毎朝タスクを整理して優先順位をつける習慣があります。コミュニケーションは非同期を基本としつつ、緊急時はすぐビデオ通話で解決するというスタンスです。"}
        ], ensure_ascii=False),
        "scores": json.dumps({"growth": 9, "stability": 6, "culture_fit": 9, "work_life_balance": 9, "compensation": 7}, ensure_ascii=False),
        "status": "応募済",
        "source": "Wantedly",
        "notes": "フルリモートで郡山から勤務可能。技術レベルが高いため書類でどこまで通過できるか。",
        "motivation": "フルリモート・高技術水準・WLB最高",
    },
    {
        "name": "株式会社サイバーエージェント",
        "url": "https://www.cyberagent.co.jp/demo-seed-3",
        "job_url": "https://www.cyberagent.co.jp/careers/",
        "industry": "インターネット広告・メディア・ゲーム",
        "employees": "7,000名（グループ全体）",
        "founded_year": 1998,
        "listing_status": "東証プライム",
        "development_type": "自社開発",
        "location": "東京都渋谷区",
        "commute_time_car": None,
        "commute_time_shinkansen": 80,
        "commute_allowance": "支給（条件あり）",
        "work_style": "出社メイン（週3〜4日）",
        "overtime_hours": 25,
        "paid_leave_rate": 70,
        "transfer": "グループ会社への転籍あり",
        "salary": "500〜1000万円",
        "expected_first_salary": 520,
        "salary_upper": 1000,
        "years_to_recover": 0.0,
        "inexperienced_ok": 1,
        "training_program": "CA Tech Kids/CA Academyなど充実した研修制度",
        "hiring_probability_score": 38,
        "job_description": "Ameba・ABEMA・ウマ娘など自社サービスのバックエンド開発。Go/Java/Scala + マイクロサービスアーキテクチャで大規模システムを開発。",
        "skill_stack": '["Go", "Java", "Scala", "MySQL", "Redis", "Kubernetes", "GCP"]',
        "tech_growth_score": 10,
        "career_growth_score": 9,
        "career_path": "エンジニア → シニア → テックリード → CTO候補",
        "benefits": "福利厚生充実・社内副業・技術書籍支援・健康経営優良法人認定",
        "summary": "「ABEMA」「Ameba」「ウマ娘」を展開する日本トップクラスのインターネット企業。技術力の高さと若手登用文化が特徴。新卒・第二新卒採用に力を入れており、未経験でもポテンシャル採用あり。",
        "strengths_weaknesses": json.dumps({
            "strengths": ["日本最高水準の技術環境", "大きなプロダクトへの関与でスキルが急成長", "若手登用文化・裁量が大きい", "給与上限が非常に高い"],
            "weaknesses": ["競争率が非常に高い（採用倍率高）", "出社メインで東京在住が実質必要", "成果主義で結果を出し続ける必要がある", "渋谷本社のため郡山からの通勤は困難"]
        }, ensure_ascii=False),
        "interview_strategy": json.dumps([
            {"question": "なぜサイバーエージェントを志望しましたか？", "answer": "ABEMAやウマ娘など、億単位のユーザーが使うサービスを開発できる環境は他にありません。最高の技術環境でエンジニアとして急成長したいと考え、志望しました。"},
            {"question": "ポートフォリオについて教えてください。", "answer": "CareerSync AIという転職活動支援アプリを個人開発しました。FastAPI + SQLite + Gemini AIで、企業URLを入力するだけでAIが自動分析・スコアリングするWebアプリです。GitHubで公開しており、コードの品質にこだわりました。"},
            {"question": "入社後5年でどのようなエンジニアになりたいですか？", "answer": "大規模システムの設計・実装を通じて、テックリードとして技術判断を行えるエンジニアになりたいと考えています。そのために最初の2年は基礎を徹底的に固め、その後はシステム設計の経験を積みたいです。"}
        ], ensure_ascii=False),
        "scores": json.dumps({"growth": 10, "stability": 8, "culture_fit": 7, "work_life_balance": 5, "compensation": 9}, ensure_ascii=False),
        "status": "検討中",
        "source": "マイナビ転職",
        "notes": "技術力は最高だが、東京在住が実質必要。通勤手当の条件要確認。競争率も高い。",
        "motivation": "最高の技術環境でスキルを急成長させたい",
    },
    {
        "name": "株式会社SmartHR",
        "url": "https://smarthr.co.jp/demo-seed-4",
        "job_url": "https://smarthr.co.jp/job/",
        "industry": "HR Tech・クラウドSaaS",
        "employees": "1,200名",
        "founded_year": 2013,
        "listing_status": "未上場（IPO準備中）",
        "development_type": "自社開発",
        "location": "東京都港区（フルリモート可）",
        "commute_time_car": None,
        "commute_time_shinkansen": None,
        "commute_allowance": "フルリモートのため不要",
        "work_style": "フルリモート（希望者は出社可）",
        "overtime_hours": 15,
        "paid_leave_rate": 85,
        "transfer": "なし",
        "salary": "500〜900万円",
        "expected_first_salary": 530,
        "salary_upper": 900,
        "years_to_recover": 0.0,
        "inexperienced_ok": 0,
        "training_program": "メンター制度・オンボーディングプログラム完備",
        "hiring_probability_score": 50,
        "job_description": "クラウド人事労務ソフト「SmartHR」のバックエンド開発。Ruby on Rails + PostgreSQLで日本最大級のHR SaaSを開発。",
        "skill_stack": '["Ruby", "Ruby on Rails", "PostgreSQL", "AWS", "Docker", "Terraform"]',
        "tech_growth_score": 8,
        "career_growth_score": 9,
        "career_path": "エンジニア → シニア → スタッフ → プリンシパル",
        "benefits": "フルリモート・フレックス・書籍購入全額支援・カンファレンス費用支援・副業OK・育児支援充実",
        "summary": "HR領域クラウドSaaSとして国内シェアNo.1を誇るSmartHR。IPO準備中のスタートアップで、急成長フェーズにある。技術的な負債を丁寧に解消しながら品質を高める文化と、フルリモートによる働きやすさが評価されている。",
        "strengths_weaknesses": json.dumps({
            "strengths": ["フルリモートで郡山から勤務可能", "IPO前のストックオプション機会", "HR領域国内シェアNo.1で安定した成長", "WLBが良く育児支援も充実"],
            "weaknesses": ["未経験者採用は少ない（即戦力重視）", "Ruby未経験者にはキャッチアップが必要", "未上場のためIPO時期は不確定"]
        }, ensure_ascii=False),
        "interview_strategy": json.dumps([
            {"question": "なぜSmartHRを志望しましたか？", "answer": "HR領域のデジタル化は日本社会の課題解決に直結すると考えています。SmartHRが人事労務のデジタル化を推進することで、多くの企業の管理部門の負担が軽減されます。また、フルリモートで郡山から働ける環境も大きな魅力です。"},
            {"question": "Rubyの経験はありますか？", "answer": "直接の業務経験はありませんが、JavaとPythonでの開発経験があります。RubyはJavaよりも記述が簡潔で、Rails conventions を習得することでスムーズにキャッチアップできると考えています。選考期間中も積極的に学習します。"},
            {"question": "リモートワークで困ったことはありますか？", "answer": "対面でのコミュニケーションがないため、意図が伝わりにくいことがあります。対策として、テキストコミュニケーションでは背景と結論を最初に書くこと、絵文字や例示で感情を補うことを意識しています。"}
        ], ensure_ascii=False),
        "scores": json.dumps({"growth": 9, "stability": 7, "culture_fit": 8, "work_life_balance": 9, "compensation": 8}, ensure_ascii=False),
        "status": "書類選考中",
        "source": "Findy",
        "notes": "フルリモート可・IPO前で成長期。Rubyのキャッチアップが課題。",
        "motivation": "フルリモート＋IPO前の成長機会＋WLBのバランスが理想的",
    },
]

DEMO_SCHEDULES = [
    {
        "company_name": "株式会社ラクス",
        "event_title": "ラクス 1次面接",
        "interview_format": "オンライン（Zoom）",
        "interviewer": "人事部 田中様、エンジニアリング部 山田様",
        "interview_notes": "技術面接あり。Spring Bootの基礎を復習しておくこと。",
        "start_time": "2026-06-25T14:00:00",
    },
    {
        "company_name": "株式会社SmartHR",
        "event_title": "SmartHR 書類選考結果連絡（予定）",
        "interview_format": "メール",
        "interviewer": None,
        "interview_notes": "書類提出から2週間以内に連絡とのこと。",
        "start_time": "2026-06-30T10:00:00",
    },
]


def seed():
    init_db()
    conn = get_connection()

    try:
        # 企業データ投入
        inserted = 0
        for c in DEMO_COMPANIES:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO companies (
                        name, url, job_url, industry, employees, founded_year,
                        listing_status, development_type, location,
                        commute_time_car, commute_time_shinkansen, commute_allowance,
                        work_style, overtime_hours, paid_leave_rate, transfer,
                        salary, expected_first_salary, salary_upper, years_to_recover,
                        inexperienced_ok, training_program, hiring_probability_score,
                        job_description, skill_stack, tech_growth_score, career_growth_score,
                        career_path, benefits, summary, strengths_weaknesses,
                        interview_strategy, scores, status, source, notes, motivation
                    ) VALUES (
                        :name, :url, :job_url, :industry, :employees, :founded_year,
                        :listing_status, :development_type, :location,
                        :commute_time_car, :commute_time_shinkansen, :commute_allowance,
                        :work_style, :overtime_hours, :paid_leave_rate, :transfer,
                        :salary, :expected_first_salary, :salary_upper, :years_to_recover,
                        :inexperienced_ok, :training_program, :hiring_probability_score,
                        :job_description, :skill_stack, :tech_growth_score, :career_growth_score,
                        :career_path, :benefits, :summary, :strengths_weaknesses,
                        :interview_strategy, :scores, :status, :source, :notes, :motivation
                    )
                """, c)
                if conn.execute("SELECT changes()").fetchone()[0] > 0:
                    inserted += 1
                    print(f"  [追加] {c['name']}")
                else:
                    print(f"  [スキップ] {c['name']}（既存）")
            except Exception as e:
                print(f"  [エラー] {c['name']}: {e}")

        # スケジュールデータ投入
        for s in DEMO_SCHEDULES:
            row = conn.execute(
                "SELECT id FROM companies WHERE name = ?", (s["company_name"],)
            ).fetchone()
            if row is None:
                print(f"  [スキップ] スケジュール: 企業が見つかりません ({s['company_name']})")
                continue
            company_id = row[0]
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO schedules (
                        company_id, event_title, interview_format,
                        interviewer, interview_notes, start_time
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    company_id, s["event_title"], s["interview_format"],
                    s["interviewer"], s["interview_notes"], s["start_time"],
                ))
                if conn.execute("SELECT changes()").fetchone()[0] > 0:
                    print(f"  [追加] スケジュール: {s['event_title']}")
            except Exception as e:
                print(f"  [エラー] スケジュール {s['event_title']}: {e}")

        conn.commit()
        print(f"\n[完了] デモデータを投入しました（企業 {inserted} 件追加）")

    finally:
        conn.close()


if __name__ == "__main__":
    seed()
