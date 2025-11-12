#!/usr/bin/env python3
"""
Fix TensorFlow model compatibility issue by re-saving the model
with the current TensorFlow version.
This script handles the batch_shape compatibility issue.
"""

import os
import sys
import tensorflow as tf
import numpy as np

def fix_mlp_model():
    """Fix MLP model compatibility by re-saving it."""
    print("🔧 Fixing MLP model compatibility...")
    print("=" * 60)
    
    model_path = "saved_models/mlp_emotion_model.h5"
    backup_path = "saved_models/mlp_emotion_model.h5.backup"
    new_model_path = "saved_models/mlp_emotion_model_fixed.h5"
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    try:
        # Step 1: Backup original model
        print(f"📦 Backing up original model to {backup_path}...")
        import shutil
        shutil.copy2(model_path, backup_path)
        print("✅ Backup created")
        
        # Step 2: Load and fix the model
        print(f"\n📥 Loading model from {model_path}...")
        
        model = None
        
        # Method 1: Try loading with safe_mode=False (TensorFlow 2.13+)
        try:
            print("   Attempting Method 1: Load with safe_mode=False...")
            model = tf.keras.models.load_model(
                model_path,
                compile=False,
                safe_mode=False
            )
            print("   ✅ Method 1 succeeded!")
        except Exception as e1:
            print(f"   ❌ Method 1 failed: {str(e1)[:100]}...")
            
            # Method 2: Fix the HDF5 file directly by modifying the config
            try:
                print("   Attempting Method 2: Fix HDF5 config directly...")
                import h5py
                import json
                import shutil
                
                # First, copy the entire file
                temp_path = model_path + ".temp"
                shutil.copy2(model_path, temp_path)
                
                # Now modify the config in the copied file
                with h5py.File(temp_path, 'r+') as f:
                    # Get model config
                    if 'model_config' in f.attrs:
                        config_str = f.attrs['model_config']
                        if isinstance(config_str, bytes):
                            config_str = config_str.decode('utf-8')
                        
                        config = json.loads(config_str)
                        
                        # Fix the config by replacing batch_shape with input_shape and fixing DTypePolicy
                        fixes_applied = {'batch_shape': 0, 'dtype_policy': 0}
                        
                        def fix_config(obj, path=""):
                            if isinstance(obj, dict):
                                # Fix ANY batch_shape - convert to input_shape (works for InputLayer)
                                if 'batch_shape' in obj:
                                    batch_shape = obj.pop('batch_shape', None)
                                    if batch_shape and len(batch_shape) > 1:
                                        obj['input_shape'] = batch_shape[1:]
                                        fixes_applied['batch_shape'] += 1
                                        print(f"      Fixed batch_shape at {path}: {batch_shape} -> {obj['input_shape']}")
                                
                                # Also check nested config dicts
                                if 'config' in obj and isinstance(obj['config'], dict):
                                    if 'batch_shape' in obj['config']:
                                        batch_shape = obj['config'].pop('batch_shape', None)
                                        if batch_shape and len(batch_shape) > 1:
                                            obj['config']['input_shape'] = batch_shape[1:]
                                            fixes_applied['batch_shape'] += 1
                                            print(f"      Fixed batch_shape in nested config at {path}")
                                
                                # Fix DTypePolicy - convert to string (check both direct and nested)
                                if 'dtype' in obj:
                                    if isinstance(obj['dtype'], dict):
                                        if obj['dtype'].get('class_name') == 'DTypePolicy':
                                            dtype_name = obj['dtype'].get('config', {}).get('name', 'float32')
                                            obj['dtype'] = dtype_name
                                            fixes_applied['dtype_policy'] += 1
                                            if fixes_applied['dtype_policy'] <= 5:  # Only print first few
                                                print(f"      Fixed DTypePolicy at {path}: -> {dtype_name}")
                                
                                # Also check for DTypePolicy in nested config dicts
                                if 'config' in obj and isinstance(obj['config'], dict):
                                    if 'dtype' in obj['config'] and isinstance(obj['config']['dtype'], dict):
                                        if obj['config']['dtype'].get('class_name') == 'DTypePolicy':
                                            dtype_name = obj['config']['dtype'].get('config', {}).get('name', 'float32')
                                            obj['config']['dtype'] = dtype_name
                                            fixes_applied['dtype_policy'] += 1
                                            if fixes_applied['dtype_policy'] <= 5:
                                                print(f"      Fixed DTypePolicy in nested config at {path}: -> {dtype_name}")
                                
                                # Recursively fix nested configs
                                for key, value in obj.items():
                                    fix_config(value, f"{path}.{key}" if path else key)
                            elif isinstance(obj, list):
                                for i, item in enumerate(obj):
                                    fix_config(item, f"{path}[{i}]" if path else f"[{i}]")
                        
                        fix_config(config)
                        print(f"   Applied {fixes_applied['batch_shape']} batch_shape fixes and {fixes_applied['dtype_policy']} DTypePolicy fixes")
                        
                        # Write fixed config back
                        fixed_config_str = json.dumps(config)
                        del f.attrs['model_config']
                        f.attrs['model_config'] = fixed_config_str.encode('utf-8')
                
                # Try loading the fixed model
                model = tf.keras.models.load_model(
                    temp_path,
                    compile=False
                )
                
                # Move fixed file to final location
                if os.path.exists(new_model_path):
                    os.remove(new_model_path)
                os.replace(temp_path, new_model_path)
                print("   ✅ Method 2 succeeded!")
                        
            except Exception as e2:
                print(f"   ❌ Method 2 failed: {str(e2)[:100]}...")
                
                # Method 3: Use custom object scope with both fixes
                try:
                    print("   Attempting Method 3: Custom object handlers...")
                    from tensorflow.keras.layers import InputLayer, Dense
                    from tensorflow.keras.utils import CustomObjectScope
                    from tensorflow.keras import mixed_precision
                    
                    class CompatibleInputLayer(InputLayer):
                        def __init__(self, **kwargs):
                            if 'batch_shape' in kwargs:
                                batch_shape = kwargs.pop('batch_shape')
                                if batch_shape and len(batch_shape) > 1:
                                    kwargs['input_shape'] = batch_shape[1:]
                            super().__init__(**kwargs)
                    
                    # Handle DTypePolicy by using a string dtype
                    def get_dtype_policy(dtype_config):
                        """Convert DTypePolicy config to string dtype."""
                        if isinstance(dtype_config, dict) and dtype_config.get('class_name') == 'DTypePolicy':
                            return dtype_config.get('config', {}).get('name', 'float32')
                        return dtype_config
                    
                    custom_objects = {
                        'InputLayer': CompatibleInputLayer,
                    }
                    
                    with CustomObjectScope(custom_objects):
                        model = tf.keras.models.load_model(
                            model_path,
                            compile=False
                        )
                    print("   ✅ Method 3 succeeded!")
                    
                except Exception as e3:
                    print(f"   ❌ Method 3 failed: {str(e3)[:100]}...")
                    raise Exception(f"All loading methods failed. Errors: {e1}, {e2}, {e3}")
        
        if model is None:
            raise Exception("Failed to load model with any method")
        
        # Step 3: Re-save the model in a compatible format (if not already saved by Method 2)
        if not os.path.exists(new_model_path):
            print(f"\n💾 Re-saving model to {new_model_path}...")
            # Save in H5 format with current TensorFlow
            model.save(new_model_path, save_format='h5')
            print("✅ Model re-saved successfully!")
        else:
            print(f"\n✅ Model already saved to {new_model_path} by Method 2")
        
        # Step 4: Verify the new model can be loaded
        print(f"\n🔍 Verifying new model can be loaded...")
        test_model = tf.keras.models.load_model(new_model_path, compile=False)
        print("✅ New model loads successfully!")
        
        # Step 5: Replace old model with fixed model
        print(f"\n🔄 Replacing old model with fixed version...")
        os.replace(model_path, backup_path)  # Move old to backup
        os.replace(new_model_path, model_path)  # Move fixed to original location
        print("✅ Model replaced successfully!")
        
        print("\n" + "=" * 60)
        print("🎉 Model compatibility fix completed successfully!")
        print(f"   Original model backed up to: {backup_path}")
        print(f"   Fixed model at: {model_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error fixing model: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting MLP Model Compatibility Fix")
    print("=" * 60)
    print(f"TensorFlow version: {tf.__version__}")
    print()
    
    success = fix_mlp_model()
    
    if success:
        print("\n✅ All done! You can now rebuild your Docker container.")
        sys.exit(0)
    else:
        print("\n❌ Fix failed. Please check the errors above.")
        sys.exit(1)

