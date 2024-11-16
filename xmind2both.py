import xmindparser
import os

def convert_to_mermaid(data, level=1):
    """
    再帰的にXMindデータをMermaid mindmap形式に変換
    """
    mermaid_content = ""
    indent = "  " * level  # インデント管理
    for topic in data:
        # ノードのタイトルを取得
        title = topic.get("title", "Untitled")
        mermaid_content += f"{indent}{title}\n"

        # 子トピックが存在する場合
        if "topics" in topic:
            mermaid_content += convert_to_mermaid(topic["topics"], level + 1)

    return mermaid_content


def xmind_to_mermaid(xmind_file, output_md_file):
    """
    XMindファイルをMermaid mindmap形式に変換
    """
    # XMindファイルを解析
    xmind_data = xmindparser.xmind_to_dict(xmind_file)
    sheet_data = xmind_data[0]  # 最初のシートのみを対象にする
    root_topic = sheet_data["topic"]

    # ルートトピックのタイトル
    root_title = root_topic.get("title", "Untitled")

    # Mermaid記法のヘッダー
    mermaid_content = (
        "```mermaid\n"
        "%%{init:{'theme':'default'}}%%\n"
        "mindmap\n"
        f"  top(({root_title}))\n"
    )
    # レベル2以下を追加
    if "topics" in root_topic:
        mermaid_content += convert_to_mermaid(root_topic["topics"], level=2)

    mermaid_content += "```\n"

    # ファイル保存
    with open(output_md_file, "w", encoding="utf-8") as md_file:
        md_file.write(mermaid_content)

    print(f"Markdownファイルを生成しました: {output_md_file}")

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

def process_directory(input_dir, markdown_output_dir, mermaid_output_dir):
    """
    inputディレクトリ内のすべてのXMindファイルを処理してoutputディレクトリに保存。
    処理後、inputディレクトリ内のファイルを削除。
    """
    if not os.path.exists(markdown_output_dir):
        os.makedirs(markdown_output_dir)
    
    if not os.path.exists(mermaid_output_dir):
        os.makedirs(mermaid_output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xmind"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".md"
            markdown_output_file_path = os.path.join(markdown_output_dir, output_file_name)
            mermaid_output_file_path = os.path.join(mermaid_output_dir, output_file_name)

            # XMindファイルをMarkdownに変換
            xmind_to_md(input_file_path, markdown_output_file_path)

            # XMindファイルをMermaid形式に変換
            xmind_to_mermaid(input_file_path, mermaid_output_file_path)

            # 処理済みファイルを削除
            os.remove(input_file_path)
            print(f"処理完了: {file_name} -> {output_file_name} (削除済み)")


if __name__ == "__main__":
    # ディレクトリ設定
    input_directory = "input"
    markdown_output_directory = "output/markdown"
    mermaid_output_directory = "output/mermaid"

    if not os.path.exists(input_directory):
        print(f"入力ディレクトリが存在しません: {input_directory}")
    else:
        process_directory(input_directory, markdown_output_directory, mermaid_output_directory)
        print("全てのファイルを処理し、入力ディレクトリを空にしました。")
