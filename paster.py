"""Input to help with addition of documents to supabase"""
import time
from build_supabase import segment_write_to_supabase
end_text = "/stop"
confirm_text = "OK"
running = True
data = []
while running:
    content = input("Document Content: ")
    if content == end_text:
        running = False
        break
    time.sleep(1)
    source = input("Document Source: ")
    if source == end_text:
        running = False
        break
    content = {"content": content, "source": source}
    data.append(content)

print("===========")
print("S/N", "\t", "CONTENT", "\t", "SOURCE")
for idx, row in enumerate(data):
    doc = row["content"]
    src = row["source"]
    print(f"{idx+1}.", "\t", f"{doc[:20]}...", "\t", f"{source[:20]}...")
print("===========\n\n")
response = input("Check content above, if correct write 'OK': ")

if response == confirm_text:
    print("Writing to Supabase Now...")
    segment_write_to_supabase(data)
    print("Done!")
