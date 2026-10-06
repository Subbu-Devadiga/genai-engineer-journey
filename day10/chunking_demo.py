document="""
Normal changes follow the standard change management process.

They should be reviewed for risk, impact, implementation steps,
validation activities, and rollback procedures before implementation.

Production changes should include validation activities such as
application health checks, functional testing, monitoring, log
verification, transaction testing, and confirmation that the
expected business functionality is working.

After successful implementation, the change should be reviewed
for completion. Implementation results, validation results,
incidents, issues, and required documentation should be recorded
before closure.
"""

def chunk_text(text,chunk_size=100,overlap=10):
    
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk.strip())
        start=end-overlap

    return chunks

chunks=chunk_text(document)

print("Number of chunks:",len(chunks))

for i,chunk in enumerate(chunks):
    print(f"\n---Chunk {i+1}----")
    print(chunk)
