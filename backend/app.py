import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # JSからのアクセス（CORS）を許可

def create_prefecture_dataframe():
    """
    Excelファイルから2桁の都道府県コードと都道府県名のDataFrameを生成
    """
    file_path = r"C:\Users\KENTA SHIMOJI\Documents\git\web_first\backend\000925835.xlsx"
    
    # Excelファイルを読み込み（最初のシート）
    df = pd.read_excel(file_path, sheet_name=0)
    
    # 団体コードから2桁の都道府県コードを抽出
    df['都道府県コード'] = df['団体コード'].astype(str).str[:2]
    
    # 都道府県名の列名を統一（改行文字を削除）
    prefecture_col = '都道府県名\r\n（漢字）'
    if prefecture_col not in df.columns:
        # 列名が異なる場合の対応
        prefecture_col = [col for col in df.columns if '都道府県' in col and '漢字' in col][0]
    
    # 都道府県コードと都道府県名でグループ化して重複を除去
    prefecture_df = df[['都道府県コード', prefecture_col]].drop_duplicates()
    prefecture_df = prefecture_df.rename(columns={prefecture_col: '都道府県名'})
    
    # 都道府県コード順にソート
    prefecture_df = prefecture_df.sort_values('都道府県コード').reset_index(drop=True)
    
    return prefecture_df

@app.route("/prefectures", methods=["GET"])
def get_prefectures():
    """
    都道府県リストをJSON形式で返す
    JavaScript側で期待される形式: [{"code": "01", "name": "北海道"}, ...]
    """
    try:
        # DataFrameを生成
        prefecture_df = create_prefecture_dataframe()
        
        # JavaScript側が期待する形式に変換
        prefectures = []
        for _, row in prefecture_df.iterrows():
            prefectures.append({
                "code": row['都道府県コード'],
                "name": row['都道府県名']
            })
        
        return jsonify(prefectures)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/prefectures/dataframe", methods=["GET"])
def get_prefectures_dataframe():
    """
    DataFrameの内容を確認用のエンドポイント
    """
    try:
        prefecture_df = create_prefecture_dataframe()
        
        # DataFrameを辞書形式に変換
        return jsonify({
            "columns": prefecture_df.columns.tolist(),
            "data": prefecture_df.to_dict('records'),
            "shape": prefecture_df.shape
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 起動時にDataFrameの内容を確認
    try:
        df = create_prefecture_dataframe()
        print("都道府県データの生成が完了しました。")
        print(f"データ件数: {len(df)}件")
        print("\n最初の5件:")
        print(df.head())
        print("\n最後の5件:")
        print(df.tail())
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    app.run(port=8000, debug=True)