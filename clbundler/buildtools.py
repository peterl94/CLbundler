import os

import system

def cmake_generator(toolchain, arch):
    """Return name of CMake generator for toolchain"""
    generator = ""
    if toolchain.startswith("vc"):
        if toolchain == "vc9":
            generator = "Visual Studio 9 2008"
        else:
            generator = "Visual Studio " + vc_version(toolchain)
        if arch == "x64":
            generator = generator + " Win64"
    else:
        generator = "Unix Makefiles"
        
    return generator

def cmake(context, options={}, build_dir=""):
    """Configure a CMake based project

    The current directory is assumed to be the top level source directory
    CMAKE_INSTALL_PREFIX will be set to context.install_dir
    
    Arguments:
    context -- BuildContext instance
    options -- dictionary of CMake cache variables
    build_dir -- the directory used for the build (defaults to ./cmake_build)
    """
    if not build_dir:
        build_dir = "cmake_build"
    
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
        
    os.chdir(build_dir)
    
    args = ["-D", "CMAKE_INSTALL_PREFIX=" + context.install_dir]
    for i in options.iteritems():
        args.extend(["-D", "=".join(i)])
    args.extend(["-G", cmake_generator(context.toolchain, context.arch)])
    args.append(os.path.relpath(".", build_dir))
    
    system.run_cmd("cmake", args)
    
    os.chdir("..")

def vc_version(toolchain):
    """Return the Visual C++ version from the toolchain string"""
    if toolchain.startswith("vc"):
        return toolchain[2:]
    
def vcproj_ext(version):
    """Return file extension for Visual C++ projects"""
    if int(version) > 9:
        return ".vcxproj"
    else:
        return ".vcproj"
    
def vcbuild(context, filepath, config, extras=[], ignore_errors=False):
    """Build a Visual C++ project file or solution
    
    Uses vcbuild for vc9 and older, msbuild otherwise 
    
    Arguments:
    context -- BuildContext instance
    filepath -- path to project or solution
    config -- the solution configuration to use
    extras -- extra command line options to pass to vcbuild or msbuild
    ignore_errors -- ignore CalledProcessError or not
    """
    if context.arch == "x64":
        platform = "Win64"
    else:
        platform = "Win32"
        
    if int(vc_version(context.toolchain)) > 9:
        system.run_cmd("msbuild", [filepath, "/m", "/nologo", "/verbosity:minimal",
                                   "/p:Configuration=" + config,
                                   "/p:Platform=" + platform] + extras, 
                                   ignore_errors=ignore_errors)
    else:    
        system.run_cmd("vcbuild", [filepath, "{0}|{1}".format(config, platform)] + extras, 
                       ignore_errors=ignore_errors)
    
    