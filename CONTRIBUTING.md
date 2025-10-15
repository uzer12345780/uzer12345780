# Contributing to KoloCloud

Thank you for your interest in contributing to KoloCloud! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, browser)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/uzer12345780/uzer12345780.git
   cd uzer12345780
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Ensure the server starts without errors
   - Test all affected functionality
   - Check for console errors

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Wait for review

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### JavaScript
- Use modern ES6+ syntax
- Use meaningful variable names
- Add comments for complex logic
- Follow existing patterns

### HTML/CSS
- Use semantic HTML
- Follow Tailwind CSS conventions
- Keep templates clean and readable
- Add comments for complex layouts

## Project Structure

```
KoloCloud/
├── backend/          # Python Flask backend
├── frontend/         # HTML/CSS/JS frontend
├── data/            # Data storage (not committed)
├── config/          # Configuration files
└── docs/            # Documentation
```

## Development Setup

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Run development server:
   ```bash
   export DEBUG=True
   python backend/app.py
   ```

## Testing

Currently, the project doesn't have automated tests. Contributions to add tests are highly welcome!

Manual testing checklist:
- [ ] Login/logout functionality
- [ ] File upload/download/delete
- [ ] OCR processing
- [ ] AI assistant queries
- [ ] Real-time chat
- [ ] Admin panel access

## Documentation

When adding new features:
- Update README.md if needed
- Update QUICKSTART.md for user-facing features
- Add inline code comments
- Update API documentation

## Security

- Never commit sensitive data (.env files, passwords, keys)
- Always validate user input
- Use parameterized queries for database
- Follow secure coding practices

## Questions?

If you have questions:
- Check existing documentation
- Search existing issues
- Create a new issue for discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to KoloCloud! 🇺🇦
