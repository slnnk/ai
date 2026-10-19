"""Static Codex JavaScript extraction and conservative shell KB classification.

Counts syntactic command sites, not confirmed execution, output bytes or tokens.
Only Node plus Acorn are required for JavaScript extraction; shell parsing uses
Python's standard library. No transcript command or JavaScript is executed.
"""
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


def extract_shell_calls(sources, *, node='node'):
    """Return aligned extraction records; dependency failures are explicit.

    calls contains literal cmd/workdir dictionaries. unresolved counts dynamic
    exec_command sites, parse_error counts invalid JS sources, and unavailable
    marks sources that could not be inspected (missing Node/Acorn, failed helper).
    """
    if not sources:
        return []
    try:
        process = subprocess.run(
            [node, str(Path(__file__).with_name('token_usage_extract.js'))],
            input=json.dumps(sources), text=True, capture_output=True,
            check=True, timeout=30,
        )
        results = json.loads(process.stdout)
        if not isinstance(results, list) or len(results) != len(sources):
            raise ValueError('invalid extractor result')
        return results
    except (OSError, subprocess.SubprocessError, ValueError):
        return [dict(calls=[], unresolved=0, parse_error=0, exec_nodes=0, unavailable=1)
                for _ in sources]


def pathresolve(path, cwd, home=None):
    home = str(home or Path.home())
    path = path.replace('${HOME}', home).replace('$HOME', home)
    if path == '~' or path.startswith('~/'):
        path = home + path[1:]
    if '$' in path or '`' in path or any(c in path for c in '*?[]'):
        return None
    return os.path.normpath(path if os.path.isabs(path) else os.path.join(cwd, path))


def strip_heredocs(command):
    lines, output, ends = command.splitlines(), [], []
    for line in lines:
        if ends:
            if line.strip() == ends[0]:
                ends.pop(0)
            continue
        output.append(line)
        ends.extend(match.group(1) for match in
                    re.finditer(r"<<-?\s*['\"]?([\w]+)['\"]?", line))
    return '\n'.join(output)


def _shell_groups(command):
    lexer = shlex.shlex(strip_heredocs(command), posix=True, punctuation_chars=';|&()<>\n')
    lexer.whitespace = ' \t\r'
    lexer.whitespace_split = True
    # Preserve newline boundaries after shell comments.
    lexer.commenters = ''
    tokens = list(lexer)
    groups, current, comment = [], [], False
    for token in tokens:
        if token.startswith('#'):
            comment = True
        if re.fullmatch(r'[;|&()\n]+', token):
            if current:
                groups.append((current, '|' if token.strip() == '|' else token))
                current = []
            if '\n' in token:
                comment = False
        elif not comment:
            current.append(token)
    if current:
        groups.append((current, ''))
    return groups


def shell_groups(command):
    try:
        return _shell_groups(command)
    except ValueError:
        return []


def classification_status(command):
    """Whether the shell tokenizer accepted this command (not a shell validator)."""
    try:
        _shell_groups(command)
        return True
    except ValueError:
        return False


def classify_command(command, cwd, ai_root, home=None):
    """Yield one (kind, path) per recognized reader/file, searches use path None.

    Ordinary literal cd, readers and pipelines are supported. Dynamic shell paths,
    loops, custom readers and command substitutions are outside this heuristic.
    """
    cwd, ai_root = str(cwd), os.path.normpath(str(ai_root))
    note = re.compile(re.escape(ai_root) + r'/(?:general|personal|current|companies/[^/]+)/knowledge/.+\.md$')
    groups, output = shell_groups(command), []
    for index, (tokens, separator) in enumerate(groups):
        tokens = list(tokens)
        while tokens and re.match(r'^[A-Za-z_]\w*=', tokens[0]):
            tokens.pop(0)
        if not tokens:
            continue
        name, args = os.path.basename(tokens[0]), tokens[1:]
        if name == 'cd' and args:
            cwd = pathresolve(args[0], cwd, home) or cwd
            continue
        if name in ('sudo', 'env', 'command') and args:
            while args and (args[0].startswith('-') or re.match(r'^[A-Za-z_]\w*=', args[0])):
                args = args[1:]
            if not args:
                continue
            name, args = os.path.basename(args[0]), args[1:]
        if name in ('bash', 'sh') and '-c' in args:
            pos = args.index('-c')
            if len(args) > pos + 1:
                output.extend(classify_command(args[pos + 1], cwd, ai_root, home))
            continue
        if name == 'kb_find.py' or (name.startswith('python') and args and os.path.basename(args[0]) == 'kb_find.py'):
            output.append(('kb_find', None))
            continue
        if name in ('rg', 'grep', 'ugrep'):
            if any((path := pathresolve(arg, cwd, home)) and
                   (path == ai_root or path.startswith(ai_root + '/')) for arg in args):
                output.append(('search', None))
            continue
        if name not in ('cat', 'less', 'more', 'bat', 'head', 'tail', 'sed', 'awk'):
            continue
        # Redirected output and heredoc bodies/targets cannot establish note reads.
        if any(arg in ('>', '>>', '<<', '<<-') for arg in args):
            continue
        partial = name in ('head', 'tail', 'sed', 'awk')
        if separator == '|' and index + 1 < len(groups):
            following = groups[index + 1][0]
            if following and os.path.basename(following[0]) in ('head', 'tail', 'sed', 'awk', 'grep', 'rg'):
                partial = True
        files = []
        for arg in args:
            if arg.startswith('-') or arg == '<':
                continue
            path = pathresolve(arg, cwd, home)
            if path and note.fullmatch(path):
                files.append(path)
        for path in dict.fromkeys(files):
            output.append(('index' if path.endswith('/INDEX.md') else 'partial' if partial else 'full', path))
    return output
