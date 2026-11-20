"""公開してはいけない情報がファイルに含まれていないかを調べる。

ローカルでもCIでも実行する:  python tools/check_sensitive.py
見つかった場合は終了コード1で終わる。
"""

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "Windowsのユーザーフォルダのパス": re.compile(
        r"[A-Za-z]:\\+Users\\+(?!<user>)[^\\\s<>]+", re.I
    ),
    "macOS/Linuxのホームフォルダのパス": re.compile(
        r"/(?:Users|home)/(?!<user>|runner\b)[A-Za-z0-9._-]+"
    ),
    "AWSのARN（アカウントIDを含む）": re.compile(r"arn:aws[a-z-]*:[^\s:]*:[^\s:]*:\d{12}"),
    "AWSのアクセスキー": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "NVIDIA NGCのAPIキー": re.compile(r"\bnvapi-[A-Za-z0-9_-]{20,}"),
    "秘密鍵": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
}

SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".pt", ".pth", ".onnx", ".usd"}


def tracked_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
        return [Path(p) for p in out.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in Path(".").rglob("*") if p.is_file() and ".git" not in p.parts]


def main() -> int:
    findings = []
    this_file = Path(__file__).resolve()
    for path in tracked_files():
        if path.suffix.lower() in SKIP_SUFFIXES or path.resolve() == this_file:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(f"{path}:{lineno}: {label}")
    if findings:
        print("公開前に確認が必要な箇所があります:")
        print("\n".join(findings))
        return 1
    print("OK: 問題は見つかりませんでした")
    return 0


if __name__ == "__main__":
    sys.exit(main())
