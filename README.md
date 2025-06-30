# AI-Setup-Cursor

A comprehensive setup project demonstrating best practices for AI-assisted development with Cursor IDE.

## 🎯 Project Purpose

This project serves as a template and learning resource for setting up an optimal development environment with Cursor AI assistant. It includes:

- **`.cursorrules`** - Comprehensive guidelines for AI assistant behavior
- **Project Templates** - Framework-agnostic project structure templates
- **Git workflow** - Best practices for version control
- **Documentation** - Complete setup and usage guides
- **PRD Templates** - Professional product requirement documentation

## 🚀 Quick Start

### Prerequisites
- Git
- GitHub CLI (gh)
- Cursor IDE
- Language-specific tools based on your project needs

## 📋 Using This as a Template

### Method 1: Fork and Customize (Recommended)
1. **Fork this repository**
   - Click the "Fork" button on GitHub
   - Choose your account as the destination
   - Optionally rename the repository

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

3. **Customize for your project**
   - Update `README.md` with your project details
   - Modify `.cursorrules` if needed for your specific workflow
   - Remove/add files in `docs/` as appropriate
   - Update `requirements.txt` or add your dependency files

### Method 2: Manual Clone and Setup
1. **Clone this repository**
   ```bash
   git clone https://github.com/akyrat/ai-setup-cursor.git
   cd ai-setup-cursor
   ```

2. **Remove existing git history and reinitialize**
   ```bash
   rm -rf .git
   git init
   git add .
   git commit -m "Initial commit from AI-Setup-Cursor template"
   ```

3. **Connect to your new remote repository**
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git
   git branch -M main
   git push -u origin main
   ```

### Post-Setup Steps

1. **Open in Cursor**
   ```bash
   cursor .
   ```

2. **Test the AI assistant**
   - The `.cursorrules` file will automatically configure Cursor's behavior
   - Try asking the AI to help with your project setup
   - Chat history will be automatically saved in `chat-history/` when you indicate you're ending the session

3. **Customize the template**
   - Replace this README content with your project-specific information
   - Update the PRD templates in `docs/` for your project requirements
   - Modify `.cursorrules` if you have specific AI assistant preferences

## 📁 Project Structure

```
AI-Setup-Cursor/
├── .cursorrules          # AI assistant behavior guidelines
├── README.md             # This file
├── .gitignore           # Git ignore patterns
├── chat-history/        # AI conversation exports (auto-generated)
├── .vscode/             # VSCode workspace configuration
│   ├── extensions.json # Recommended extensions
│   └── settings.json   # Workspace settings
├── .eslintrc.json       # ESLint configuration
├── .prettierrc          # Prettier formatting rules
├── pyproject.toml       # Python tools configuration
├── templates/           # Project-specific templates
│   ├── python/         # Python project template
│   ├── react/          # React project template
│   └── other/          # Additional templates
└── docs/               # Documentation
    ├── setup/          # Setup guides by framework
    └── PRD-template.md # Product Requirements Doc template
```

## 🛠️ Development

### Running the Application
```bash
python src/main.py
```

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black src/ tests/
```

## 📚 Key Features

### 1. AI Assistant Optimization
The `.cursorrules` file contains comprehensive guidelines for:
- Clear communication patterns
- Technical workflow best practices
- Error handling and recovery
- User experience optimization
- Framework-specific best practices
- **Automatic chat history export** - Conversations are automatically saved to `chat-history/` folder when sessions end

### 2. Code Quality & Linting
Pre-configured linting and formatting setup for multiple languages:
- **VSCode Extensions**: Automatic recommendations for essential development tools
- **ESLint**: JavaScript/TypeScript linting with React and Next.js support
- **Prettier**: Consistent code formatting across all file types
- **Python Tools**: Black, isort, pylint, flake8, and mypy configurations
- **Auto-formatting**: Format on save and paste enabled by default
- **Git Integration**: GitLens and Git Graph for enhanced version control

### 3. Product Requirements Documentation
The `docs/PRD-template.md` provides a professional template for documenting product requirements:
- Clear project overview and scope definition
- Structured feature planning with milestones
- Technical requirements and skill specifications
- Client and stakeholder information
- Example PRD for reference (`docs/PRD-example.md`)

This template helps maintain consistent and comprehensive project documentation, ensuring:
- Clear communication between stakeholders
- Well-defined project scope and requirements
- Organized feature development planning
- Professional project presentation

### 4. Development Environment
- Framework-specific setup guides
- Best practices for each supported stack
- Testing and quality assurance
- Code style and formatting guidelines

### 5. Git Workflow
- Proper repository initialization
- Meaningful commit messages
- Remote repository setup
- Branch management strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Cursor IDE team for the amazing AI-assisted development experience
- The open-source community for best practices and tools
- All contributors who help improve this template

---

**Happy coding with AI! 🚀**
