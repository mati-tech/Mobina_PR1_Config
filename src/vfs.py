"""Virtual File System module for the UNIX shell emulator."""
import csv
import base64
import os
import posixpath


class VFS:
    """Manages the virtual file system loaded from a CSV file."""

    def __init__(self):
        """Initialize an empty VFS."""
        self.nodes = {}
        self.cwd = "/"
        self._add_node("/", "", "dir", "")

    def _add_node(self, name, parent, node_type, content):
        """Add a single node to the internal dictionary."""
        if not parent:
            parent = "/"
        parent = posixpath.normpath(parent)
        if not parent.startswith("/"):
            parent = "/" + parent

        path = posixpath.join(parent, name)
        path = posixpath.normpath(path)
        if not path.startswith("/"):
            path = "/" + path

        self.nodes[path] = {
            "name": name,
            "parent": parent,
            "type": node_type,
            "content": content,
        }

    def load_csv(self, filepath):
        """Load VFS data from a CSV file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"VFS file not found: {filepath}")
        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self._add_node(
                        row["name"].strip(),
                        row["parent"].strip(),
                        row["type"].strip(),
                        row.get("content", ""),
                    )
        except Exception as e:
            raise ValueError(f"Error parsing VFS CSV: {e}")

    def resolve_path(self, path):
        """Resolve a given path relative to the current working directory."""
        if not path:
            return self.cwd
        if path.startswith("/"):
            resolved = path
        else:
            resolved = posixpath.join(self.cwd, path)
        resolved = posixpath.normpath(resolved)
        if not resolved.startswith("/"):
            resolved = "/" + resolved
        return resolved

    def get_node(self, path):
        """Retrieve a node by its absolute path."""
        return self.nodes.get(self.resolve_path(path))

    def read_file(self, path):
        """Read content of a file node."""
        node = self.get_node(path)
        if not node:
            return None, "File not found"
        if node["type"] != "file":
            return None, "Not a file"
        content = node["content"]
        try:
            decoded = base64.b64decode(content).decode("utf-8")
            return decoded, None
        except Exception:
            return content, None

    def list_dir(self, path):
        """List contents of a directory."""
        node = self.get_node(path)
        if not node:
            return None, "Directory not found"
        if node["type"] != "dir":
            return None, "Not a directory"
        resolved = self.resolve_path(path)
        children = []
        for p, n in self.nodes.items():
            if n["parent"] == resolved and p != resolved:
                children.append(n["name"])
        return children, None

    def create_dir(self, path):
        """Create a new directory in memory."""
        resolved = self.resolve_path(path)
        if resolved in self.nodes:
            return "Directory already exists"
        parent_path = posixpath.dirname(resolved) or "/"
        parent_node = self.get_node(parent_path)
        if not parent_node or parent_node["type"] != "dir":
            return "Parent directory does not exist"
        name = posixpath.basename(resolved)
        self._add_node(name, parent_path, "dir", "")
        return None

    def find_file(self, start_path, name_pattern):
        """Find files matching a pattern starting from a path."""
        start_node = self.get_node(start_path)
        if not start_node:
            return None, "Start path not found"
        resolved_start = self.resolve_path(start_path)
        results = []
        for p, n in self.nodes.items():
            if n["name"] == name_pattern and p.startswith(resolved_start):
                results.append(p)
        return results, None