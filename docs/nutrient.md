

-----

### **1. Basic File Conversion**

This script reads a local `.docx` file, uploads it, and saves the resulting PDF.

```python
import requests

# Configuration
API_KEY = "YOUR_API_KEY_HERE"
INPUT_FILE = "contract.docx"
OUTPUT_FILE = "contract.pdf"
ENDPOINT = "https://api.nutrient.io/processor/convert_to_pdf"

def convert_word_to_pdf():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        # Strict content type is required for raw binary upload
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    try:
        print(f"Uploading {INPUT_FILE}...")
        
        with open(INPUT_FILE, "rb") as f:
            response = requests.post(ENDPOINT, headers=headers, data=f)

        if response.status_code == 200:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            print(f"Success! Saved to {OUTPUT_FILE}")
        
        elif response.status_code == 401:
            print("Error: Invalid API Key.")
        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_word_to_pdf()
```

-----

### **2. In-Memory Conversion (Flask/FastAPI/Django)**

If you are building a web server, you likely want to handle the file in memory (using `BytesIO`) without saving it to disk first.

```python
import requests
import io

def convert_stream_to_pdf(file_stream, api_key):
    """
    Takes a file-like object (bytes) and returns the PDF bytes.
    """
    url = "https://api.nutrient.io/processor/convert_to_pdf"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    # Ensure stream is at the beginning
    file_stream.seek(0)
    
    response = requests.post(url, headers=headers, data=file_stream)
    
    if response.status_code == 200:
        return response.content # Returns raw PDF bytes
    else:
        raise Exception(f"Conversion failed: {response.text}")

# Example usage with a local file masquerading as a stream
with open("report.docx", "rb") as f:
    # 'f' acts as the file stream here
    pdf_bytes = convert_stream_to_pdf(f, "YOUR_API_KEY")
    
    # Do something with the bytes (e.g., return to user in Flask)
    with open("report_memory.pdf", "wb") as out:
        out.write(pdf_bytes)
```

-----

### **3. Async Conversion (Batch Processing)**

If you need to convert many documents at once, using `aiohttp` is significantly faster than standard `requests` because it doesn't block while waiting for the server.

```bash
pip install aiohttp
```

```python
import aiohttp
import asyncio

API_KEY = "YOUR_API_KEY"

async def convert_file(session, file_path):
    url = "https://api.nutrient.io/processor/convert_to_pdf"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    print(f"Starting: {file_path}")
    
    # Read file asynchronously
    with open(file_path, 'rb') as f:
        file_data = f.read()

    async with session.post(url, headers=headers, data=file_data) as response:
        if response.status == 200:
            result_data = await response.read()
            output_name = file_path.replace(".docx", ".pdf")
            
            with open(output_name, 'wb') as f_out:
                f_out.write(result_data)
            print(f"Finished: {output_name}")
        else:
            print(f"Failed: {file_path} (Status: {response.status})")

async def main():
    files_to_convert = ["doc1.docx", "doc2.docx", "doc3.docx"]
    
    async with aiohttp.ClientSession() as session:
        tasks = [convert_file(session, f) for f in files_to_convert]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

### **Common Troubleshooting**

  * **HTTP 415 (Unsupported Media Type):** This usually means you forgot the `Content-Type` header or set it to `application/json` instead of the Word MIME type.
  * **Timeouts:** Large documents may take time to render. If using `requests`, you can add a timeout parameter: `requests.post(..., timeout=30)`.

**Would you like an example of how to implement this inside a specific framework like Flask or FastAPI?**
