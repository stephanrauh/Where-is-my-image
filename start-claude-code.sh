docker build -t claude-dev .

docker run -it \
  -v $(pwd):/workspace \
  -p 4201:4200 \
  claude-dev

# Example commands (exact syntax depends on installation)
# claude-code --help
# claude-code analyze-project
# claude-code fix-bugs