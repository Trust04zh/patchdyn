import argparse
import sys

import lief.ELF as ELF

class PatchDynException(Exception):
    pass

def retrieve_interpreter(binary: ELF.Binary):
    if binary.has_interpreter:
        print(binary.interpreter)

def update_interpreter(binary: ELF.Binary, interpreter: str):
    binary.interpreter = interpreter

def retrieve_needed(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryLibrary):
            print(dyn.name)

def update_needed(binary: ELF.Binary, old_needed: str, new_needed: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryLibrary):
            if dyn.name == old_needed:
                dyn.name = new_needed
                return
    raise PatchDynException('No such needed')

def create_needed(binary: ELF.Binary, needed: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryLibrary):
            if dyn.name == needed:
                raise PatchDynException('Needed already exists')
    needed_entry = ELF.DynamicEntryLibrary(needed)
    binary.add(needed_entry)

def delete_needed(binary: ELF.Binary, needed: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryLibrary):
            if dyn.name == needed:
                binary.remove(dyn)
                return
    raise PatchDynException('No such needed')

def retrieve_soname(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicSharedObject):
            print(dyn.name)
            return

def update_soname(binary: ELF.Binary, soname: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicSharedObject):
            if soname == '':  # delete soname
                binary.remove(dyn)
            else:  # update soname
                dyn.name = soname
            return
    if soname != '':  # create soname
        soname_entry = ELF.DynamicSharedObject(soname)
        binary.add(soname_entry)
        return
    raise PatchDynException('Tried to delete non-existent soname')

def retrieve_rpath(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryRpath):
            print(dyn.name)
            return

def update_rpath(binary: ELF.Binary, rpath: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryRpath):
            if rpath == '':  # delete rpath
                binary.remove(dyn)
            else:  # update rpath
                dyn.name = rpath
            return
    if rpath != '':  # create rpath
        rpath_entry = ELF.DynamicEntryRpath(rpath)
        binary.add(rpath_entry)
        return
    raise PatchDynException('Tried to delete non-existent rpath')

def retrieve_runpath(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryRunPath):
            print(dyn.name)
            return

def update_runpath(binary: ELF.Binary, runpath: str):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryRunPath):
            if runpath == '':  # delete runpath
                binary.remove(dyn)
            else:  # update runpath
                dyn.name = runpath
            return
    if runpath != '':  # create runpath
        runpath_entry = ELF.DynamicEntryRunPath(runpath)
        binary.add(runpath_entry)
        return
    raise PatchDynException('Tried to delete non-existent runpath')

def retrieve_no_default_lib(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryFlags) \
                and ELF.DYNAMIC_FLAGS_1.NODEFLIB in dyn:
            print('Found')
            return
    print('Not found')

def set_no_default_lib(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryFlags):
            dyn.add(ELF.DYNAMIC_FLAGS_1.NODEFLIB)
            return

def unset_no_default_lib(binary: ELF.Binary):
    dyns_iter = binary.dynamic_entries
    for dyn in dyns_iter:
        if isinstance(dyn, ELF.DynamicEntryFlags):
            dyn.remove(ELF.DYNAMIC_FLAGS_1.NODEFLIB)
            return

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--retrieve-interpreter', '--ri', action='store_true', dest='retrieve_interpreter', help='todo')
    action.add_argument('--update-interpreter', '--ui', metavar='INTERPRETER', type=str, nargs=1, dest='update_interpreter', help='todo')
    action.add_argument('--retrieve-needed', '--rn', action='store_true', dest='retrieve_needed', help='todo')
    action.add_argument('--update-needed', '--un', metavar=('OLD_NEEDED', 'NEW_NEEDED'), type=str, nargs=2, dest='update_needed', help='todo')
    action.add_argument('--create-needed', '--cn', metavar='NEEDED', type=str, nargs=1, dest='create_needed', help='todo')
    action.add_argument('--delete-needed', '--dn', metavar='NEEDED', type=str, nargs=1, dest='delete_needed', help='todo')
    action.add_argument('--retrieve-soname', '--rs', action='store_true', dest='retrieve_soname', help='todo')
    action.add_argument('--update-soname', '--us', metavar='SONAME', type=str, nargs=1, dest='update_soname', help='todo')
    action.add_argument('--retrieve-rpath', '--rrpath', action='store_true', dest='retrieve_rpath', help='todo')
    action.add_argument('--update-rpath', '--urpath', metavar='RPATH', type=str, nargs=1, dest='update_rpath', help='todo')
    action.add_argument('--retrieve-runpath', '--rr', action='store_true', dest='retrieve_runpath', help='todo')
    action.add_argument('--update-runpath', '--ur', metavar='RUNPATH', type=str, nargs=1, dest='update_runpath', help='todo')
    action.add_argument('--retrieve-no-default-lib', '--rndl', action='store_true', dest='retrieve_no_default_lib', help='todo')
    action.add_argument('--set-no-default-lib', '--sndl', action='store_true', dest='set_no_default_lib', help='todo')
    action.add_argument('--unset-no-default-lib', '--usndl', action='store_true', dest='unset_no_default_lib', help='todo')
    parser.add_argument('input', metavar='FILENAME', type=str, help='todo')
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILENAME', type=str, dest='output', help='todo')
    args = parser.parse_args()

    binary: ELF.Binary = ELF.parse(args.input)

    updated = False

    try:
        if args.retrieve_interpreter:
            retrieve_interpreter(binary)
        elif args.update_interpreter:
            update_interpreter(binary, args.update_interpreter[0])
            updated = True
        elif args.retrieve_needed:
            retrieve_needed(binary)
        elif args.update_needed:
            update_needed(binary, args.update_needed[0], args.update_needed[1])
            updated = True
        elif args.create_needed:
            create_needed(binary, args.create_needed[0])
            updated = True
        elif args.delete_needed:
            delete_needed(binary, args.delete_needed[0])
            updated = True
        elif args.retrieve_soname:
            retrieve_soname(binary)
        elif args.update_soname:
            update_soname(binary, args.update_soname[0])
            updated = True
        elif args.retrieve_rpath:
            retrieve_rpath(binary)
        elif args.update_rpath:
            update_rpath(binary, args.update_rpath[0])
            updated = True
        elif args.retrieve_runpath:
            retrieve_runpath(binary)
        elif args.update_runpath:
            update_runpath(binary, args.update_runpath[0])
            updated = True
        elif args.retrieve_no_default_lib:
            retrieve_no_default_lib(binary)
        elif args.set_no_default_lib:
            set_no_default_lib(binary)
            updated = True
        elif args.unset_no_default_lib:
            unset_no_default_lib(binary)
            updated = True
    except PatchDynException as e:
        print(e)
        sys.exit(1)

    # updated = False  # FIXME: debug
    if updated:
        if args.output is None:
            output_filename = args.input
        else:
            output_filename = args.output
        builder = ELF.Builder(binary)
        builder.build()
        builder.write(output_filename)
        # binary.write(output_filename)
