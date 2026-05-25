import os
import glob
import re

files = glob.glob('client/src/*.jsx')

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()

    # Replace rogue slate buttons with blue/indigo
    content = re.sub(r'bg-slate-900', 'bg-blue-600', content)
    content = re.sub(r'hover:bg-slate-800', 'hover:bg-blue-700', content)
    content = re.sub(r'bg-slate-800', 'bg-blue-700', content)
    content = re.sub(r'text-slate-900', 'text-blue-900', content)
    content = re.sub(r'text-slate-800', 'text-blue-800', content)
    
    # Standardize structure borders and rounding
    content = re.sub(r'rounded-sm md:rounded-lg', 'rounded-xl', content)
    content = re.sub(r'rounded-sm md:rounded-xl', 'rounded-xl', content)
    content = re.sub(r'border-slate-200', 'border-gray-200', content)
    content = re.sub(r'border-slate-100', 'border-gray-100', content)
    content = re.sub(r'bg-slate-50', 'bg-gray-50', content)
    
    # Headers/Heroes - Find common header patterns and replace background
    # (Simple heuristic for div headers that are often white/slate)
    content = re.sub(r'className="([^"]*)bg-white([^"]*)border-b([^"]*)"', 
                     r'className="\1bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900\2border-b\3"', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

print("UI fixes applied to client/src/*.jsx")
