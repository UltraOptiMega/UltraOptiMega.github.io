import os
import re
from datetime import datetime


def define_env(env):
    """自定义宏，用于自动读取 posts 目录并生成文章列表"""

    @env.macro
    def post_list():
        docs_dir = os.path.join(env.project_dir, "docs")
        posts_dir = os.path.join(docs_dir, "posts")

        if not os.path.exists(posts_dir):
            return "_暂无文章_"

        posts = []
        for fname in sorted(os.listdir(posts_dir), reverse=True):
            if not fname.endswith(".md"):
                continue
            f = os.path.join(posts_dir, fname)
            with open(f, encoding="utf-8") as fp:
                content = fp.read()

            # 解析 front matter
            date = ""
            tags = []
            title = fname.replace(".md", "").replace("-", " ").title()

            fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                date_match = re.search(r"date:\s*(.+)", fm)
                if date_match:
                    date = date_match.group(1).strip()
                tag_matches = re.findall(r"-\s+(.+)", fm)
                # 过滤掉 date 行，只取 tags 部分
                in_tags = False
                for line in fm.splitlines():
                    if line.strip().startswith("tags:"):
                        in_tags = True
                        continue
                    if in_tags and line.strip().startswith("- "):
                        tags.append(line.strip()[2:].strip())
                    elif in_tags:
                        break
                title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()

            # 提取第一段正文（# 标题后的第一段非空文本）
            body = content[fm_match.end():] if fm_match else content
            lines = body.strip().splitlines()
            summary = ""
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                summary = line
                break

            rel_path = f"posts/{fname}"
            posts.append({
                "title": title,
                "date": date,
                "tags": tags,
                "summary": summary,
                "path": rel_path,
            })

        if not posts:
            return "_暂无文章_"

        # 按日期排序（新的在前）
        posts.sort(key=lambda p: p["date"], reverse=True)

        # 生成 Markdown
        lines = []
        for p in posts:
            tag_str = " ".join(f"`{t}`" for t in p["tags"])
            date_str = f'\U0001f4c5 {p["date"]}' if p["date"] else ""
            meta = f'{date_str}  \U0001f3f7\ufe0f {tag_str}' if p["tags"] else date_str

            lines.append(f'### [{p["title"]}]({p["path"]})')
            lines.append(meta)
            lines.append("")
            if p["summary"]:
                lines.append(p["summary"])
                lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    @env.macro
    def book_list():
        docs_dir = os.path.join(env.project_dir, "docs")
        books_dir = os.path.join(docs_dir, "books")

        if not os.path.exists(books_dir):
            return "_暂无书籍_"

        books = []
        for fname in sorted(os.listdir(books_dir)):
            if not fname.endswith(".md"):
                continue
            f = os.path.join(books_dir, fname)
            with open(f, encoding="utf-8") as fp:
                content = fp.read()

            title = fname.replace(".md", "").replace("-", " ").title()
            author = ""
            category = "未分类"
            rating = 0
            link = "#"

            fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                for line in fm.splitlines():
                    line = line.strip()
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("author:"):
                        author = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("category:"):
                        category = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("rating:"):
                        try:
                            rating = int(line.split(":", 1)[1].strip())
                        except ValueError:
                            pass
                    elif line.startswith("link:"):
                        link = line.split(":", 1)[1].strip().strip('"')

                # 提取正文摘要
                body = content[fm_match.end():]
                summary = ""
                for line in body.strip().splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    summary = line
                    break
            else:
                summary = ""

            books.append({
                "title": title,
                "author": author,
                "category": category,
                "rating": rating,
                "link": link,
                "summary": summary,
                "fname": fname,
            })

        if not books:
            return "_暂无书籍_"

        # 按分类分组
        categories = {}
        for b in books:
            cat = b["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(b)

        # 生成 Markdown
        stars = "\u2b50"
        lines = []
        for cat, cat_books in categories.items():
            lines.append(f"## {cat}")
            lines.append("")
            for b in cat_books:
                rating_str = stars * b["rating"] if b["rating"] else ""
                local_path = f'books/{b["fname"]}'
                lines.append(f'### [{b["title"]}]({local_path})')
                if b["author"]:
                    lines.append(f"**{b['author']}**")
                lines.append("")
                if b["summary"]:
                    lines.append(b["summary"])
                    lines.append("")
                if rating_str:
                    lines.append(f"!!! info \"推荐指数\"")
                    lines.append(f"    {rating_str}")
                    lines.append("")
                lines.append("---")
                lines.append("")

        return "\n".join(lines)

    @env.macro
    def tag_list():
        """扫描 posts 目录，按标签聚合生成标签页"""
        docs_dir = os.path.join(env.project_dir, "docs")
        posts_dir = os.path.join(docs_dir, "posts")

        if not os.path.exists(posts_dir):
            return "_暂无标签_"

        tag_map = {}  # tag -> list of {title, date, path}
        for fname in sorted(os.listdir(posts_dir)):
            if not fname.endswith(".md"):
                continue
            f = os.path.join(posts_dir, fname)
            with open(f, encoding="utf-8") as fp:
                content = fp.read()

            title = fname.replace(".md", "").replace("-", " ").title()
            date = ""
            tags = []

            fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                date_match = re.search(r"date:\s*(.+)", fm)
                if date_match:
                    date = date_match.group(1).strip()
                in_tags = False
                for line in fm.splitlines():
                    if line.strip().startswith("tags:"):
                        in_tags = True
                        continue
                    if in_tags and line.strip().startswith("- "):
                        tags.append(line.strip()[2:].strip())
                    elif in_tags:
                        break
                title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()

            rel_path = f"posts/{fname}"
            for tag in tags:
                if tag not in tag_map:
                    tag_map[tag] = []
                tag_map[tag].append({"title": title, "date": date, "path": rel_path})

        if not tag_map:
            return "_暂无标签_"

        # 生成 Markdown
        lines = []
        # 标签云
        all_tags = sorted(tag_map.keys())
        cloud = "  ".join(f"`{t}`" for t in all_tags)
        lines.append(f"**所有标签：** {cloud}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 按标签分组列出文章
        for tag in all_tags:
            posts = tag_map[tag]
            posts.sort(key=lambda p: p["date"], reverse=True)
            lines.append(f"## `{tag}`")
            lines.append("")
            for p in posts:
                date_str = f'\U0001f4c5 {p["date"]}' if p["date"] else ""
                lines.append(f'- [{p["title"]}]({p["path"]}) {date_str}')
            lines.append("")

        return "\n".join(lines)
