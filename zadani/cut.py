#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import fitz

doc = fitz.open("plan.pdf")
new_doc = fitz.open()

for page in doc:
    rect = page.rect
    # printable area – dejme tomu margin 25 mm kolem
    margin = 25  # mm
    scale = 72 / 25.4  # mm -> points
    margin_pt = margin * scale
    printable = fitz.Rect(rect.x0 + margin_pt, rect.y0 + margin_pt,
                          rect.x1 - margin_pt, rect.y1 - margin_pt)

    # počet "řádků" a "sloupců" podle A4
    a4_w = 210 * scale
    a4_h = 297 * scale

    x0, y0, x1, y1 = printable
    x1 /= 2
    x = x0
    while x < x1:
        y = y0
        while y < y1:
            clip = fitz.Rect(x, y, min(x + a4_w, x1), min(y + a4_h, y1))
            new_page: fitz.Page = new_doc.new_page(width=a4_w, height=a4_h)
            new_page.show_pdf_page(fitz.Rect(0, 0, a4_w, a4_h), doc, page.number, clip=clip)
            y += a4_h
        x += a4_w

# new_doc.save("plan_cut.pdf") # Use at your own risk.
# Note that this code's 'margin' only crops the input PDF, and it doesn't cut smaller pieces for the pages.
# Use at your own risk. My print turned out pretty well, using this UI (Czech) script, but it's not perfect.
