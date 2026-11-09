#!/usr/bin/env python3
"""Keep this folder's copy of the house thesis class in step with the registry.

The copy is vendored: the PDF build reads only committed files and never fetches
anything. `registry-source.json` (beside this script) records which commit of
https://github.com/dataimago/dissertation-thesis-classes the copy came from and
which files it holds. This script has two jobs:

  python3 thesis-class/sync.py check
      Fail when a vendored file differs from the registry at the recorded commit
      (a hand edit, or a file that is missing). Reads nothing newer than that commit.

  python3 thesis-class/sync.py sync [--ref REF] [--profile ID ...]
      Copy the class bundle and the chosen profiles from the registry at REF (a
      branch, tag or commit; default: the recorded commit, which restores the files
      to what they were) and rewrite registry-source.json. `--profile` adds a
      shipped profile (its .yaml and compiled .cfg) to those already vendored.
      Review what changed with `git diff` and commit it as a pull request.

Both read the public registry over HTTPS and need only Python 3 and git. Use
`--from DIR` to read a local checkout of the registry instead (offline use, tests).
Run it from anywhere; paths are relative to the folder that holds `thesis-class/`
(the Quarto book folder: ui/www in an R package, thesis/ in a content-only repo).

Never edit a vendored file by hand: put your institution's rules in a profile of
your own (profiles/<id>.yaml, compiled with thesis-class/thesis-profile.lua).
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

REPO = "dataimago/dissertation-thesis-classes"
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, "registry-source.json")
SCHEMA = 2


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


class Source:
    """Reads files of the registry at one commit, from GitHub or a local checkout."""

    def __init__(self, local):
        self.local = os.path.abspath(local) if local else None

    def resolve(self, ref):
        if len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
            return ref
        if self.local:
            out = subprocess.run(["git", "-C", self.local, "rev-parse", ref + "^{commit}"],
                                 capture_output=True, text=True)
            if out.returncode:
                fail("cannot resolve %s in %s: %s" % (ref, self.local, out.stderr.strip()))
            return out.stdout.strip()
        out = subprocess.run(["git", "ls-remote", "https://github.com/%s.git" % REPO, ref,
                              "refs/heads/%s" % ref, "refs/tags/%s^{}" % ref, "refs/tags/%s" % ref],
                             capture_output=True, text=True)
        if out.returncode or not out.stdout.strip():
            fail("cannot resolve %s in %s: %s" % (ref, REPO, out.stderr.strip() or "no such ref"))
        lines = [ln.split() for ln in out.stdout.strip().splitlines()]
        peeled = [ln for ln in lines if ln[1].endswith("^{}")]
        return (peeled or lines)[0][0]

    def read(self, commit, path):
        if self.local:
            out = subprocess.run(["git", "-C", self.local, "show", "%s:%s" % (commit, path)],
                                 capture_output=True)
            if out.returncode:
                fail("%s not found at %s in %s" % (path, commit[:12], self.local))
            return out.stdout
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, commit, path)
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return resp.read()
        except Exception as err:  # network, 404
            fail("cannot read %s: %s" % (url, err))


def load_manifest():
    try:
        with open(MANIFEST, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as err:
        fail("cannot read %s: %s" % (MANIFEST, err))


def local_path(rel):
    return os.path.join(BOOK, *rel.split("/"))


def check(source):
    manifest = load_manifest()
    commit = manifest["commit"]
    bad = []
    for rel, upstream in sorted(manifest["files"].items()):
        want = source.read(commit, upstream)
        try:
            with open(local_path(rel), "rb") as fh:
                have = fh.read()
        except OSError:
            bad.append("%s: missing" % rel)
            continue
        if have != want:
            bad.append("%s: differs from %s at %s" % (rel, upstream, commit[:12]))
    if bad:
        print("The vendored thesis class differs from %s at %s:" % (REPO, commit[:12]), file=sys.stderr)
        for line in bad:
            print("  " + line, file=sys.stderr)
        print("Do not edit these files by hand. Restore them with: python3 thesis-class/sync.py sync\n"
              "(or move your formatting rules into a profile of your own).", file=sys.stderr)
        sys.exit(1)
    print("%d vendored files match %s at %s (class %s)" %
          (len(manifest["files"]), REPO, commit[:12], manifest["classVersion"]))


def sync(source, ref, extra_profiles):
    manifest = load_manifest()
    commit = source.resolve(ref or manifest["commit"])
    registry = json.loads(source.read(commit, "registry.json").decode("utf-8"))
    if registry.get("schemaVersion") != SCHEMA:
        fail("registry.json at %s has schemaVersion %r; this script reads version %d. "
             "Update the script from the template first." % (commit[:12], registry.get("schemaVersion"), SCHEMA))
    cls = next((c for c in registry["classes"] if c["id"] == manifest["class"]), None)
    if not cls or cls.get("status") != "available":
        fail("class %s is not an available class at %s" % (manifest["class"], commit[:12]))
    ids = list(manifest["profiles"])
    for pid in extra_profiles:
        if pid not in ids:
            ids.append(pid)
    files = {}
    for upstream in [cls["path"]] + list(cls["companions"]):
        files["thesis-class/" + upstream.rsplit("/", 1)[1]] = upstream
    for pid in ids:
        prof = next((p for p in registry["profiles"] if p["id"] == pid), None)
        if not prof:
            fail("no profile %s in the registry at %s (a newer profile needs a newer commit: try --ref main)"
                 % (pid, commit[:12]))
        if prof["class"] != cls["id"]:
            fail("profile %s is for class %s, not %s" % (pid, prof["class"], cls["id"]))
        if prof.get("status") != "available":
            fail("profile %s is %s, not available" % (pid, prof.get("status")))
        for key in ("yaml", "cfg"):
            files["profiles/" + prof[key].rsplit("/", 1)[1]] = prof[key]
    for rel, upstream in sorted(files.items()):
        data = source.read(commit, upstream)
        os.makedirs(os.path.dirname(local_path(rel)), exist_ok=True)
        with open(local_path(rel), "wb") as fh:
            fh.write(data)
    manifest.update({"commit": commit, "classVersion": cls["version"], "profiles": ids, "files": files})
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print("synced %d files from %s at %s (class %s); review with git diff" %
          (len(files), REPO, commit[:12], cls["version"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=["check", "sync"])
    parser.add_argument("--ref", help="sync: branch, tag or commit to copy from (default: the recorded commit)")
    parser.add_argument("--profile", action="append", default=[], help="sync: also vendor this shipped profile")
    parser.add_argument("--from", dest="local", help="read a local checkout of the registry instead of GitHub")
    args = parser.parse_args()
    source = Source(args.local)
    if args.command == "check":
        check(source)
    else:
        sync(source, args.ref, args.profile)


if __name__ == "__main__":
    main()
