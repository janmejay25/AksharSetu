# 📚 Akshar Setu — Gujarati OCR

**Akshar Setu** is a local web application for extracting Gujarati text from printed PDF documents and images using the project's bundled Indic-OCR model.

Upload a document, choose the PDF page range, run OCR, review the extracted Gujarati text, and export the results as **TXT**, **Word (`.docx`)**, or **JSON**.

> **Model note:** This repository is intended to include the model in `finetuned-model/`. The app uses the local `IndicOCR` API and does **not** fall back to Tesseract. The model folder must contain the model's inference code and required model files, not only weights.

## Features

- **Local OCR:** runs the bundled Indic-OCR model on your machine.
- **PDF and image input:** supports PDF, PNG, JPG/JPEG, TIFF, BMP, and WEBP.
- **Page-range selection:** choose an inclusive starting and ending page for PDFs.
- **Live processing status:** displays completed pages, progress, current page, and elapsed time.
- **Gujarati Unicode output:** preserves Gujarati text in the extracted results.
- **Three export formats:**
  - **TXT** — plain text, saved as UTF-8 with BOM for compatibility with Windows text editors.
  - **Word (`.docx`)** — editable document with page headings.
  - **JSON** — structured output containing the source filename, combined extracted text, and page-by-page results.
- **Page-by-page review:** open the collapsed page-results section when you need detailed results.
- **Scrollable output panel:** read long OCR results without making the entire page grow.
- **System-aware appearance:** the interface styles respond to the operating system's light/dark preference.
- **Local favicon support:** add `assets/favicon.png` to customize the browser tab icon.

## Demo screenshots

Add screenshots of your running app to the `screenshots/` folder, then update the image paths below if your filenames differ.

### Main interface

![Akshar Setu main interface](screenshots/main-interface.png)

### OCR processing

![Akshar Setu OCR processing progress](screenshots/processing-progress.png)

### Extracted text and downloads

![Gujarati text output and TXT, Word, JSON download options](screenshots/extracted-text-downloads.png)

### Page-by-page JSON results

![Page-by-page OCR results](screenshots/page-by-page-results.png)

> These are image placeholders until you add your own screenshots. Capture them from the app running locally; do not commit screenshots containing private documents or personal information.

## Project structure

The repository should look similar to this:

```text
akshar-setu/
├── app.py
├── requirements.txt
├── README.md
├── finetuned-model/
│   ├── indic_ocr/              # Expected if supplied by the model repository
│   ├── config.json             # Example; exact files depend on the model
│   ├── ...                     # Model weights, tokenizer/processor and other files
├── assets/
│   └── favicon.png             # Optional
└── screenshots/
    ├── main-interface.png
    ├── processing-progress.png
    ├── extracted-text-downloads.png
    └── page-by-page-results.png
```

The exact contents of `finetuned-model/` depend on the Indic-OCR model version. Keep the model's required Python package and supporting files together with its weights.

## Requirements

- Windows 10/11, Linux, or macOS
- Python **3.11 or 3.12** recommended
- Git
- Enough disk space and RAM for the model and OCR workload
- A compatible NVIDIA GPU is optional; CPU inference may be slower

Python dependencies are listed in [`requirements.txt`](requirements.txt), including Gradio, PyTorch, PyMuPDF, Pillow, Transformers, and `python-docx`.

## 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL with your actual GitHub repository URL.

**Model included in the repository:** if `finetuned-model/` has been committed and pushed successfully, you should not need to download the model separately. Wait for Git to finish downloading the repository before continuing.

## 2. Create and activate a virtual environment

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

### Linux or macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3. Install PyTorch and project dependencies

Install a PyTorch build appropriate for your machine and operating system. For NVIDIA GPU support, select the matching command from the official [PyTorch installation selector](https://pytorch.org/get-started/locally/).

Then install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

If installation fails, check that your Python version is supported and consult the package's official installation instructions.

## 4. Configure the bundled model path

The application loads the model through:

```python
from indic_ocr import IndicOCR
model = IndicOCR.from_pretrained(model_dir)
result = model.parse(image_path)
```

```

Alternatively, set the environment variable to your model directory.

**Windows PowerShell:**

```powershell
$env:INDIC_OCR_MODEL_PATH = "$PWD\finetuned-model"
```

**Linux/macOS:**

```bash
export INDIC_OCR_MODEL_PATH="$PWD/finetuned-model"
```

The directory must include the `indic_ocr` package and every file required by `IndicOCR.from_pretrained()`. If the model uses a different layout, update the model-loading adapter to match the model's official inference instructions. Do not enable remote/custom code unless you trust the code being loaded.

## 5. Run the application

From the project root, with the virtual environment activated:

```bash
python app.py
```

Open the local address printed in the terminal. It is commonly:

```text
http://127.0.0.1:7860
```

The application is served locally by Gradio.

## How to use Akshar Setu

1. Open the local web address in your browser.
2. Upload **one PDF or image**.
3. For a PDF, check the detected page count and choose the starting and ending pages. Page numbers start at **1** and the ending page is included.
4. Click **Extract Gujarati text**.
5. Follow the progress, completed-page count, and elapsed time in the processing section.
6. Read or scroll through the extracted Gujarati text.
7. Download the result as TXT, Word, or JSON.
8. Expand **Show page-by-page results** if you want to inspect the structured results for individual pages.

For an image, page-range controls are not needed; the image is treated as one page.

## JSON output

The JSON export contains document-level metadata and a `pages` array. Each page result includes fields such as:

- `file` — source filename
- `page` — page number
- `characters` — number of extracted characters
- `text` — OCR text for that page

The JSON also includes `source_file`, `total_pages_processed`, `total_characters`, and `extracted_text`. Gujarati characters are written directly as Unicode (`ensure_ascii=False`).

## Optional: change the favicon

Create an `assets/` directory beside `app.py` and put your icon here:

```text
assets/favicon.png
```

Use a square PNG (for example, 64 × 64 pixels). Restart the app after adding or changing the file. The app uses this icon if the file exists and its launch configuration points to it.

## Model and GitHub storage notes

This project expects the model to be available locally in `finetuned-model/`. Before publishing, make sure you have the right to redistribute the model files and any included code or training artifacts.

GitHub blocks regular Git files larger than **100 MB**. If any model file exceeds that limit, use [Git LFS](https://git-lfs.com/) and follow GitHub's [large-file documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files). Ensure your repository's LFS storage and bandwidth limits are sufficient. Do not assume a model was uploaded just because its folder exists on your computer—verify the files appear in the GitHub repository.

For very large model artifacts, Git LFS or a dedicated model-storage service may be necessary. If you want users to clone the repo and receive the model automatically, verify that the model files are actually tracked and downloadable through your repository setup.

## Troubleshooting

### Model folder does not exist

- Confirm `finetuned-model/` exists next to `app.py`.
- Confirm `MODEL_PATH` or `INDIC_OCR_MODEL_PATH` points to that directory.
- Ensure the folder was pushed to GitHub and downloaded when cloning.

### `Could not import IndicOCR`

- Check that the `indic_ocr` package is inside the configured model directory, or that the module is installed and importable.
- Verify the model repository's own dependencies are installed.
- Confirm the directory layout matches the model's inference instructions.

### Model initialization fails

- Check that all model weights, configuration, processor/tokenizer files, and supporting files are present.
- Confirm PyTorch and other dependencies are compatible with the model.
- If the model requires a specific inference adapter, use the model's official instructions rather than replacing the OCR engine with another one.

### OCR is slow

- CPU inference may be significantly slower than a compatible GPU.
- For NVIDIA GPUs, install a compatible CUDA-enabled PyTorch build and verify GPU availability using the official PyTorch guidance.

### Gujarati text looks incorrect

- OCR quality depends on scan clarity, page layout, font, resolution, and the model's training data.
- Try a clean, high-resolution scan with readable printed text.
- Review the page-by-page output to identify pages where recognition failed.

## Privacy

Files are processed by the application running on your machine. This project does not intentionally send uploaded documents to a remote OCR service. Model libraries may have their own behavior depending on configuration; use local model files and inspect dependencies if strict offline operation is required.

## Technology

- [Gradio](https://www.gradio.app/)
- [PyTorch](https://pytorch.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Pillow](https://pillow.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)

## License

Add the license that applies to your application code and model. Do not assume the model license is the same as the app's license; check the source model's terms before redistributing it.
