import xmindparser
import os


def convert_to_markdown(data, level=1):
    """
    再帰的にXMindデータをMarkdown形式に変換
    """
    md_content = ""
    for topic in data:
        # Markdownの見出しレベル
        md_content += f"{'#' * level} {topic.get('title', 'Untitled')}\n\n"

        # メモ (notes) の追加
        if 'note' in topic:
            md_content += f"{topic['note']}\n\n"

        # 子トピックが存在する場合
        if 'topics' in topic:
            md_content += convert_to_markdown(topic['topics'], level + 1)

    return md_content


def xmind_to_md(xmind_file, output_md_file):
    """
    XMindファイルをMarkdown形式に変換
    """
    # XMindファイルを解析
    xmind_data = xmindparser.xmind_to_dict(xmind_file)
    sheet_data = xmind_data[0]  # 最初のシートのみを対象にする
    root_topic = sheet_data['topic']

    # Markdown変換
    md_content = convert_to_markdown([root_topic])

    # ファイル保存
    with open(output_md_file, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

    print(f"Markdownファイルを生成しました: {output_md_file}")


def process_directory(input_dir, output_dir):
    """
    inputディレクトリ内のすべてのXMindファイルを処理してoutputディレクトリに保存。
    処理後、inputディレクトリ内のファイルを削除。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xmind"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".md"
            output_file_path = os.path.join(output_dir, output_file_name)

            # XMindファイルをMarkdownに変換
            xmind_to_md(input_file_path, output_file_path)

            # 処理済みファイルを削除
            os.remove(input_file_path)
            print(f"処理完了: {file_name} -> {output_file_name} (削除済み)")


if __name__ == "__main__":
    # ディレクトリ設定
    input_directory = "input"
    output_directory = "output/markdown"

    if not os.path.exists(input_directory):
        print(f"入力ディレクトリが存在しません: {input_directory}")
    else:
        process_directory(input_directory, output_directory)
        print("全てのファイルを処理し、入力ディレクトリを空にしました。")

