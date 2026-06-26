"""
Git MCP Server — exposes git operations as MCP tools for SDLC workflows.
"""

import subprocess
import os
from mcp.server.fastmcp import FastMCP

# Ensure git is on PATH when Claude Code spawns this server on Windows
_GIT_DIRS = [
    r"C:\Program Files\Git\mingw64\bin",
    r"C:\Program Files\Git\cmd",
]
for _d in _GIT_DIRS:
    if os.path.isdir(_d) and _d not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _d + os.pathsep + os.environ.get("PATH", "")

REPO = os.path.dirname(os.path.abspath(__file__))

mcp = FastMCP("git-mcp")


def _git(*args: str) -> dict:
    result = subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True,
        text=True,
    )
    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode,
    }


# ── Status & Info ────────────────────────────────────────────────────────────

@mcp.tool()
def git_status() -> dict:
    """Show the working tree status (staged, unstaged, untracked files)."""
    return _git("status", "--short", "--branch")


@mcp.tool()
def git_log(n: int = 10) -> dict:
    """Show the last n commits with hash, author, date, and subject."""
    return _git("log", f"-{n}", "--pretty=format:%h | %an | %ar | %s")


@mcp.tool()
def git_diff(staged: bool = False) -> dict:
    """Show unstaged diff. Set staged=True to see staged (index) diff."""
    args = ["diff"]
    if staged:
        args.append("--cached")
    return _git(*args)


@mcp.tool()
def git_show(ref: str = "HEAD") -> dict:
    """Show details of a specific commit (default: HEAD)."""
    return _git("show", "--stat", ref)


# ── Branching ────────────────────────────────────────────────────────────────

@mcp.tool()
def git_branch_list() -> dict:
    """List all local branches, marking the current one."""
    return _git("branch", "-v")


@mcp.tool()
def git_branch_create(name: str) -> dict:
    """Create a new branch from current HEAD."""
    return _git("checkout", "-b", name)


@mcp.tool()
def git_checkout(branch: str) -> dict:
    """Switch to an existing branch."""
    return _git("checkout", branch)


@mcp.tool()
def git_merge(branch: str) -> dict:
    """Merge the given branch into the current branch."""
    return _git("merge", "--no-ff", branch, "-m", f"Merge branch '{branch}'")


@mcp.tool()
def git_branch_delete(name: str, force: bool = False) -> dict:
    """Delete a local branch. Use force=True to force-delete unmerged branches."""
    flag = "-D" if force else "-d"
    return _git("branch", flag, name)


# ── Staging & Committing ─────────────────────────────────────────────────────

@mcp.tool()
def git_add(path: str = ".") -> dict:
    """Stage files for commit. path can be a file, directory, or '.' for all."""
    return _git("add", path)


@mcp.tool()
def git_commit(message: str) -> dict:
    """Create a commit with the given message."""
    return _git("commit", "-m", message)


@mcp.tool()
def git_reset(path: str = "", hard: bool = False) -> dict:
    """Unstage a file, or reset HEAD (hard=True discards working tree changes too)."""
    if hard:
        return _git("reset", "--hard", "HEAD")
    if path:
        return _git("reset", "HEAD", "--", path)
    return _git("reset", "HEAD")


# ── Remote Operations ─────────────────────────────────────────────────────────

@mcp.tool()
def git_pull(remote: str = "origin", branch: str = "") -> dict:
    """Pull latest changes from remote."""
    args = ["pull", remote]
    if branch:
        args.append(branch)
    return _git(*args)


@mcp.tool()
def git_push(remote: str = "origin", branch: str = "", set_upstream: bool = False) -> dict:
    """Push commits to remote. set_upstream=True adds -u flag."""
    args = ["push"]
    if set_upstream:
        args.append("-u")
    args.append(remote)
    if branch:
        args.append(branch)
    return _git(*args)


@mcp.tool()
def git_remote_list() -> dict:
    """List configured remotes with their URLs."""
    return _git("remote", "-v")


# ── Tags ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def git_tag_create(name: str, message: str = "") -> dict:
    """Create a tag. Provide message for an annotated tag."""
    if message:
        return _git("tag", "-a", name, "-m", message)
    return _git("tag", name)


@mcp.tool()
def git_tag_list() -> dict:
    """List all tags."""
    return _git("tag", "-l", "--sort=-version:refname")


if __name__ == "__main__":
    mcp.run()
