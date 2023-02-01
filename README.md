# patchdyn

A toy tool to patch some dynamic linking related attributes in ELF files.

Depends on [LIEF](https://github.com/lief-project/LIEF/).

Ideas from [patchelf](https://github.com/NixOS/patchelf/).

## Usage

This may be outdated, it is recommended to use `-h` option to get the latest help message.

```bash
$ python patchdyn.py -h
usage: patchdyn.py [-h]
                   (--retrieve-interpreter | --update-interpreter INTERPRETER | --retrieve-needed | --update-needed OLD_NEEDED NEW_NEEDED | --create-needed NEEDED | --delete-needed NEEDED | --retrieve-soname | --update-soname SONAME | --retrieve-rpath | --update-rpath RPATH | --retrieve-runpath | --update-runpath RUNPATH | --retrieve-no-default-lib | --set-no-default-lib | --unset-no-default-lib)
                   [-o OUTPUT_FILENAME]
                   FILENAME

positional arguments:
  FILENAME              filename of the ELF file to be patched

optional arguments:
  -h, --help            show this help message and exit
  --retrieve-interpreter, --ri
  --update-interpreter INTERPRETER, --ui INTERPRETER
                        update dynamic linker/loader (in .interp section)
  --retrieve-needed, --rn
  --update-needed OLD_NEEDED NEW_NEEDED, --un OLD_NEEDED NEW_NEEDED
                        update shared object/library dependency (DT_NEEDED entry in .dynamic section)
  --create-needed NEEDED, --cn NEEDED
  --delete-needed NEEDED, --dn NEEDED
  --retrieve-soname, --rs
  --update-soname SONAME, --us SONAME
                        update shared object/library name (DT_SONAME entry in .dynamic section)
  --retrieve-rpath, --rrpath
  --update-rpath RPATH, --urpath RPATH
                        update rpath (DT_RPATH entry in .dynamic section)
  --retrieve-runpath, --rr
  --update-runpath RUNPATH, --ur RUNPATH
                        update runpath (DT_RUNPATH entry in .dynamic section)
  --retrieve-no-default-lib, --rndl
  --set-no-default-lib, --sndl
                        set DT_FLAGS_1 (DF_1_NODEFLIB) in .dynamic section
  --unset-no-default-lib, --usndl
  -o OUTPUT_FILENAME, --output OUTPUT_FILENAME
                        filename of the patched ELF file, <input filename>.patched by default
```
