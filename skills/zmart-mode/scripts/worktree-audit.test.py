import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class WorktreeAuditTest(unittest.TestCase):
    def test_spaced_paths_and_explicit_transcript_exports(self):
        script = Path(__file__).with_name("worktree-audit.sh").resolve()
        with tempfile.TemporaryDirectory(prefix="worktree audit ") as temporary:
            root = Path(temporary).resolve()
            repo, worktree = root / "main repo", root / "worker tree"
            binaries = root / "bin"
            binaries.mkdir()
            for name in ("origin", "gh"):
                executable = binaries / name
                executable.write_text("#!/bin/sh\nexit 1\n")
                executable.chmod(0o755)

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=root, capture_output=True, text=True, check=True
                )

            git("init", str(repo))
            git("-C", str(repo), "-c", "user.name=Test", "-c",
                "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "test")
            git("-C", str(repo), "worktree", "add", "-b", "worker", str(worktree))
            environment = dict(os.environ, PATH=str(binaries) + os.pathsep + os.environ["PATH"])

            def audit(*args):
                output = subprocess.run(
                    ["bash", str(script), "-b", "HEAD", *args, str(repo)],
                    env=environment, capture_output=True, text=True, check=True,
                ).stdout
                return output.splitlines()[-1].split("\t")

            row = audit()
            self.assertEqual(row[-1], str(worktree))
            self.assertEqual(row[-2], "verify-unused")
            exports = root / "chat exports"
            exports.mkdir()
            transcript = exports / "chat export.txt"
            transcript.write_text(str(worktree) + "/file.ts")
            self.assertEqual(audit("--transcripts", str(exports))[-2], "verify-recent-chat")
            transcript.write_text(str(worktree) + "-other/file.ts")
            self.assertEqual(audit("--transcripts", str(exports))[-2], "verify-unused")
            (worktree / "user notes.txt").write_text("keep this")
            self.assertTrue(audit()[3].startswith("scratch:"))
            self.assertEqual((worktree / "user notes.txt").read_text(), "keep this")


if __name__ == "__main__":
    unittest.main()
