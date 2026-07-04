import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="競合求人テスト", layout="wide")
st.title("🧪 競合求人 自動抽出テストアプリ")
st.markdown("SerpApiを使って、指定した条件の求人データをインターネットから自動で集めてくる実験です。")

# 画面からAPIキーを入力させる（テスト用）
api_key_input = st.text_input("SerpApiのAPIキーを貼り付けてください", type="password")

st.markdown("### 🔍 検索条件")
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("職種キーワード", placeholder="例: 介護職, 看護師, サービス管理責任者")
with col2:
    location = st.text_input("勤務地・エリア", placeholder="例: 大阪市中央区, 梅田駅")

if st.button("🚀 競合求人を検索する", use_container_width=True):
    if not api_key_input:
        st.warning("⚠️ SerpApiのAPIキーを入力してください。")
    elif not keyword or not location:
        st.warning("⚠️ キーワードと勤務地を入力してください。")
    else:
        with st.spinner("Googleしごと検索（Indeed等）からデータを自動取得中..."):
            try:
                # SerpApiへリクエストを送る
                url = "https://serpapi.com/search.json"
                params = {
                    "engine": "google_jobs", # 求人検索専用エンジン
                    "q": f"{keyword} {location}",
                    "hl": "ja", # 日本語
                    "gl": "jp", # 日本
                    "api_key": api_key_input
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # 検索結果（求人リスト）を取り出す
                jobs = data.get("jobs_results", [])
                
                if not jobs:
                    st.error("求人が見つかりませんでした。条件を変えてみてください。")
                else:
                    st.success(f"✅ {len(jobs)}件の求人データを取得しました！")
                    
                    # 取得した生データを、見やすい表（データフレーム）に変換する
                    job_list = []
                    for job in jobs:
                        job_list.append({
                            "会社名": job.get("company_name", "不明"),
                            "職種名": job.get("title", "不明"),
                            "勤務地": job.get("location", "不明"),
                            "給与・条件": job.get("salary", "記載なし"),
                            "求人本文": job.get("description", "記載なし")
                        })
                    
                    df = pd.DataFrame(job_list)
                    st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {e}")
