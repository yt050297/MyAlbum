import os
import sys
import base64
import mimetypes

# ベースパスを指定（例: backend/app ディレクトリ）
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if base_path not in sys.path:
    sys.path.append(base_path)

from fastapi import HTTPException

# 画像を格納するディレクトリ
UPLOAD_BASE_DIRECTORY = os.path.abspath(
    os.path.join(base_path, "../public/uploaded_images")
)


# 画像ファイルをBase64エンコードしてデータURL形式に変換する関数
# Base64エンコードすることで、画像ファイルを文字列として送信可能なデータに変換できる
def encode_image_to_base64(filepath):
    try:
        # 画像ファイルをバイナリモードで開き、読み込む
        with open(filepath, "rb") as image_file:
            # ファイル内容をBase64エンコードし、デコードしてUTF-8の文字列として保存
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # MIMEタイプ（例: image/jpeg, image/pngなど）をファイルパスから推測
        # MIMEタイプはファイルの種類を示し、データURLに含めることでクライアント側で適切に処理できるようにする
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type is None:
            # MIMEタイプが不明な場合には、application/octet-streamをデフォルトで設定
            mime_type = "application/octet-stream"

        # データURL形式（例: data:image/jpeg;base64,...）に変換して返す
        data_url = f"data:{mime_type};base64,{encoded_string}"
        return data_url
    except Exception as e:
        # 例外発生時にはNoneを返す（必要に応じて詳細な例外処理を追加することも可能）
        return None


# 画像ファイルをディレクトリごとに一覧表示する関数
def list_image_files():
    try:
        # ディレクトリ構造とファイル情報を格納する辞書
        folder_structure = {}

        # 指定したルートディレクトリ（UPLOAD_BASE_DIRECTORY）内の1階層目のみを探索
        for root, dirs, files in os.walk(UPLOAD_BASE_DIRECTORY):
            # root: 現在のディレクトリパス
            # dirs: 現在のディレクトリ内のサブディレクトリ名リスト
            # files: 現在のディレクトリ内のファイル名リスト
            # 1階層目で止めるため、このループ内で処理を完結させる
            # 現在のディレクトリの相対パスを取得（ルートディレクトリからの相対的な位置）
            relative_root = os.path.relpath(root, UPLOAD_BASE_DIRECTORY)

            # ディレクトリ内の画像ファイルをフィルタリングして取得（.png, .jpg, .jpeg, .gifファイルのみ）
            # 空のリストを用意
            image_files = []
            # 条件に合うファイルのみを追加
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    image_files.append(file)

            # 画像ファイルリストを格納するためのリスト
            image_files_data = []
            for file in image_files:
                # 各画像ファイルの絶対パスを作成
                filepath = os.path.join(root, file)

                # 画像ファイルをBase64エンコードしてデータURL形式に変換
                base64_data = encode_image_to_base64(filepath)

                # エンコードが成功した場合、ファイル名とエンコードデータをリストに追加
                if base64_data is not None:
                    image_files_data.append({"filename": file, "base64": base64_data})

            # 現在のフォルダ内の画像データをフォルダ構造辞書に追加
            folder_structure[relative_root] = {
                "files": image_files_data,
            }

            # サブディレクトリ（2階層目）の処理
            # 1階層目のみを含めるため、サブディレクトリの中身を個別に取得
            for sub_dir in dirs:
                # サブディレクトリのパスを作成
                sub_dir_path = os.path.join(root, sub_dir)

                # サブディレクトリ内の画像ファイルをフィルタリング
                sub_dir_files = [
                    file
                    for file in os.listdir(sub_dir_path)
                    if file.endswith((".png", ".jpg", ".jpeg", ".gif"))
                ]

                # サブディレクトリ内の画像ファイルを格納するためのリスト
                sub_dir_files_data = []
                for file in sub_dir_files:
                    # 各サブディレクトリ内の画像ファイルの絶対パスを作成
                    filepath = os.path.join(sub_dir_path, file)

                    # 画像ファイルをBase64エンコード
                    base64_data = encode_image_to_base64(filepath)

                    # エンコードが成功した場合、サブディレクトリ内のファイルリストに追加
                    if base64_data is not None:
                        sub_dir_files_data.append(
                            {"filename": file, "base64": base64_data}
                        )

                # サブディレクトリ名をキーとして、サブディレクトリ内の画像ファイル情報を辞書に保存
                folder_structure[sub_dir] = {"files": sub_dir_files_data}

            # 1階層目のディレクトリでループを終了（1階層目のみを探索）
            break

        # 画像データが一つも見つからない場合、404エラーを発生させる
        if not folder_structure:
            raise HTTPException(
                status_code=404, detail="No directories or images found"
            )

        # フォルダ構造（ディレクトリとファイル情報の辞書）を返す
        return folder_structure

    except Exception as e:
        # 処理中に例外が発生した場合、500エラーを発生させてエラーメッセージを返す
        raise HTTPException(status_code=500, detail=str(e))
