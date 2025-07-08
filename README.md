# PDF Duplex Merger

This tool helps you efficiently digitize double-sided documents using a simple scanner with an automatic feeder **without a duplex unit**. It merges your scanned front and back pages into a correctly ordered PDF.

---

## Scanning Workflow

1. **Scan All Front Sides (Odd Pages)**
    - Place the entire stack in your scanner’s automatic feeder with page 1 facing up.
    - Scan all front sides. The resulting PDF will contain pages in this order: 1, 3, 5, 7, ...

2. **Flip the Stack and Scan All Back Sides (Even Pages)**
    - Flip the stack so that the back sides are now facing up, keeping the page order.
    - Scan again. The resulting PDF will contain the back sides in reverse order: last page, next-to-last, ..., 2.

3. **Result**
    - You will have two PDFs:
        - **Fronts:** All odd pages, starting with page 1.
        - **Backs:** All even pages, starting with the last page and ending with page 2.

---

## How to Use

1. **Add Two PDF Files**
    - Drag and drop both PDFs (fronts and backs) into the program window  
      *or*  
      use the "Add Files" button to select them.

2. **Start Merging**
    - Double-click the file in the list that contains the front pages.  
      The tool will automatically detect which file contains the back pages.

3. **Result**
    - The two PDFs will be merged so that the pages are correctly interleaved:  
      1, 2, 3, 4, 5, 6, ...

4. **Output Filename and Location**
    - The merged PDF will be named `Fronts_Backs.pdf` (using your actual filenames)  
      and saved in the same folder as the front pages file.


## 🛠 Requirements

- Python 3
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [tkinterdnd2](https://pypi.org/project/tkinterdnd2/) (for drag & drop support)
- Tkinter (included with standard Python installations)

### Install dependencies
pip install -r requirements.txt

