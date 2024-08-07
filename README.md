# texpack
Pack .tex files into a single .tex file.
This may be useful for arXiv, etc.


## Background
When creating LaTeX documents, it's often convenient to split the work into smaller .tex files using commands like `\input` or `\subfile`. 
However, platforms like arXiv require submissions as a single .tex file.
This package, texpack, addresses this need by packing multiple .tex files connected via `\input` or `\subfile` into a single .tex file. 
The package name is inspired by the JavaScript module [webpack](https://github.com/webpack/webpack), which serves a similar purpose.

## Usage
Install the package if you don't have yet.
```bash
python3 -m pip install texpack
```
Move to your LaTeX project directory.
```bash
cd your/LaTeX/project
```
Call our module to execute. In the 1st argument, apply the root tex file of your project.
```bash
python3 -m texpack root-texfile.tex
```
You'll find a new tex file in the same directory as your root tex file.
By default, the file name of the generated file is in the form "texpack-" added to the beginning of the file you have specified.
In the example above, the file "texpack-root-texfile.tex" will be generated.

## Custom output file name
You can specify the custom output file name by adding the `-o` argument.
```bash
python3 -m texpack root-texfile.tex -o main.tex
```
In the example above, the file "main.tex" will be generated.