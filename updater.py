#! /usr/bin/env python3

import requests
import argparse
import json
import hashlib
import glob
import os
from tqdm import tqdm

HEADER = {'user-agent': 'Giacomino99/minecraft-server-mod-updater (Discord: Giacomino_)'}
API_URL = 'https://api.modrinth.com/v2/'

def get_args():
    """Get command line arguments."""
    parser = argparse.ArgumentParser(allow_abbrev = False,
                                     description = '''Minecraft Server Mod Updater.
                                                      Checks for and downloads updated mods.
                                                      All old mod files are renamed.''')
    parser.add_argument('-f', '--folder', metavar= 'F', required=True,
                        help='The directory of the mods folder.')
    parser.add_argument('-v', '--version', metavar='V', required=True,
                        help='The version of Minecraft to update mods to')
    parser.add_argument('-l', '--loader', metavar='L', required=True, type=str.lower,
                        help='The mod loader you are using (Fabric, Forge, etc...)')
    parser.add_argument('-y', action='store_true',
                        help='Automatically accept update')
    return parser.parse_args()

def main(loader, version, folder, auto_yes):
    """Check for updates and download files."""
    # Hash Jar Files
    jar_names = glob.glob(glob.escape(folder) + '*.jar')
    if not jar_names:
        print('No .jar files found in directory.')
        exit(1)
    jar_hashes = [hash_file(x) for x in jar_names]
    file_hashes = dict(zip(jar_hashes, jar_names))

    # Make request to Modrinth Servers
    data = make_post_data(jar_hashes, loader, version)
    search_data = requests.post(API_URL+'version_files/update', json=data, headers = HEADER)
    if not search_data.status_code == requests.codes.ok:
        print(f'Error: Could not fetch updates: ({search_data.status_code})')
        exit(1)
    search_data = search_data.json()
    
    # Display Updates
    update_list = []
    for update in search_data:
        # Ignore files that are the same version as current
        if update == search_data[update]['files'][0]['hashes']['sha1']:
            continue
        update_list.append(update)

    no_version_available = []
    for file in file_hashes:
        if not file in search_data:
            no_version_available.append(file)

    if no_version_available:
        print(f'No Versions Available for "{loader.title()}" and Minecraft Version "{version}":')
        [print(f"\t{file_hashes[file].split('/')[-1]}") for file in no_version_available]
        print()
    
    if update_list:
        print(f'{len(update_list)} Update{"s" if len(update_list) > 1 else ""} Available:')
        [print(f"\t{file_hashes[u].split('/')[-1]} -> {search_data[u]['files'][0]['filename']}") for u in update_list]
        print()
    else:
        print('No Updates Available.')
        exit(0)


    # Ask for conformation
    
    answer = 'Y' if auto_yes else input('Update All? [y/n]\n').upper()
    if answer != 'Y':
        exit(0)

    # Update Files
    for update in update_list:
        os.rename(file_hashes[update], file_hashes[update]+'.outdated')
        file_info = search_data[update]['files'][0]
        download_file(file_info['url'], file_info['filename'], folder)

    print('Update completed successfully!')
    exit(0)

def hash_file(file_name):
    """Return the SHA1 hash of the specified file."""
    with open(file_name, 'rb') as f:
        sha1 = hashlib.sha1(f.read()).hexdigest()
    return sha1

def make_post_data(hashes, loader, version):
    """Create a dictionary for the Modrinth POST request."""
    data = {
        'hashes': hashes,
        'algorithm': 'sha1',
        'loaders': [loader],
        'game_versions': [version]
    }
    return data

def download_file(url, file_name, folder):
    """Download the file at 'url' and save to 'file_name'"""
    download = requests.get(url, stream = True, headers=HEADER)
    total_size = int(download.headers.get('Content-Length'))
    block_size = 1024

    with open(folder+file_name, 'wb') as jar, tqdm(desc=file_name, total=total_size, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in download.iter_content(chunk_size=block_size):
            size=jar.write(data)
            bar.update(size)

if __name__ == '__main__':
    args = get_args()
    print(args)
    main(args.loader, args.version, args.folder, args.y)

