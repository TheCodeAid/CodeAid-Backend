import re
def cleanContent(content: str) -> str:
    # 1. Remove actual escape characters (newline, tab, etc.)
    content = re.sub(r'[\n\r\t\f\v]', '', content)

    # 2. Remove any number of backslashes before letters n, r, t, f, v
    content = re.sub(r'(\\+)[nrtfv]', '', content)

    # 3. Collapse multiple spaces to one
    content = re.sub(r' {2,}', ' ', content)

    # 4. Trim leading/trailing spaces
    return content.strip()


content = """
'package com.suraj.blog.dao;\\n\\nimport org.springframework.data.jpa.repository.JpaRepository;\\n\\nimport com.suraj.blog.entity.Category;\\n\\npublic interface Ca
tegoryRepo extends JpaRepository<Category, Integer> {\\n\t\\n}\\n'
"""

print(cleanContent(content))
