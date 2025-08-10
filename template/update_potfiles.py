#!/usr/bin/env python
import sys
import os

SRC_DIR = "src/"
POTFILES_PATH = f"{os.getenv('POTFILES_FILE')}"


def find_translation_files():
    translation_files = []

    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Only check text-based files (e.g., .py, .html, etc.)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "_('" in content or '_("' in content:
                        translation_files.append(file_path)
            except (UnicodeDecodeError, FileNotFoundError):
                # Skip files that can't be decoded (binary or unreadable)
                continue

    # Manually add in non-src files to be translated
    translation_files += [
        "data/{{APP_ID}}.desktop.in",
        "data/{{APP_ID}}.metainfo.xml.in",
        "data/{{APP_ID}}.gschema.xml",
    ]

    translation_files = sorted(translation_files)
    return translation_files


def write_to_file(files):
    with open(POTFILES_PATH, "w") as f:
        for line in files:
            f.write(f"{line}\n")
            print("Wrote", line, "to", POTFILES_PATH)


if __name__ == "__main__":
    if not os.path.exists(POTFILES_PATH):
        print("No POTFIELS file found at:", POTFILES_PATH)
        sys.exit(1)

    if not os.path.exists(SRC_DIR):
        print("SRC_DIR path is not found, path:", SRC_DIR)
        sys.exit(1)

    translation_files = find_translation_files()
    write_to_file(translation_files)
    print("Updated", POTFILES_PATH, "\n")
