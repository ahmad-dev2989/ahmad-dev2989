# Script configuration for Ahmad (Roll #24f-0004)
import base64
import urllib.request
import re
import time

def process_svg():
    # Read the original SVG file
    try:
        with open('tech-stack.svg', 'r') as file:
            svg_content = file.read()
    except FileNotFoundError:
        print("Error: Could not find 'tech-stack.svg' in the current directory.")
        return

    # Find all http/https links inside href="..."
    urls = re.findall(r'href="(https?://[^"]+)"', svg_content)
    
    print(f"Found {len(urls)} icons to convert. Processing with rate-limit delays...")

    for url in urls:
        try:
            # Add a User-Agent to bypass blocks from sites like Wikimedia
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
                
            # Determine the correct MIME type
            ext = url.split('.')[-1].split('?')[0].lower()
            mime_type = "image/svg+xml" if ext == "svg" else "image/png"
            
            # Convert to Base64
            b64_data = base64.b64encode(img_data).decode('utf-8')
            data_uri = f"data:{mime_type};base64,{b64_data}"
            
            # Replace the standard URL with the Base64 string in the SVG text
            svg_content = svg_content.replace(url, data_uri)
            print(f" [Success] Converted: {url.split('/')[-1][:20]}...")
            
            # Sleep for 1.5 seconds to prevent 429 Too Many Requests errors
            time.sleep(1.5)
            
        except Exception as e:
            print(f" [Failed] Could not convert {url}\n Error: {e}")
            # If a server gets mad, wait a bit longer before trying the next one
            time.sleep(3)

    # Save the new, GitHub-ready SVG
    with open('tech-stack-ready.svg', 'w') as file:
        file.write(svg_content)
        
    print("\nDone! Upload 'tech-stack-ready.svg' to your repository.")

if __name__ == "__main__":
    process_svg()