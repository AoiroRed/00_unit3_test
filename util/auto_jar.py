import os
import zipfile
import shutil


def unzip(zip_file, dest_dir):
    """Unzip a file to a destination directory and delete the zip file.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(dest_dir)


def compile_java(class_path, java_files, lib_path):
    """Compile java files in src_path and output to class_path.
    """
    cmd = 'javac -encoding UTF-8 -d ' + class_path
    if lib_path:
        cmd += ' -cp '
        for jar in os.listdir(lib_path):
            if jar.endswith('.jar'):
                cmd += os.path.join(lib_path, jar) + ';'
    for java_file in java_files:
        cmd += ' ' + java_file
    print(cmd)
    os.system(cmd)


def create_MANIFEST(class_path, main_class, lib_path):
    """Create a MANIFEST file.
    """
    manifest = os.path.join(class_path, 'MY_MANIFEST.MF')
    with open(manifest, 'w') as f:
        f.write('Manifest-Version: 1.0\n')
        if lib_path:
            f.write('Class-Path:')
            for jar in os.listdir(lib_path):
                if jar.endswith('.jar'):
                    f.write(' lib/' + jar)
            f.write('\n')
        f.write('Created-By: Red\n')
        f.write('Main-Class: %s\n' % main_class)
        f.write('\n')
    return manifest


def make_jar(src_path, jar_file, manifest='MY_MANIFEST.MF'):
    """Create a jar file from a class path.
    """
    cmd = 'jar cvfm %s %s -C %s .' % (jar_file, manifest, src_path)
    os.system(cmd)


def auto_jar(zip_path, lib_path=None, delete_src=True):
    """Automatically compile, create jar files from zip files 
    and load libraries in lib_path.
    """
    if not os.path.exists('temp'):
        os.mkdir('temp')
    if not os.path.exists('jar'):
        os.mkdir('jar')

    for zip_file in os.listdir(zip_path):
        if not zip_file.endswith('.zip'):
            continue
        if delete_src:
            project_path = os.path.join('temp', zip_file[:-4])
        else:
            project_path = os.path.join('src', zip_file[:-4])
        class_path = os.path.join('temp', zip_file[:-4], 'classes')
        if not os.path.exists(class_path):
            os.makedirs(class_path)
        main_class = 'unknown'
        java_files = []

        unzip(os.path.join(zip_path, zip_file), project_path)
        for dirpath, dirnames, filenames in os.walk(project_path):
            for filename in filenames:
                if filename.endswith('.java'):
                    java_file = os.path.join(dirpath, filename)
                    with open(java_file, 'r', encoding='utf8') as f:
                        if 'public static void main' in f.read():
                            f.buffer.seek(0)
                            if 'package' in f.read():
                                f.buffer.seek(0)
                                main_class = f.read().split('package ')[1].split(';')[
                                    0] + '.' + filename[:-5]
                            else:
                                main_class = filename[:-5]
                    java_files.append(java_file)

        if main_class == 'unknown':
            print('No main class found in %s' % zip_file)
            continue

        compile_java(class_path, java_files, lib_path)
        manifest = create_MANIFEST(class_path, main_class, lib_path)
        make_jar(class_path, os.path.join(
            'jar', zip_file[:-4] + '.jar'), manifest)

    shutil.rmtree('temp')
    if lib_path:
        if not os.path.exists('jar/lib'):
            os.mkdir('jar/lib')
        for jar in os.listdir(lib_path):
            if jar.endswith('.jar'):
                shutil.copy(os.path.join(lib_path, jar), 'jar/lib')


if __name__ == '__main__':
    zip_path = input('Enter the path to the zip files: ')
    auto_jar(zip_path, lib_path=None)
