import re
from pathlib import Path

def normalize_front_matter(path: Path):
    text = path.read_text(encoding='utf-8')

    # 去掉 BOM 和文首空白
    text2 = text.lstrip("\ufeff\r\n")

    # 如果没有 front matter，就不处理
    if not text2.startswith('---'):
        return False

    lines = text2.splitlines(keepends=True)

    # 第一行规范为 '---\n'
    lines[0] = '---\n'

    # 找到闭合分隔线，规范为 '---\n'
    for i in range(1, min(len(lines), 200)):  # 只在前 200 行内找，避免卡大文件
        if lines[i].strip() == '---':
            lines[i] = '---\n'
            break

    fixed = ''.join(lines)
    if fixed != text:
        path.write_text(fixed, encoding='utf-8')
        return True
    return False

# 用法：遍历 _posts 目录
posts_dir = Path("_posts")
for p in posts_dir.glob("*.md"):
    if normalize_front_matter(p):
        print("已修复：", p)
