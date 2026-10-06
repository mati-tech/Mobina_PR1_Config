"""Main entry point for the UNIX shell emulator."""
import argparse
import sys
from src.vfs import VFS
from src.shell import Shell

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="UNIX Shell Emulator")
    parser.add_argument(
        "--vfs", 
        required=True, 
        help="Path to the VFS CSV file"
    )
    parser.add_argument(
        "--script", 
        required=False, 
        help="Path to the startup script"
    )
    return parser.parse_args()

def main():
    """Main function to initialize and run the shell."""
    args = parse_arguments()
    
    vfs = VFS()
    try:
        vfs.load_csv(args.vfs)
    except (FileNotFoundError, ValueError) as e:
        print(f"VFS Load Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    shell = Shell(vfs)
    
    if args.script:
        shell.execute_script(args.script)
    else:
        shell.start_repl()

if __name__ == "__main__":
    main()