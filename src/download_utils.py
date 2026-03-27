
import requests, zipfile, io, os
from pathlib import Path
import pandas as pd
import shutil

def download_file(url, out_path, timeout=180):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        print(f"Downloading dataset from: {url}")
        r = requests.get(url, stream=True, timeout=timeout)
        if r.status_code != 200:
            print('Download failed. Status code:', r.status_code)
            return False
        with open(out_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
        print('Saved to', out_path)
        return True
    except Exception as e:
        print('Download error:', e)
        return False

def unzip_all_in_folder(folder):
    folder = Path(folder)
    zips = list(folder.glob('*.zip'))
    for z in zips:
        try:
            print('Extracting', z)
            with zipfile.ZipFile(z, 'r') as zip_ref:
                extract_to = folder / z.stem
                extract_to.mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(extract_to)
                print('Extracted to', extract_to)
        except Exception as e:
            print('Failed to extract', z, e)

def find_files(folder, exts=['.csv','.mat','.txt']):
    files = []
    for ext in exts:
        files.extend([p for p in Path(folder).rglob(f'*{ext}')])
    return files

def try_read_file(filepath):
    path = Path(filepath)
    suf = path.suffix.lower()
    if suf == '.csv' or suf == '.txt':
        try:
            return pd.read_csv(path), 'csv'
        except Exception as e:
            print('CSV read error', e)
            return None, None
    if suf == '.mat':
        try:
            from scipy.io import loadmat
            mat = loadmat(path)
            # heuristics: find arrays with shape (n,) or (n,1) or (n,m)
            return mat, 'mat'
        except Exception as e:
            print('MAT read error', e)
            return None, None
    return None, None
