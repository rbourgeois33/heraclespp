import re
import subprocess
import os
import sys

def demangle(symbol):
    """Demangles a C++ mangled symbol using c++filt."""
    try:
        result = subprocess.run(['c++filt', symbol], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return symbol

def extract_functor_name(demangled):
    """
    Try to extract the functor/class name from a demangled C++ symbol.
    """
    match = re.search(r'ParallelFor<([^<>\s]+)', demangled)
    if match:
        full = match.group(1)
        return full.split('<')[0].split('::')[-1]

    match = re.search(r'([a-zA-Z_][\w:]*)::(operator\(\)|execute|.*lambda.*)', demangled)
    if match:
        return match.group(1).split('::')[-1]

    return 'UnknownFunctor'

def replace_mangled_with_functor(line):
    """Replace all mangled symbols in a line with their demangled functor names."""
    mangled_pattern = r'_ZN[\w\d_]+'
    matches = re.findall(mangled_pattern, line)
    for mangled in matches:
        demangled = demangle(mangled)
        functor = extract_functor_name(demangled)
        line = line.replace(mangled, functor)
    return line

def process_file_in_place(input_filename):
    """Processes the file and replaces its content with demangled functor names."""
    with open(input_filename, 'r') as fin:
        lines = fin.readlines()

    with open(input_filename, 'w') as fout:
        for line in lines:
            fout.write(replace_mangled_with_functor(line))

    print(f"Demangled and updated: {input_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python demangle_functors.py <filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    process_file_in_place(input_file)