# Contributing to Emotion Recognition from Speech

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/EmotionRecognitionSpeech.git
   cd EmotionRecognitionSpeech
   ```

2. **Create a branch for your work**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up your development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 🔄 Development Workflow

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions or updates

### Workflow Steps

1. **Create a new branch** from `master`
2. **Make your changes** following coding standards
3. **Test your changes** thoroughly
4. **Commit your changes** with clear messages
5. **Push to your fork** and create a pull request

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example Code Style

```python
def extract_mfcc_features(
    audio_path: str,
    n_mfcc: int = 13,
    hop_length: int = 512
) -> np.ndarray:
    """
    Extract MFCC features from audio file.
    
    Args:
        audio_path: Path to the audio file
        n_mfcc: Number of MFCC coefficients to extract
        hop_length: Number of samples between successive frames
        
    Returns:
        Array of MFCC features
    """
    # Implementation here
    pass
```

### Notebook Guidelines

- Keep notebooks organized and well-documented
- Use markdown cells to explain the workflow
- Clear variable names and comments
- Remove unnecessary output cells before committing
- Keep notebooks focused on specific tasks

### File Organization

- Place new features in appropriate directories
- Follow existing directory structure
- Keep related files together
- Use descriptive file names

## 💬 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat: Add RASTA-MFCC feature extraction

Implement RASTA filtering for improved noise robustness
in MFCC feature extraction pipeline.

Closes #123
```

```
fix: Resolve model loading compatibility issue

Fix TensorFlow version compatibility when loading saved
MLP models. Update model architecture to use current
TensorFlow API.

Fixes #456
```

## 🔍 Pull Request Process

### Before Submitting

1. **Ensure your code works**
   - Test all functionality
   - Run existing tests
   - Check for linting errors

2. **Update documentation**
   - Update README if needed
   - Add docstrings to new functions
   - Update relevant notebooks

3. **Clean up your code**
   - Remove debug prints
   - Remove commented-out code
   - Format code consistently

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass
```

### Review Process

1. PR will be reviewed by maintainers
2. Address any feedback or requested changes
3. Once approved, PR will be merged

## 🐛 Reporting Issues

### Before Reporting

- Check if the issue already exists
- Verify it's not a configuration problem
- Gather relevant information

### Issue Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. ...
2. ...

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9]
- TensorFlow version: [e.g., 2.8.0]

**Additional context**
Any other relevant information.
```

## 📚 Additional Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [NumPy Docstring Convention](https://numpydoc.readthedocs.io/)
- [Git Best Practices](https://git-scm.com/book)

## ❓ Questions?

If you have questions about contributing, please:
- Open an issue with the `question` label
- Check existing documentation
- Review similar contributions

Thank you for contributing! 🎉

