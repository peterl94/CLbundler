from __future__ import print_function
import os
import urllib
import logging
import shutil

import config
import system
import exceptions

def extract_source(filepath, dest_dir, dest_name):
    """
    Extract a source archive to dest_dir. 
    To keep names consistent, top level dir in archive will be renamed to dest_name 
    """
    tmp_dir = os.path.join(os.path.dirname(filepath), "tmp")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    
    #extract to a temporary directory so that we can get the dir name
    system.extract(filepath, tmp_dir)
    
    src_dir = os.listdir(tmp_dir)[0]
    src_dir = os.path.join(tmp_dir, src_dir)
    if not os.path.isdir(src_dir):
        raise exceptions.SourceArchiveError("Expected a directory, got " + src_dir)
        
    os.rename(src_dir, os.path.join(dest_dir, dest_name))
    
    shutil.rmtree(tmp_dir)

def _check_archive_url(url):
    try:
        response = urllib.urlopen(url)
    except IOError:
        raise exceptions.InvalidUrlError("Invalid URL: " + url)
        
    if not response.info().gettype().startswith("application"):
        raise exceptions.InvalidUrlError(url + " does not seem to point to a archive file")
         
def _download_progress(blocks, block_size, file_size):
    percent = min(blocks*block_size*100.0 / file_size, 100)
    print("{0:3.1f}%".format(percent), end='\r')

def download_source(source_info):
    if source_info["type"] == "archive":
        src_cache_dir = config.global_config().src_dir()
        filename = os.path.basename(source_info["url"])
        filepath = os.path.join(src_cache_dir, filename)
        
        _check_archive_url(source_info["url"])
        
        if not os.path.exists(filepath):
            logging.getLogger().info("Downloading {}...".format(filename))
            urllib.urlretrieve(source_info["url"], filepath, _download_progress)
            
        return filepath
    
def get_source(dest_dir, name, version, source_info):
    """
    Get source code directory named name-version,
    downloaded according to source_info
    
    souce_info is expected to be a dictionary with at least two entries:
    'type': one of ['archive']
    'url': str
    """
    src_path = download_source(source_info)
    dest_src_name = "{0}-{1}".format(name, version)
    dest_src_dir = os.path.join(dest_dir, dest_src_name)
        
    if source_info["type"] == "archive":
        if not os.path.exists(dest_src_dir):
            logging.getLogger().info("Extracting {}...".format(os.path.basename(src_path)))
            extract_source(src_path, dest_dir, dest_src_name)
        
        return dest_src_dir

def patch_source(names, paths, src_dir):
    """Apply patches in src_dir
    
    Arguments:
    names -- list of patch names without extension
    paths -- list of directories to search for patch files
    src_dir -- directory to apply patches in
    """
    patches = []
    for n in names:
        patch = ""
        for p in paths:
            if os.path.exists(os.path.join(p, n + ".diff")):
                patch = os.path.join(p, n + ".diff")
                break          
        if not patch:
            raise exceptions.FileNotFoundError("Could not find patch: " + p + ".diff")
            
        patches.append(patch)
        
    system.patch(patches, src_dir)
    