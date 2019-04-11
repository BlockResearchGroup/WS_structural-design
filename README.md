# WS_structural-design

Workshop on Structural Design with COMPAS

**Schedule**

*   10.00: Introduction -- *Short presentation about the structure of COMPAS*
*   10.30: Installation & Examples -- *Install a released version of COMPAS*
*   11.00: Installing from source -- *Install the latest COMPAS version in a separate environment*
*   11.30: Contributing -- *Submitting pull requests from a fork*
*   12.00: Lunch
*   13.00: Packages -- *Make your own package*
*   14.00: compas_fofin -- *Install compas_fofin from source*
*   15.00: Case study: HiLo shell -- *Generating structural geometry from a data structure*

**Requirements**

*   Operating System: Mac (OSX) or Windows
*   [Anaconda Python Distribution](https://www.anaconda.com/download/): 3.7
*   [Rhino](https://www.rhino3d.com/)
*   Code editor: [ST3](https://compas-dev.github.io/main/environments/sublimetext.html) or [VS Code](https://compas-dev.github.io/main/environments/vscode.html)
*   Git: [official command-line client](https://git-scm.com/)
*   Git GUI: SourceTree, Github Desktop, ...

> **Note**
>
> When installing Anaconda, use the default settings.
> And make sure Anaconda is installed on your home drive to avoid problems with
> admin rights further down the road.
> In my experience, a default install should result in the following
>
> * On Windows: ``%USERPROFILE%\Anaconda3``
> * On Mac: ``~/Anaconda3``

---

## Introduction

[Draft slides](https://docs.google.com/presentation/d/1ShrSs-ZNuvNCekuP1iqGNFOmCickg6J_fNtqn5D3Rz0/edit?usp=sharing)

## Getting started

> **Note**
>
> Most of the following procedures are executed using the command line.
> On Mac this means the Terminal.
> On Windows, you should use the Anaconda Prompt and run it as administrator.

**Clone the workshop repo**

https://github.com/BlockResearchGroup/WS_structural-design.git

*On Windows*

```bash
mkdir %USERPROFILE%\Code
mkdir %USERPROFILE%\Code\Workshops
cd %USERPROFILE%\Code\Workshops
git clone https://github.com/BlockResearchGroup/WS_structural-design.git
```

*On Mac*

```bash
mkdir ~/Code
mkdir ~/Code/Workshops
cd ~/Code/Workshops
git clone https://github.com/BlockResearchGroup/WS_structural-design.git
```

**Clean up path variables**

*   Remove COMPAS from `PYTHONPATH`
*   Remove COMPAS from `Module Search Path` in Rhino
*   Remove COMPAS from `RhinoSettings` in Atom

## Installation

**Install the latest released version of COMPAS (`0.5.1`) using `conda`**

```bash
conda config --add channels conda-forge
conda install COMPAS
```

**Check your installation**

Launch the interactive Python interpreter and import `compas`, `compas_rhino`, `compas_ghpython`.

```bash
>>> import compas
>>> import compas_rhino
>>> import compas_ghpython
>>> compas.__version__
0.5.1
```

If no error messages appear and the COMPAS version is correct, you're good to go.
Type `exit()` to quit the interpreter.

**Install COMPAS for Rhino**

To make the installed COMPAS packages available in Rhino run the following on the command line

```bash
python -m compas_rhino.install -v 5.0
```

> **Note** (Windows only)
>
> Use `-v 6.0` instead of `-v 5.0` if you want to use Rhino 6 instead of Rhino 5.

Open Rhino and run `verify_rhino.py`.
If this does not throw an error and prints the correct COMPAS version (`0.5.1`),
Rhino is properly configured.

> **Note**
>
> To run a script in Rhino, just type `RunPythonScript` at the Rhino command prompt
> and select the script you want to run.

**Configure your editor**

*   Sublime Text 3: https://compas-dev.github.io/main/environments/sublimetext.html
*   VS Code: https://compas-dev.github.io/main/environments/vscode.html

Finally, run `verify_editor.py` to check the setup.
If this prints `0.5.1` in the Terminal window,your editor is properly configured.

## Examples

*   Plotters
    *   Shortest path (plot): [network_shortestpath.py](examples/network_shortestpath.py)
        <br />*Plot the shortest path between two vertices of a network.*
    *   Shortest path (interactive plot): [network_shortestpath.py](examples/network_shortestpath.py)
        <br />*Plot the shortest path between a given start vertex and a point picked by the user.*
    *   Equilibrium (dynamic plot): [network_equilibrium.py](examples/network_equilibrium.py)
        <br />*Plot the dynamic relaxation process of a network with randomly prescribed edge force densities.*
*   Rhino
    *   Subdivision: [mesh_subdivision_rhino.py](examples/mesh_subdividion_rhino.py)
        <br />*Generate a subdivision surface using a control mesh.*
    *   Mesh smoothing: [mesh_smoothing_rhino.py](examples/mesh_smoothing_rhino.py)
        <br />*Smooth a mesh on a given target surface.*
*   RPC
    *   Equilibrium: [rpc_fd_rhino.py](examples/rpc_fd_rhino.py)
        <br />*Force desnity calculation using Numpy/Scipy.*
    *   CDT: [rpc_cdt_rhino.py](examples/rpc_cdt_rhino.py)
        <br />*Constrained Delaunay Triangulation using triangle.*
        <br />Note that for this example you have to install `triangle`.

---

## Installing from source

Install the latest unreleased version of COMPAS from the cloned Github repo in a separate Python *virtual environment*.

**Clone the COMPAS repo**

*On Windows*

```bash
mkdir %USERPROFILE%\Code\compas-dev
cd %USERPROFILE%\Code\compas-dev
git clone https://github.com/compas-dev/compas.git
cd compas
```

*On Mac*

```bash
mkdir ~/Code/compas-dev
cd ~/Code/compas-dev
git clone https://github.com/compas-dev/compas.git
cd compas
```

**Create and activate a virtual environment**

```bash
conda create -n unreleased
conda activate unreleased
```

> **Note**
>
> The active environment is listed before the prompt on the command line.
> After activating the environment you should thuse see something like this
> `(unreleased) $` or `(unreleased) >` instead of `(base) $` or `(base) >`.

**Create an editable installation**

```bash
pip install -e .
```

**Update Rhino**

```bash
python -m compas_rhino.uninstall -v 5.0
python -m compas_rhino.install -v 5.0
```

## Contributing

All contributions to the main library of COMPAS are handled through pull requests.
To be able to issue a pull request, you need to install COMPAS via a forked repo.

**Fork COMPAS to your personal account**

Go to https://github.com/compas-dev/compas and click `Fork` on the top right of the page.
Select your personal account as the fork location.

**Clone the fork to your computer**

*On Windows*

```bash
mkdir %USERPROFILE%\Code\<github username>
cd %USERPROFILE%\Code\<github username>
git clone https://github.com/<github username>/compas.git
cd compas
```

*On Mac*

```bash
mkdir ~/Code/<github username>
cd ~/Code/<github username>
git clone https://github.com/<github username>/compas.git
cd compas
```

**Create and activate a virtual environment**

```bash
conda create -n contrib
conda activate contrib
```

**Create an editable installation**

```bash
pip install -e .
```

**Update Rhino**

```bash
python -m compas_rhino.uninstall -v 5.0
python -m compas_rhino.install -v 5.0
```

**Exercise**

*Under construction...*

---

## Make your own package

*Under construction...*

## Install `compas_fofin` from source

*Under construction...*

---

## Case study: HiLo shell

*Under construction...*

---

## Troubleshooting

If you have a problem and don't find the solution here, please submit an issue on the issue tracker of the repository.

> **Problem**
> <br />*error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools*

Follow the link to install Microsoft Visual C++ 14.0
https://www.scivision.co/python-windows-visual-c++-14-required/

> **Problem**
> <br />*Exception: The lib folder for IronPython does not exist in this location: C:\Users\AppData\Roaming\McNeel\Rhinoceros\6.0\Plug-ins\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\settings\lib*

This happens if you have a brand new installation of Rhino.
After opening Rhino and the PythonScriptEditor for the first time, the required folders will be created automatically.

> **Problem** 
> <br />*NoneType object has no attribute Geometry*

This sometimes happens in Rhino when wrapping Rhino Geometry.
Just reset the script engine and try again.

```
Tools > PythonScript > Edit > Tools > Reset Script Engine
```

> **Problem**
> <br />*I don't see the DisplayConduit in Rhino on Mac*

DisplayConduits are not supported yet on Mac. The result should be correct though...

