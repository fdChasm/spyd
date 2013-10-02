import os.path
import glob

def import_all(init_module_name, module_prefix, exclude):

    file_path = os.path.abspath(init_module_name)
    dir_dir = os.path.dirname(file_path)

    filenames = glob.glob(os.path.join(dir_dir, "*.py"))

    for filename in filenames:
        module_name, _py = os.path.splitext(os.path.basename(filename))
        
        # Don't try to load this file, __init__.py
        if module_name in exclude:
            continue
        
        module_import_path = '{}.{}'.format(module_prefix, module_name)
        
        __import__(module_import_path)
        
