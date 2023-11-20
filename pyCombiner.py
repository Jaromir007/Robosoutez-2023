import argparse
import ast
import os
import re

ignoredLibraries = ["pybricks"]

# Written by chatGPT
def get_module_paths(script_path):

    module_paths = set()

    def visit_Import(node):
        for alias in node.names:
            module_paths.add(alias.name)

    def visit_ImportFrom(node):
        if node.module is not None:
            module_paths.add(node.module)

    def visit(node):
        if isinstance(node, ast.Import):
            visit_Import(node)
        elif isinstance(node, ast.ImportFrom):
            visit_ImportFrom(node)
        for child_node in ast.iter_child_nodes(node):
            visit(child_node)

    with open(script_path, 'r') as file:
        tree = ast.parse(file.read(), filename=script_path)

    visit(tree)

    script_directory = os.path.dirname(os.path.abspath(script_path))
    module_paths = [os.path.join(script_directory, module.replace('.', os.sep) + '.py') for module in module_paths]

    return module_paths

def keep_first_occurrence(input_array):
    unique_strings = set()
    result_array = []

    for string in input_array:
        if string not in unique_strings:
            result_array.append(string)
            unique_strings.add(string)

    return result_array

# Create argument parser
parser = argparse.ArgumentParser(description='Argument Parser Example')
# Add required rootFile argument
parser.add_argument('rootFile', type=str, help='Root file string (required)')
# Parse the arguments
args = parser.parse_args()
# Access the arguments
rootFile = args.rootFile

# Check if the file exists
if not os.path.isfile(rootFile):
    print("File not found.")
    exit(-1)

moduleQueue = []

def addToQueue(path):
    moduleQueue.append(path)
    importedModulesPaths = get_module_paths(path)
    for modulePath in importedModulesPaths:
        for ignoredLib in ignoredLibraries:
            if not ignoredLib in modulePath:
                print(f'Combining {modulePath} to out.py')
                addToQueue(modulePath)

print(f'Combining {os.path.abspath(rootFile)} to out.py')
addToQueue(os.path.abspath(rootFile))

# Reverse the array
moduleQueue.reverse()

# Filter out duplicates
moduleQueue = keep_first_occurrence(moduleQueue)

with open(f'out.py', 'w') as outFile:
    outFile.write("#!/usr/bin/env pybricks-micropython\n")
    outFile.write("# Auto generated file\n")
    outFile.write("# Pybricks modules \nfrom pybricks.hubs import EV3Brick \nfrom pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor) \nfrom pybricks.parameters import Port, Stop, Direction, Button, Color \nfrom pybricks.tools import wait, StopWatch, DataLog \nfrom pybricks.robotics import DriveBase \nfrom pybricks.media.ev3dev import SoundFile, ImageFile\n")
    
    for modulePath in moduleQueue:
        outFile.write(f'\n#===========================================\n#{modulePath}\n#===========================================\n')
        moduleString = open(modulePath, "r").read()
        moduleString = re.sub(r'^\s*import\s+.*$\n', '', moduleString, flags=re.MULTILINE)
        moduleString = re.sub(r'^\s*from\s+.*\s+import\s+.*$\n', '', moduleString, flags=re.MULTILINE)
        outFile.write(moduleString)