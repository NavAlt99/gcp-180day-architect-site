with open('scratch/day021/make_part3.py') as f:
    text = f.read()

text = text.replace("${var.project_name}", "$${var.project_name}")

with open('scratch/day021/make_part3.py', 'w') as f:
    f.write(text)

print("Updated make_part3.py cleanly")
