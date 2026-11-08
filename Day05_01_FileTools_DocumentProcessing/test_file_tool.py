"""
Day05_01_FileTools_DocumentProcessing: a quick manual test that uses the
`read_text_file` tool to load a sample notes file from disk and print its
contents, demonstrating how an agent could read a document before processing
it further.
"""

from tools import read_text_file

# Read the sample notes file using our file tool.
text = read_text_file("data/notes.txt")

# Print the file's contents to verify it loaded correctly.
print(text)
