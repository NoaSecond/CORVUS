import os
import re

# Configurations des commentaires pour chaque type de fichier
copyright_comment = "Développé avec ❤️ par : www.noasecond.com"

comments = {
    '.py': "# {}".format(copyright_comment),
    '.cpp': "// {}".format(copyright_comment),
    '.h': "// {}".format(copyright_comment),
    '.ts': "// {}".format(copyright_comment),
}

extensions = tuple(comments.keys())
exclude_dirs = ['.git', '.github', '.vscode']
exclude_files = ['.gitattributes', '.gitignore']

def should_exclude(file_path):
    for excl_dir in exclude_dirs:
        if excl_dir in file_path:
            return True
    for excl_file in exclude_files:
        if file_path.endswith(excl_file):
            return True
    return False

def add_comment_to_file(file_path, comment):
    with open(file_path, 'r+') as file:
        content = file.read()
        # Remove old comment if present
        content = re.sub(r'(\n\n{}|\n\n{}|\n\n{}|\n\n{}|\n\n{})'.format(
            comments['.py'],
            comments['.cpp'],
            comments['.h'],
            comments['.ts'],
        ), '', content)

        # Remove trailing empty lines
        content = content.rstrip()
        
        if comment.strip() not in content:
            # Add a newline if the last line is not empty
            if not content.endswith(('\n', '\r')):
                content += "\n"
            file.seek(0)
            file.write(content + comment)
            file.truncate()

def main():
    for root, dirs, files in os.walk('.'):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(extensions) and not should_exclude(file_path):
                ext = os.path.splitext(file)[1]
                comment = comments[ext]
                add_comment_to_file(file_path, comment)

if __name__ == "__main__":
    main()