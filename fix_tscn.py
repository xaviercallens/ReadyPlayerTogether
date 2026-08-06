import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis\scenes"

count = 0
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".tscn"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "[subresource " in content:
                new_content = content.replace("[subresource ", "[sub_resource ")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Fixed {file}")

print(f"Total files fixed: {count}")
