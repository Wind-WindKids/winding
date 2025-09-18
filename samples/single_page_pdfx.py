#!/usr/bin/env python3
import subprocess
import tempfile
import os
from io import BytesIO
from fpdf import FPDF
from fpdf.enums import OutputIntentSubType
from fpdf.output import PDFICCProfile
from PIL import Image, ImageDraw, ImageCms

import sys
from datetime import datetime
import pikepdf

from fpdf import FPDF_VERSION

def generate_green_square_image(px_width, px_height, square_size, dpi):
    """
    Create an RGB image with a centered green square, convert to CMYK JPEG in-memory.
    """
    # 1. Draw RGB image
    img = Image.new("RGB", (px_width, px_height), "white")
    draw = ImageDraw.Draw(img)
    x0 = (px_width - square_size) // 2
    y0 = (px_height - square_size) // 2
    draw.rectangle([x0, y0, x0 + square_size, y0 + square_size], fill=(0, 255, 0))

    srgb = ImageCms.createProfile("sRGB")
    cmyk = ImageCms.ImageCmsProfile("icc/SWOP2006_Coated3v2.icc")
    img_cmyk = ImageCms.profileToProfile(img, srgb, cmyk, outputMode="CMYK")

    return img_cmyk

def create_raw_pdf(img_cmyk, trim_in, bleed_in, dpi, raw_pdf_path):
    """
    Create a single-page PDF with no inside (binding) bleed,
    embedding the CMYK JPEG image.
    """
    # Compute page size: width = trim + outer bleed; height = trim + top & bottom bleed
    trim_w, trim_h = trim_in
    page_w = trim_w + bleed_in
    page_h = trim_h + 2 * bleed_in

    pdf = FPDF(unit="in", format=(page_w, page_h))

    #icc_profile = img_cmyk.info.get("icc_profile")
    #print("ICC Profile:", icc_profile)
    #return


    # 1. Read your CMYK ICC profile
    with open("icc/SWOP2006_Coated3v2.icc", "rb") as icc_file:
        icc_profile = PDFICCProfile(
            contents=icc_file.read(),
            n=4,                      # CMYK has 4 components, not 3
            alternate="DeviceCMYK"    # the alternate color space must be CMYK
        )

    # 2. Embed it as the PDF/X output intent
    pdf.add_output_intent(
        OutputIntentSubType.PDFX,
        "CGATS TR003",                 # the Profile ID / reference name
        "ISO 12647-2:2004",            # the printing condition
        "http://www.color.org",        # registry
        icc_profile,                   # your PDFICCProfileObject
        "SWOP2006 Coated 3 v2"         # a human‐readable description
    )

    #pdf.allow_images_transparency = False
    author, title = "Wind", "PDF/X Test"
    pdf.set_title(title)
    pdf.set_lang("en-US")
    #pdf.set_subject("PDF/X Test")
    pdf.set_author(author)
    #pdf.set_keywords("PDF/X, test")
    #pdf.set_producer("Acrobat Distiller")
    pdf.set_creator(author)

    
    pdf.add_page()

    # Place image flush to the binding edge (left side), bleed on right/top/bottom
    x = 0
    y = bleed_in
    w = trim_w
    h = trim_h

    pdf.image(img_cmyk, x=x, y=y, w=w, h=h)
    pdf.output(raw_pdf_path)
    print(f"Generated raw PDF: {raw_pdf_path}")

    with pikepdf.open(raw_pdf_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = "Title"
            meta["dc:language"] = "en-US"
            meta["dc:creator"] = [author]
            #meta["dc:description"] = "Description"
            #meta["dc:subject"] = "keyword1 keyword2 keyword3"
            #meta["pdf:Keywords"] = "keyword1 keyword2 keyword3"
            #meta["pdf:Producer"] = f"py-pdf/fpdf{FPDF_VERSION}"
            meta["xmp:CreatorTool"] = __file__
            meta["xmp:CreateDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()
        pdf.save()



def convert_to_pdfx(raw_pdf, final_pdf, icc_profile_path, pdfx_standard="PDF/X-3:2002"):
    """
    Use Ghostscript to convert raw_pdf → PDF/X-3–compliant final_pdf.
    Requires Ghostscript (gs) and a CMYK ICC profile on disk.
    """
    # 1. Create a tiny pdfmarks file that declares GTS_PDFXVersion
    pdfmarks = f"""%!
% PDF/X OutputIntent declaration
[/_objdef {{OutputIntent}} /type /dict /OBJ pdfmark
[ OutputIntent <<
   /Type /OutputIntent
   /S /GTS_PDFX
   /GTS_PDFXVersion ({pdfx_standard})
   /OutputConditionIdentifier (SWOP2006 Coated3v2)
   /RegistryName (http://www.color.org)
   /DestOutputProfile ({icc_profile_path})
>> /PUT pdfmark
]
"""
    with tempfile.NamedTemporaryFile("w", suffix=".pdfmarks", delete=False) as pm:
        pm.write(pdfmarks)
        pm_path = pm.name

    gs_cmd = [
        "gs",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=pdfwrite",
        #"-dCompatibilityLevel=1.3",        # PDF 1.3 => no transparency
        #"-dPDFX=1",                        # produce PDF/X-3
        #"-sProcessColorModel=DeviceCMYK",
        #"-sColorConversionStrategy=CMYK",
        "-sOutputICCProfile=/tmp/icc/SWOP2006_Coated3v2.icc",  # use your embedded SWOP ICC
        "-dPreserveOutputIntents",         # keep FPDF’s /OutputIntent as-is
        #"-dEmbedAllFonts=true",
        #"-dSubsetFonts=true",
        f"-sOutputFile={final_pdf}",
        raw_pdf
    ]
    print("Running Ghostscript:", " ".join(gs_cmd))
    subprocess.run(gs_cmd, check=True)
    #os.remove(pm_path)
    print(f"✅ PDF/X-3 written to {final_pdf}")



if __name__ == "__main__":
    # Settings
    TRIM = (4.0, 6.0)           # inches
    BLEED = 0.125               # inches (outer/top/bottom only)
    DPI = 300
    RAW_PDF = "single_raw.pdf"
    FINAL_PDF = "single_pdfx.pdf"
    ICC_PROFILE = "icc/SWOP2006_Coated3v2.icc"     # must exist in CWD
    PDFX_STANDARD = "PDF/X-1a:2001"

    # 1) Generate in-memory CMYK JPEG of a green square
    px_w = int(TRIM[0] * DPI)
    px_h = int(TRIM[1] * DPI)
    square_px = min(px_w, px_h) // 2
    img_cmyk = generate_green_square_image(px_w, px_h, square_px, DPI)

    # 2) Create the raw PDF
    create_raw_pdf(img_cmyk, TRIM, BLEED, DPI, RAW_PDF)

    # 3) Convert to PDF/X-compliant file
    #convert_to_pdfx(RAW_PDF, FINAL_PDF, ICC_PROFILE)#, PDFX_STANDARD)

    # Clean up
    #os.remove(RAW_PDF)
