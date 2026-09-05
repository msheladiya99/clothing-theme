import os, re, glob

def fix_render(match):
    content = match.group(0)
    # Replace '|' with ',' for arguments
    content = re.sub(r'\|\s*(?=[a-zA-Z0-9_-]+\s*:)', ', ', content)
    # Replace '=' with ':' for arguments
    content = re.sub(r'([a-zA-Z0-9_-]+)\s*=\s*(["\'])', r'\1: \2', content)
    return content

count = 0
for filepath in glob.glob('**/*.liquid', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    content = re.sub(r"{%-\s*when\s*'collection'\s*and\s*collection\.handle\s*-%}", "{%- when 'collection' -%}", content)
    content = re.sub(r"{%\s*when\s*'collection'\s*and\s*collection\.handle\s*%}", "{% when 'collection' %}", content)
    
    content = re.sub(r'{%-?\s*render\s+[^}]+-%}', fix_render, content)
    content = re.sub(r'{%\s*render\s+[^}]+%}', fix_render, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed {filepath}")

print(f"\nFixed {count} files in total.")
