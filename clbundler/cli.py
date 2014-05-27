import commands
from commandparser import Subcommand
import config

def on_new(parser, options, args):
    if len(args) < 3:
        parser.error("too few arguments")
    if args[1] != "vc9" and args[0] != "vc12":
        parser.error("only vc9, vc12 are supported at the moment")
    if args[2] != "x86":
        parser.error("only x86 is supported at the moment")
    commands.cmd_new(args[0], args[1], args[2])

def on_install(parser, options, args):
    if not args:
        parser.error("no formula specified")
    for n in args:
        commands.cmd_install(n, options.is_kit)

def on_uninstall(parser, options, args):
    if not args:
        parser.error("no formula specified")
    for n in args:
        commands.cmd_uninstall(n)

def setup_parser(parser):
    parser.usage = "clbundler <command> [options]" 
    parser.description = "Type 'clbundler <command> --help' for more information "\
                         "on a specific command"
    
    usage = "{0} {1} [options]"

    subcommand = Subcommand("new", callback=on_new,
                            usage=usage.format("new","PATH TOOLCHAIN ARCH"), 
                            short_help="Sets up a new bundle",
                            detailed_help="Currently, only vc9 is the only supported TOOLCHAIN, and only x86")
    parser.add_subcommand(subcommand)

    subcommand = Subcommand("install", callback=on_install,
                            usage=usage.format("install","FORMULA"),
                            short_help="Install a library into a bundle")
    subcommand.add_option("--kit", dest="is_kit", action="store_true", default=False,
                          help="Specify if FORMULA is a kit")
    #subcommand.add_option("-f", "--force", dest="force_install", action="store_true",
    #                      help="Force building formulae")
    parser.add_subcommand(subcommand)
    
    subcommand = Subcommand("uninstall", callback=on_uninstall,
                          usage=usage.format("uninstall","FORMULA"),
                          short_help="Remove a library from a bundle")
    parser.add_subcommand(subcommand)