import os
import sys
import re

LICENSE_HEADER = """
# Copyright [yyyy] Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""".strip()


def create_license_regex(license_template):
    """Creates a regex from the license template string."""
    # Escape special regex characters
    escaped_template = re.escape(license_template)

    # Replace the year placeholder with a regex pattern,
    # and account for the optional projects/<numerical-value> at EOL
    year_pattern = r"(\d{4})"
    eol_pattern = r"(?: projects/\d+)?"
    regex_str = (
        escaped_template.replace(re.escape("[yyyy]"), year_pattern) + eol_pattern
    )

    # The above replacement might not catch the EOL part correctly if
    # the [yyyy] is not at the very end of the line.
    # Let's split the first line and handle it specifically.
    lines = regex_str.split(r"\\n", 1)
    if len(lines) > 1:
        lines[0] = lines[0] + eol_pattern
        regex_str = r"\\n".join(lines)

    return re.compile(r"^" + regex_str + r"\n?", re.MULTILINE)


LICENSE_HEADER_REGEX = create_license_regex(LICENSE_HEADER)


def check_file(filepath):
    """Checks if the given file has the correct license header."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
            if LICENSE_HEADER_REGEX.match(content):
                return True
            else:
                print(f"ERROR: Missing or incorrect license header in: {filepath}")
                # Optionally print the expected header for easier debugging
                # print(f"Expected:\n{LICENSE_HEADER}\n")
                return False
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return False


def main():
    """Checks all Python files in the current directory (recursively)."""
    failed = False
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(
                __file__
            ):  # Exclude self
                filepath = os.path.join(root, file)
                if not check_file(filepath):
                    failed = True

    if failed:
        sys.exit(1)
    else:
        print("License header check passed for all Python files.")
        sys.exit(0)


if __name__ == "__main__":
    main()
