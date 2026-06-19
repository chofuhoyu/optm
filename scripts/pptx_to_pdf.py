"""将 material/ 下所有 PPTX 转成 PDF（1:1 页数对应）"""
import os
import sys
import io
import win32com.client

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def main():
    material = os.path.join(os.path.dirname(os.path.dirname(__file__)), "material")
    pptx_files = sorted([f for f in os.listdir(material) if f.endswith(".pptx")])

    if not pptx_files:
        print("material/ 下无 PPTX 文件")
        return

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    try:
        ppt.Visible = False
    except Exception:
        ppt.WindowState = 2  # minimized

    try:
        for name in pptx_files:
            pptx_path = os.path.join(material, name)
            pdf_name = name.replace(".pptx", ".pdf")
            pdf_path = os.path.join(material, pdf_name)

            if os.path.exists(pdf_path):
                print(f"  跳过 {name}（已有 PDF）")
                continue

            try:
                pres = ppt.Presentations.Open(pptx_path, ReadOnly=True)
                pres.SaveAs(pdf_path, 32)  # 32 = ppSaveAsPDF
                pres.Close()
                # 核对页数
                from pptx import Presentation
                prs = Presentation(pptx_path)
                pptx_pages = len(prs.slides)
                import fitz
                doc = fitz.open(pdf_path)
                pdf_pages = doc.page_count
                doc.close()
                match = "✓" if pptx_pages == pdf_pages else f"✗ PPTX={pptx_pages} PDF={pdf_pages}"
                print(f"  {match}  {pdf_name}")
            except Exception as e:
                print(f"  ✗ {name}: {e}")

    finally:
        ppt.Quit()

    # 统计
    pdfs = [f for f in os.listdir(material) if f.endswith(".pdf")]
    print(f"\n共 {len(pdfs)} 个 PDF")


if __name__ == "__main__":
    main()
