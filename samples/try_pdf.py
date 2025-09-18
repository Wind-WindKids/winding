#!/usr/bin/env python3
import subprocess
import tempfile
import os
from io import BytesIO

from fpdf import FPDF
from fpdf.enums import OutputIntentSubType
from fpdf.output import PDFICCProfile
from PIL import Image, ImageDraw, ImageCms

class PDFX3(FPDF):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # force PDF 1.3 (no transparency)
        self.pdf_version = "1.3"
        # ensure the “binary comment” immediately after the header
        # so that %PDF-1.3\n%âãÏÓ\n is emitted
        self._put_header = lambda: (
            self._out(f"%PDF-{self.pdf_version}"),
            self._out("%âãÏÓ"),
        )

    def header(self):
        # no page‐header
        pass

def generate_green_square_image(px_width, px_height, square_size):
    img = Image.new("RGB", (px_width, px_height), "white")
    draw = ImageDraw.Draw(img)
    x0 = (px_width - square_size) // 2
    y0 = (px_height - square_size) // 2
    draw.rectangle([x0, y0, x0 + square_size, y0 + square_size], fill=(0, 255, 0))

    # perform a proper ICC‐aware conversion
    srgb = ImageCms.createProfile("sRGB")
    cmyk = ImageCms.ImageCmsProfile("icc/SWOP2006_Coated3v2.icc")
    img_cmyk = ImageCms.profileToProfile(
        img, srgb, cmyk, outputMode="CMYK"
    )

    # embed the raw ICC bytes into the PIL image info so we can carry them through to JPEG
    img_cmyk.info["icc_profile"] = cmyk.tobytes()
    return img_cmyk

def create_pdfx3(img_cmyk, trim_in, bleed_in, raw_pdf_path):
    trim_w, trim_h = trim_in
    page_w = trim_w + bleed_in
    page_h = trim_h + 2 * bleed_in

    pdf = PDFX3(unit="in", format=(page_w, page_h))

    # --- embed your SWOP2006 Coated3 v2 profile as a PDF/X output intent ---
    with open("icc/SWOP2006_Coated3v2.icc", "rb") as f:
        icc = PDFICCProfile(
            contents=f.read(),
            n=4,                     # CMYK = 4 channels
            alternate="DeviceCMYK",  # must match CMYK
        )

    pdf.add_output_intent(
        OutputIntentSubType.PDFX,     # PDF/X (not PDFA)
        "CGATS TR003",                # the “Reference Name” from color.org
        "ISO 12647-2:2004",           # your printing condition
        "http://www.color.org",       # registry
        icc,                          # the PDFICCProfile object
        "SWOP2006 Coated3 v2",        # human‐readable description
    )

    # --- minimal metadata + XMP (so you get /Metadata in catalog) ---
    #pdf.set_title("PDF/X-3 CMYK Test")
    #pdf.set_author("Wind")
    #pdf.set_subject("SWOP2006 Coated3 v2 OutputIntent")
    #pdf.set_creator("Wind Script")
    #pdf.set_xmp_metadata()       # injects the Metadata stream with Subtype /XML

    pdf.add_page()

    # rasterize the CMYK image out to an in-memory JPEG with embedded ICC
    buf = BytesIO()
    img_cmyk.save(
        buf,
        format="JPEG",
        icc_profile=img_cmyk.info["icc_profile"],
        quality=100,
    )
    buf.seek(0)

    # place it flush at the binding edge
    pdf.image(buf, x=0, y=bleed_in, w=trim_w, h=trim_h, type="JPG")

    pdf.output(raw_pdf_path)
    print(f"Written PDF/X-3 to {raw_pdf_path}")

if __name__ == "__main__":
    img = generate_green_square_image(400, 300, 150)
    create_pdfx3(img, trim_in=(6, 4), bleed_in=0.125, raw_pdf_path="out_pdfx3.pdf")
