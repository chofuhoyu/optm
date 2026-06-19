"""浏览器登录并下载 PPTX 文件。

使用方式:
  uv run python scripts/download_pptx.py

流程:
  1. 启动 Chrome 浏览器
  2. 你在浏览器中登录、导航到课件页面
  3. 回到终端按 Enter
  4. 脚本分析页面 + 网络请求，找到 PPTX 并下载

每次进入时会打开更多入口：
  1 = 扫描当前页面 PPTX 链接
  2 = 高亮可能的下载按钮
  3 = 监听后续点击（拦截下载）
  4 = 查看页面结构（调试用）
  5 = 执行自定义 JS
  0 = 退出
"""

import sys
import os
import json
import re
from pathlib import Path


def main():
    from playwright.sync_api import sync_playwright

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_data_dir = os.path.join(project_root, "chrome_profile")
    material_dir = os.path.join(project_root, "material")
    os.makedirs(material_dir, exist_ok=True)

    captured_pptx_links = []  # 从网络请求中捕获的 pptx 链接

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        # ======== 监听网络请求，捕获 PPTX 相关 ========
        def on_response(response):
            url = response.url.lower()
            if any(ext in url for ext in [".pptx", ".ppt", "pptx", "download"]):
                content_type = response.headers.get("content-type", "")
                info = {
                    "url": response.url,
                    "content_type": content_type,
                    "status": response.status,
                    "headers": dict(response.headers),
                }
                if info not in captured_pptx_links:
                    captured_pptx_links.append(info)
                    print(f"  [网络] 捕获: {response.url[:120]}")

        page.on("response", on_response)

        # ======== 导航 ========
        start_url = "https://ucloud.bupt.edu.cn/uclass/course.html"
        print(f"打开: {start_url}")
        page.goto(start_url, wait_until="domcontentloaded", timeout=30000)
        print()
        print("=" * 60)
        print("  请在浏览器中:")
        print("  1. 登录（如果需要）")
        print("  2. 导航到包含 PPTX 课件下载的页面")
        print("=" * 60)
        print()
        print("完成后回到终端，我将帮你探索和下载。")
        print()

        # ======== 交互菜单 ========
        while True:
            print()
            print("-" * 40)
            print("  1 = 扫描当前页面 <a> 链接（找 .pptx）")
            print("  2 = 高亮可能的下载按钮（红色边框）")
            print("  3 = 监听模式：你点下载，我拦截保存")
            print("  4 = 查看页面 HTML 结构（前5000字符）")
            print("  5 = 执行自定义 JavaScript")
            print("  6 = 查看捕获的网络请求")
            print("  7 = 用 fetch+referer 尝试批量下载网络请求中的 PPTX")
            print("  0 = 退出")
            print("-" * 40)

            choice = input("> ").strip()

            if choice == "0":
                break

            elif choice == "1":
                # 扫描页面 <a> 标签
                links_data = page.evaluate("""
                    Array.from(document.querySelectorAll('a, [href]')).map(el => ({
                        href: el.href || el.getAttribute('href') || '',
                        text: (el.textContent || '').trim().slice(0, 80),
                        tag: el.tagName
                    }))
                """)
                pptx_matches = [l for l in links_data if ".pptx" in l["href"].lower()]
                print(f"\n  页面共 {len(links_data)} 个链接，其中 {len(pptx_matches)} 个含 .pptx:")
                for i, link in enumerate(pptx_matches, 1):
                    print(f"  [{i}] {link['text'][:60]}")
                    print(f"      {link['href'][:150]}")

                if not pptx_matches:
                    print("  未找到直接 .pptx 链接。试试选项 2 或 3。")

                # 下载流
                if pptx_matches:
                    ans = input(f"\n  输入要下载的编号 (1-{len(pptx_matches)}) 或 'all' / 回车跳过: ").strip()
                    if ans.lower() == "all":
                        to_download = pptx_matches
                    elif ans.isdigit():
                        idx = int(ans) - 1
                        to_download = [pptx_matches[idx]] if 0 <= idx < len(pptx_matches) else []
                    else:
                        to_download = []

                    for link in to_download:
                        href = link["href"]
                        if href.startswith("//"):
                            href = "https:" + href
                        elif href.startswith("/"):
                            parsed = page.evaluate("window.location.origin")
                            href = parsed + href

                        fname = link["text"].strip() if link["text"].strip() else f"download_{link['href'].split('/')[-1]}"
                        fname = re.sub(r'[\\/:*?"<>| ]', '_', fname)
                        if not fname.endswith(".pptx"):
                            fname += ".pptx"
                        fpath = os.path.join(material_dir, fname)

                        try:
                            with page.expect_download(timeout=30000) as di:
                                page.evaluate(f"""
                                    const links = document.querySelectorAll('a, [href]');
                                    for (const l of links) {{
                                        if ((l.href || l.getAttribute('href')) === '{href}') {{
                                            l.click();
                                            break;
                                        }}
                                    }}
                                """)
                            download = di.value
                            download.save_as(fpath)
                            print(f"  ✓ 下载: {fname} ({os.path.getsize(fpath)/1024:.0f} KB)")
                        except Exception as e:
                            print(f"  ✗ 失败: {e}")

            elif choice == "2":
                # 高亮可能的下载按钮
                page.evaluate("""
                    document.querySelectorAll('a, button, [role="button"], [onclick], span, div, li').forEach(el => {
                        const txt = (el.textContent || '').toLowerCase();
                        const href = (el.href || el.getAttribute('href') || '').toLowerCase();
                        const onclick = (el.getAttribute('onclick') || '').toLowerCase();
                        if (txt.includes('.pptx') || txt.includes('.ppt') ||
                            href.includes('.pptx') || href.includes('.ppt') ||
                            txt.includes('下载') || txt.includes('download') ||
                            onclick.includes('download')) {
                            el.style.outline = '3px solid red';
                            el.style.outlineOffset = '2px';
                            el.title = '可能可下载: ' + txt.slice(0, 50);
                        }
                    })
                """)
                print("  已为可能的下载元素标记红色边框。在浏览器中查看。")

            elif choice == "3":
                # 监听模式
                print("  监听模式开启。请在浏览器中点击下载链接/按钮...")
                print("  按 Ctrl+C 停止监听")
                print()
                already = len(os.listdir(material_dir))
                try:
                    while True:
                        try:
                            with page.expect_download(timeout=120000) as di:
                                pass  # just wait
                        except Exception:
                            pass
                        else:
                            download = di.value
                            fname = download.suggested_filename
                            fpath = os.path.join(material_dir, fname)
                            download.save_as(fpath)
                            print(f"  ✓ 拦截下载: {fname} ({os.path.getsize(fpath)/1024:.0f} KB)")
                except KeyboardInterrupt:
                    new_count = len(os.listdir(material_dir)) - already
                    print(f"\n  监听结束。新增 {new_count} 个文件。")

            elif choice == "4":
                # 查看页面结构
                html = page.content()
                print(f"\n  页面 HTML ({len(html)} 字符)，前5000字符:")
                print(html[:5000])
                # 也打印 iframe
                frames = page.frames
                print(f"\n  共 {len(frames)} 个 frame")
                for i, f in enumerate(frames):
                    print(f"  Frame[{i}]: {f.url[:120]}")

            elif choice == "5":
                # 执行自定义 JS
                js = input("  输入 JavaScript 代码: ").strip()
                if js:
                    try:
                        result = page.evaluate(js)
                        print(f"  结果: {result}")
                    except Exception as e:
                        print(f"  错误: {e}")

            elif choice == "6":
                # 查看捕获的网络请求
                print(f"\n  捕获 {len(captured_pptx_links)} 个 PPTX 相关请求:")
                for i, info in enumerate(captured_pptx_links, 1):
                    print(f"  [{i}] {info['status']} {info['content_type'][:40]}")
                    print(f"      {info['url'][:150]}")

            elif choice == "7":
                # 批量下载网络请求中的 PPTX
                pptx_urls = [c for c in captured_pptx_links
                            if ".pptx" in c["url"].lower() or
                            "powerpoint" in c["content_type"] or
                            "vnd.openxmlformats" in c["content_type"]]
                if not pptx_urls:
                    print("  网络请求中未发现 PPTX。先回浏览器点击下载链接，再试。")
                else:
                    print(f"\n  尝试下载 {len(pptx_urls)} 个 PPTX...")
                    for i, info in enumerate(pptx_urls, 1):
                        fname = info["url"].split("/")[-1].split("?")[0]
                        if not fname.endswith(".pptx"):
                            fname = f"captured_{i}.pptx"
                        fname = re.sub(r'[\\/:*?"<>| ]', '_', fname)
                        fpath = os.path.join(material_dir, fname)

                        try:
                            import requests as req
                            cookies = {c["name"]: c["value"] for c in context.cookies()}
                            ua = page.evaluate("navigator.userAgent")
                            resp = req.get(info["url"], cookies=cookies,
                                          headers={"User-Agent": ua, "Referer": page.url},
                                          timeout=60)
                            resp.raise_for_status()
                            with open(fpath, "wb") as f:
                                f.write(resp.content)
                            print(f"  ✓ [{i}] {fname} ({len(resp.content)/1024:.0f} KB)")
                        except Exception as e:
                            print(f"  ✗ [{i}] {fname}: {e}")

        context.close()
        print(f"\n退出。浏览器已关闭。")


if __name__ == "__main__":
    main()
