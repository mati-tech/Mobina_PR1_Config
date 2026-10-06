"""Shell module handling command parsing and execution."""
import shlex
import os
import sys

class Shell:
    """Core shell emulator class."""
    
    def __init__(self, vfs):
        """Initialize shell with a VFS instance."""
        self.vfs = vfs
        self.running = True
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "cat": self.cmd_cat,
            "echo": self.cmd_echo,
            "mkdir": self.cmd_mkdir,
            "find": self.cmd_find,
            "tac": self.cmd_tac,
            "who": self.cmd_who,
            "exit": self.cmd_exit,
        }

    def _get_prompt(self):
        """Generate the shell prompt string."""
        return f"{self.vfs.cwd} $ "

    def _print_error(self, msg):
        """Print error message to stderr."""
        print(f"Error: {msg}", file=sys.stderr)

    def parse_and_execute(self, line):
        """Parse a command line and execute the corresponding command."""
        try:
            parts = shlex.split(line.strip())
        except ValueError as e:
            self._print_error(f"Parsing error: {e}")
            return
        
        if not parts:
            return
        
        cmd_name = parts[0]
        args = parts[1:]
        
        if cmd_name in self.commands:
            self.commands[cmd_name](args)
        else:
            self._print_error(f"Unknown command: {cmd_name}")

    def start_repl(self):
        """Start the interactive REPL loop."""
        print("Welcome to UNIX Shell Emulator. Type 'exit' to quit.")
        while self.running:
            try:
                line = input(self._get_prompt())
                self.parse_and_execute(line)
            except (KeyboardInterrupt, EOFError):
                print()
                self.running = False

    def execute_script(self, filepath):
        """Execute commands from a script file."""
        if not os.path.exists(filepath):
            self._print_error(f"Script not found: {filepath}")
            return
        
        print(f"--- Executing Script: {filepath} ---")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    print(f"{self._get_prompt()}{line}")
                    self.parse_and_execute(line)
                    if not self.running:
                        break
        except Exception as e:
            self._print_error(f"Script execution failed: {e}")
        print("--- Script Finished ---")

    def cmd_ls(self, args):
        """List directory contents."""
        path = args[0] if args else self.vfs.cwd
        items, err = self.vfs.list_dir(path)
        if err:
            self._print_error(err)
        else:
            print("  ".join(items))

    def cmd_cd(self, args):
        """Change current directory."""
        if not args:
            self._print_error("cd: missing argument")
            return
        
        path = args[0]
        node = self.vfs.get_node(path)
        if not node:
            self._print_error(f"cd: no such file or directory: {path}")
        elif node['type'] != 'dir':
            self._print_error(f"cd: not a directory: {path}")
        else:
            self.vfs.cwd = self.vfs.resolve_path(path)

    def cmd_cat(self, args):
        """Print file contents."""
        if not args:
            self._print_error("cat: missing argument")
            return
        
        content, err = self.vfs.read_file(args[0])
        if err:
            self._print_error(f"cat: {err}")
        else:
            print(content)

    def cmd_echo(self, args):
        """Print arguments to stdout."""
        print(" ".join(args))

    def cmd_mkdir(self, args):
        """Create a new directory."""
        if not args:
            self._print_error("mkdir: missing argument")
            return
        
        err = self.vfs.create_dir(args[0])
        if err:
            self._print_error(f"mkdir: {err}")

    def cmd_find(self, args):
        """Find files by name."""
        if len(args) < 2 or args[1] != "-name":
            self._print_error("find: usage: find <path> -name <pattern>")
            return
        
        path = args[0]
        pattern = args[2]
        results, err = self.vfs.find_file(path, pattern)
        if err:
            self._print_error(f"find: {err}")
        else:
            for res in results:
                print(res)

    def cmd_tac(self, args):
        """Print file contents in reverse."""
        if not args:
            self._print_error("tac: missing argument")
            return
        
        content, err = self.vfs.read_file(args[0])
        if err:
            self._print_error(f"tac: {err}")
        else:
            lines = content.splitlines()
            for line in reversed(lines):
                print(line)

    def cmd_who(self, args):
        """Print current user information."""
        print("user     pts/0        2023-10-27 10:00")

    def cmd_exit(self, args):
        """Exit the shell."""
        self.running = False