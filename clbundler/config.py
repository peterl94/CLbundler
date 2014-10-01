import os
import platform
from ConfigParser import SafeConfigParser

_config = None
_is_loaded = False

def global_config():
    global _config, _is_loaded
    
    if not _config:
        _config = Config()
    if not _is_loaded:
        _config.load()
        _is_loaded = True
    return _config  
    
class Config(SafeConfigParser):
    _default_data_dir = os.path.join(os.path.expanduser('~'), "CLbundler")
    _default_config_path = os.path.join(_default_data_dir, "CLbundler.cfg")
        
    def load(self, path=_default_config_path):
        if os.path.isfile(path):
            with open(path, "r") as config_file:
                self.readfp(config_file)
        
        #options that need to always be available    
        self.defaults()["root"] = Config._default_data_dir
        self.defaults()["workspace"] = "%(root)s" + os.path.sep + "workspace"
        self.defaults()["src_cache"] = "%(root)s" + os.path.sep + "src_cache"
        self.defaults()["formula_dirs"] = "%(root)s" + os.path.sep + "formulas"
        
        if not self.has_section("Paths"):
            self.add_section("Paths")
        if not self.has_section("Bundle"):
            self.add_section("Bundle")
         
        #create the directories
        if not os.path.exists(self.get("Paths", "root")):
            os.mkdir(self.get("Paths", "root"))
        if not os.path.exists(self.get("Paths", "workspace")):
            os.mkdir(self.get("Paths", "workspace"))
        if not os.path.exists(self.get("Paths", "src_cache")):
            os.mkdir(self.get("Paths", "src_cache"))
            
    def write(self, path=_default_config_path):
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        
        with open(path, "wb") as config_file:
            SafeConfigParser.write(self, config_file)
    
    def root_dir(self):
        return self.get("Paths", "root")    
        
    def workspace_dir(self):
        return self.get("Paths", "workspace")
        
    def src_cache_dir(self):
        return self.get("Paths", "src_cache")
        
    def build_dir(self):
        return self.get("Paths", "build")
    
    def formula_dirs(self):
        paths_str = self.get("DEFAULT", "formula_dirs") + os.pathsep
        paths_str += self.get("Paths", "formula_dirs")
        paths = filter(bool, paths_str.split(os.pathsep))
        #add platform specific directories
        platform_paths = []
        for p in paths:
            platform_paths.append(os.path.join(p, os_name()))
            
        return paths + platform_paths
        
    def current_bundle(self):
        if self.has_option("Bundle", "path"):
            return self.get("Bundle", "path")
        return None        
        
def os_name():
    p = platform.platform()
    if p.startswith("Windows"):
         return "win"
    elif p.startswith("Darwin"):
         return "mac"
    elif p.startswith("Linux"):
         return "linux"
         
def exe_arch():
    a = platform.architecture()
    if a.startswith("32"):
        return "x86"
    elif a.startswith("64"):
        return "x64 "
        