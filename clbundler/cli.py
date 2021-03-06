import commands
from commandparser import Subcommand
import config

def on_new(parser, options, args):
    if len(args) < 3:
        parser.error("too few arguments")
    if not (args[2] == "x86" or args[2] == "x64"):
        parser.error("Unknown architecture '{0}' (needs to be one of [x86, x64])".format(args[2]))
    commands.cmd_new(args[0], args[1], args[2])

def on_use(parser, options, args):
    if not args:
        parser.error("no bundle specified")
    commands.cmd_set(args[0])
    
def on_install(parser, options, args):
    if not args:
        parser.error("no formula specified")
    for n in args:
        commands.cmd_install(n, options)

def on_uninstall(parser, options, args):
    if not args:
        parser.error("no formula specified")
    for n in args:
        commands.cmd_uninstall(n, options.keep_dependent)
    
def on_archive(parser, options, args):
    commands.cmd_archive(options.path)

def on_info(parser, options, args):
    commands.cmd_info()
    
def on_formula_path(parser, options, args):
    if not args:
        print(config.global_config().get("Paths", "formula_dirs"))
    else:
        commands.cmd_set_formula_path(args[0], options.append)
        
def on_list(parser, options, args):
    if not args:
        parser.error("no package name specified")
    else:
        commands.cmd_list(args[0], options.category)

def setup_parser(parser):
    parser.usage = "clbundler <command> [options]" 
    parser.description = "Type 'clbundler <command> --help' for more information "\
                         "on a specific command"
    
    usage = "{0} {1} [options]"

    subcommand = Subcommand("new", callback=on_new,
                            usage=usage.format("new","PATH TOOLCHAIN ARCH"), 
                            short_help="Sets up a new bundle",
                            detailed_help="Currently, only vc9 is the only supported TOOLCHAIN")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("use", callback=on_use,
                            usage=usage.format("use","PATH"), 
                            short_help="Use an already existing bundle")
    parser.add_subcommand(subcommand)

    subcommand = Subcommand("install", callback=on_install,
                            usage=usage.format("install","FORMULA"),
                            short_help="Install a library into a bundle")
    subcommand.add_option("-f", "--force", dest="force", action="store_true",
                          help="Install even if already installed")
    subcommand.add_option("-i", "--interactive", dest="interactive", action="store_true",
                          help="Start a shell after downloading and patching the source")
    subcommand.add_option("--clean-src", dest="clean_src", action="store_true",
                          help="Use clean source tree")
    subcommand.add_option("--variant", dest="variant", action="store", choices=("release", "debug", "release+debug"),
                          help="Specify build variant {release, debug, release+debug}")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("uninstall", callback=on_uninstall,
                            usage=usage.format("uninstall","PACKAGE"),
                            short_help="Remove a library from a bundle")
    subcommand.add_option("-k", "--keep", dest="keep_dependent", action="store_true",
                          help="Do not also uninstall packages that require PACKAGE")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("archive", callback=on_archive,
                            usage="archive [options]",
                            short_help="Create a compressed archive of current bundle")
    subcommand.add_option("-p", "--path", dest="path",
                          help="Specify a directory to create the archive in")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("formula-path", callback=on_formula_path,
                            usage=usage.format("use","PATH"),
                            short_help="Set the formula search path",
                            detailed_help="If no arguments are given, the current search path is printed")
    subcommand.add_option("-a", "--append", dest="append", action="store_true",
                          help="Append the current value instead replacing")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("info", callback=on_info,
                            usage=usage.format("info","[PACKAGE]"),
                            short_help="Show information about installed packages",
                            detailed_help="If PACKAGE is not given, all installed packages will be shown")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("list", callback=on_list,
                            usage=usage.format("list","PACKAGE"),
                            short_help="List files that belong to PACKAGE")
    subcommand.add_option("-c", "--category", dest="category", choices=("run", "run_dbg", "build"),
                          help="Only show files belonging to a specific category:\n{run, run_dbg, build}")
    parser.add_subcommand(subcommand)
