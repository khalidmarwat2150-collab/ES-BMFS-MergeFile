import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os

st.set_page_config(page_title="PDF Page Merger", layout="centered")

st.title("📄 PDF Page-by-Page Merger")
st.write("Merge two PDFs alternately (Page1+Page1, Page2+Page2...)")

# Upload files
file1 = st.file_uploader("Upload First PDF", type=["pdf"])
file2 = st.file_uploader("Upload Second PDF", type=["pdf"])

if file1 and file2:

    st.success("✅ Both files uploaded")

    # Save uploaded files temporarily
    temp_dir = tempfile.mkdtemp()

    file1_path = os.path.join(temp_dir, "file1.pdf")
    file2_path = os.path.join(temp_dir, "file2.pdf")

    with open(file1_path, "wb") as f:
        f.write(file1.read())

    with open(file2_path, "wb") as f:
        f.write(file2.read())

    # Read PDFs
    reader1 = PdfReader(file1_path)
    reader2 = PdfReader(file2_path)

    writer = PdfWriter()

    pages1 = len(reader1.pages)
    pages2 = len(reader2.pages)

    max_pages = max(pages1, pages2)

    # Merge alternately
    for i in range(max_pages):

        if i < pages1:
            writer.add_page(reader1.pages[i])

        if i < pages2:
            writer.add_page(reader2.pages[i])

    # Save merged file
    output_path = os.path.join(temp_dir, "merged.pdf")

    with open(output_path, "wb") as f:
        writer.write(f)

    # Read for download
    with open(output_path, "rb") as f:
        merged_bytes = f.read()

    st.success("🎉 Merge completed!")

    # Download button
    st.download_button(
        label="⬇️ Download Merged PDF",
        data=merged_bytes,
        file_name="merged.pdf",
        mime="application/pdf"
    )

else:
    st.info("Please upload both PDF files to continue.")
