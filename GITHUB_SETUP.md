# GitHub Repository Setup Guide

This guide explains how to organize and upload this project to GitHub.

## 📋 Pre-Upload Checklist

### ✅ Files to Exclude

The `.gitignore` file has been configured to exclude:
- Large data files (`data/`, `*.wav`, `*.mp3`)
- Model files (`*.h5`, `*.pkl` in `saved_models/`)
- Cache files (`__pycache__/`, `feature_cache/`)
- Jupyter checkpoints (`.ipynb_checkpoints/`)
- Personal documents (specific PDFs)

### ✅ Files to Include

- All Python source code (`.py` files)
- Jupyter notebooks (`.ipynb` files)
- Documentation (`.md` files)
- Configuration files (`requirements.txt`, `Dockerfile`, etc.)
- Metadata CSV files
- Research papers in `articulos/` (if not too large)

## 🚀 Step-by-Step Upload Process

### 1. Initialize Git Repository (if not already done)

```bash
cd /home/ariel/Documents/Projects/EmotionRecognitionSpeech
git init
```

### 2. Review and Update .gitignore

The `.gitignore` file is already configured, but review it to ensure it matches your needs:

```bash
cat .gitignore
```

### 3. Stage Files for Initial Commit

```bash
# Check what will be added
git status

# Add all files (respecting .gitignore)
git add .

# Review what's staged
git status
```

### 4. Create Initial Commit

```bash
git commit -m "Initial commit: Emotion Recognition from Speech project

- Complete ML pipeline with MLP, SVM, and KNN models
- Feature extraction: MFCC, RASTA-MFCC, MSES
- Production-ready FastAPI deployment
- Comprehensive documentation and notebooks"
```

### 5. Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it: `EmotionRecognitionSpeech` (or your preferred name)
4. **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 6. Connect Local Repository to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/EmotionRecognitionSpeech.git

# Verify remote
git remote -v
```

### 7. Push to GitHub

```bash
# Push to main/master branch
git branch -M main  # Rename branch to 'main' if needed
git push -u origin main
```

## 📦 Handling Large Files

### Option 1: Git LFS (Recommended for Models)

If you want to include model files, use Git LFS:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pkl"
git lfs track "saved_models/**"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking for model files"
```

### Option 2: Exclude Large Files (Current Setup)

The current `.gitignore` excludes large files. Users can:
- Download datasets separately
- Train models using provided notebooks
- Use pre-trained models from releases

### Option 3: GitHub Releases

Upload large files (models, sample data) as GitHub Releases:
1. Go to repository → Releases → Create a new release
2. Upload model files as release assets
3. Document in README how to download

## 🏷️ Repository Settings

### Recommended Settings

1. **Description**: "Emotion recognition from speech using MFCC and multi-band spectral entropy signatures with MLP, SVM, and KNN"

2. **Topics/Tags**: Add relevant tags:
   - `emotion-recognition`
   - `speech-processing`
   - `machine-learning`
   - `mfcc`
   - `python`
   - `tensorflow`
   - `fastapi`

3. **Visibility**: Choose public or private based on your preference

4. **Default Branch**: Set to `main` or `master`

## 📝 Repository Structure on GitHub

After uploading, your repository should have:

```
EmotionRecognitionSpeech/
├── .gitignore
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── PROJECT_STRUCTURE.md         # Structure documentation
├── GITHUB_SETUP.md             # This file
├── requirements.txt
├── setup_environment.sh
├── caracteristicas/            # Feature extraction notebooks
├── clacificadores/             # Model training notebooks
├── experimentos/               # Experimental notebooks
├── visualizacion/              # Visualization notebooks
├── emotion_recognition_cloud/  # API deployment
├── helpers/                    # Utility functions
├── metadatos/                  # Dataset metadata
├── articulos/                  # Research papers
├── documento/                  # Thesis documents
└── [main pipeline notebooks]
```

## 🔄 Ongoing Maintenance

### Regular Updates

```bash
# Make changes
# ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature extraction method"

# Push to GitHub
git push origin main
```

### Branch Strategy

For larger features, use branches:

```bash
# Create feature branch
git checkout -b feature/new-model

# Make changes and commit
git add .
git commit -m "feat: Add Random Forest classifier"

# Push branch
git push origin feature/new-model

# Create Pull Request on GitHub
```

## 📊 Repository Statistics

GitHub will automatically show:
- Code statistics
- Language distribution
- Commit history
- Contributors (if public)

## 🔒 Security Considerations

### Before Making Public

1. **Check for sensitive information**:
   ```bash
   # Search for API keys, passwords, etc.
   grep -r "api_key\|password\|secret" .
   ```

2. **Review .gitignore**: Ensure sensitive files are excluded

3. **Remove large personal files**: Check `documento/` and `articulos/`

### Environment Variables

If your code uses environment variables:
- Create `.env.example` with template values
- Document required variables in README
- Never commit actual `.env` files

## 📚 Documentation on GitHub

GitHub will automatically render:
- `README.md` - Main page
- `CONTRIBUTING.md` - Linked from issues/PRs
- Code documentation in notebooks
- Markdown files in any directory

## 🎯 Best Practices

1. **Regular Commits**: Commit frequently with clear messages
2. **Descriptive Messages**: Use conventional commit format
3. **Update Documentation**: Keep README and docs current
4. **Tag Releases**: Tag major versions (v1.0.0, v2.0.0)
5. **Issues Tracking**: Use GitHub Issues for bugs and features
6. **Pull Requests**: Use PRs for code review (even for solo projects)

## 🚨 Common Issues

### Issue: Repository too large

**Solution**: 
- Use `.gitignore` to exclude large files
- Use Git LFS for necessary large files
- Upload large files to releases

### Issue: Push rejected

**Solution**:
```bash
# Pull latest changes first
git pull origin main --rebase

# Resolve conflicts if any
# Then push again
git push origin main
```

### Issue: Files still tracked after .gitignore

**Solution**:
```bash
# Remove from cache but keep locally
git rm --cached filename

# Or remove entire directory
git rm -r --cached directory/
```

## ✅ Final Checklist

Before making repository public:

- [ ] `.gitignore` properly configured
- [ ] No sensitive information in code
- [ ] README.md is complete and accurate
- [ ] All documentation files present
- [ ] Requirements.txt is up to date
- [ ] Code is properly commented
- [ ] Repository description and topics set
- [ ] License file added (if applicable)

## 📞 Need Help?

- [GitHub Docs](https://docs.github.com)
- [Git Handbook](https://git-scm.com/book)
- [Git LFS Tutorial](https://git-lfs.github.com)

---

**Ready to upload?** Follow the steps above and your project will be well-organized on GitHub! 🚀

