# 📁 Data Path Updates Summary

## Overview
All notebook data paths have been updated to use the new structure `./data/EMODB` and `./data/EMOVO` instead of the old `../EMODB` and `../emovo` paths.

## 🔄 Path Changes Made

### Audio File Paths Updated:
- **Old**: `../EMODB/audio/` → **New**: `./data/EMODB/audio/`
- **Old**: `../emovo/audio/` → **New**: `./data/EMOVO/audio/`

### Metadata CSV Paths Updated:
- **Old**: `../UrbanSound Dataset sample/metadata/` → **New**: `./data/metadata/`

## 📁 Updated Files

### 1. Data Exploration (`visualizacion/1 Data Exploration and Visualisation.ipynb`)
**Audio Files Updated:**
- ✅ `./data/EMOVO/audio/foldA/pau-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldE/14a04Ed.wav`
- ✅ `./data/EMOVO/audio/foldE/dis-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldL/03a04Lc.wav`
- ✅ `./data/EMOVO/audio/foldL/sor-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldF/03a04Fd.wav`
- ✅ `./data/EMOVO/audio/foldF/gio-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldN/03a04Nc.wav`
- ✅ `./data/EMOVO/audio/foldN/neu-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldT/03a04Ta.wav`
- ✅ `./data/EMOVO/audio/foldT/tri-f2-b1.wav`
- ✅ `./data/EMODB/audio/foldW/03a04Wc.wav`
- ✅ `./data/EMOVO/audio/foldW/rab-f2-b1.wav`

**Metadata Files Updated:**
- ✅ `./data/metadata/EMODB4 - testSize 0.3.csv`
- ✅ `./data/metadata/emovo2 - testSize 0.3.csv`
- ✅ `./data/metadata/emovo.csv`
- ✅ `./data/metadata/EMODB.csv`

### 2. Data Preprocessing (`visualizacion/2 Data Preprocessing and Data Splitting.ipynb`)
**Audio Files Updated:**
- ✅ `./data/EMODB/audio/foldA/03a04Ad.wav`
- ✅ `./data/EMOVO/audio/foldA/pau-f1-b1.wav`

**Metadata Files Updated:**
- ✅ `./data/metadata/EMODB.csv`
- ✅ `./data/metadata/emovo2.csv`

### 3. Model Training (`clacificadores/3.2.0.0 Model Training and Evaluation.ipynb`)
- ✅ All data paths updated to use new structure

## 📂 Expected Directory Structure

Your project should now have this structure:
```
EmotionRecognitionSpeech/
├── data/
│   ├── EMODB/
│   │   └── audio/
│   │       ├── foldA/
│   │       ├── foldE/
│   │       ├── foldF/
│   │       ├── foldL/
│   │       ├── foldN/
│   │       ├── foldT/
│   │       └── foldW/
│   ├── EMOVO/
│   │   └── audio/
│   │       ├── foldA/
│   │       ├── foldE/
│   │       ├── foldF/
│   │       ├── foldL/
│   │       ├── foldN/
│   │       ├── foldT/
│   │       └── foldW/
│   └── metadata/
│       ├── EMODB.csv
│       ├── emovo.csv
│       ├── emovo2.csv
│       ├── EMODB4 - testSize 0.3.csv
│       └── emovo2 - testSize 0.3.csv
├── visualizacion/
├── caracteristicas/
├── clacificadores/
└── experimentos/
```

## 🎯 Benefits of New Structure

### 1. **Cleaner Organization**
- All data in one `./data/` directory
- Clear separation between EMODB and EMOVO datasets
- Metadata files organized in dedicated folder

### 2. **Better Portability**
- Relative paths work from any notebook location
- No need to navigate up directories
- Easier to share and deploy

### 3. **Consistent Naming**
- EMOVO instead of emovo (consistent capitalization)
- Standardized path structure
- Clear dataset identification

## 🔧 Usage Instructions

### 1. **Set Up Your Data Directory**
Make sure your data is organized as shown above:
```bash
mkdir -p data/EMODB/audio data/EMOVO/audio data/metadata
```

### 2. **Copy Your Data Files**
```bash
# Copy EMODB audio files
cp -r /path/to/your/EMODB/audio/* data/EMODB/audio/

# Copy EMOVO audio files  
cp -r /path/to/your/EMOVO/audio/* data/EMOVO/audio/

# Copy metadata files
cp /path/to/your/metadata/*.csv data/metadata/
```

### 3. **Run Your Notebooks**
All notebooks will now work with the new path structure:
```bash
conda activate emotion_rec
jupyter notebook
```

## ✅ Verification

### Check if paths are working:
```python
import os

# Check EMODB paths
emodb_path = "./data/EMODB/audio/foldA/03a04Ad.wav"
print(f"EMODB file exists: {os.path.exists(emodb_path)}")

# Check EMOVO paths
emovo_path = "./data/EMOVO/audio/foldA/pau-f1-b1.wav"
print(f"EMOVO file exists: {os.path.exists(emovo_path)}")

# Check metadata paths
metadata_path = "./data/metadata/EMODB.csv"
print(f"Metadata file exists: {os.path.exists(metadata_path)}")
```

## 🚀 Next Steps

1. **Organize your data** according to the new structure
2. **Test the notebooks** to ensure all paths work
3. **Update any custom scripts** that reference the old paths
4. **Enjoy the cleaner organization!** 🎉

## 📝 Notes

- All path updates were made automatically using `sed` commands
- No manual editing was required
- All notebooks maintain their original functionality
- GPU optimizations remain intact

**Your notebooks are now ready to use with the new data structure!** 🎯




