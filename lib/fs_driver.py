"""
LVGL File System driver for MicroPython.
Bridges Python's open() / os calls to LVGL's virtual file system (lv_fs).
"""

import struct
import lvgl as lv


def _fs_open_cb(drv, path, mode):
    if mode == lv.FS_MODE.WR:
        p_mode = 'wb'
    elif mode == lv.FS_MODE.RD:
        p_mode = 'rb'
    elif mode == (lv.FS_MODE.WR | lv.FS_MODE.RD):
        p_mode = 'rb+'
    else:
        raise RuntimeError(f"fs_open_callback() - invalid mode {mode}")

    # LVGL often passes paths with a leading slash (e.g. '/DTGetaiGroteskDisplay-96.bin')
    # Try the raw path first, then try stripping the leading '/' if relative to project directory.
    try:
        f = open(path, p_mode)
        return {'file': f, 'path': path}
    except OSError:
        if path.startswith('/'):
            try:
                rel_path = path.lstrip('/')
                f = open(rel_path, p_mode)
                return {'file': f, 'path': rel_path}
            except OSError:
                pass
        raise RuntimeError(f"fs_open_callback({path}) exception: unable to open file")


def _fs_close_cb(drv, fs_file):
    try:
        fs_file.__cast__()['file'].close()
        return lv.FS_RES.OK
    except OSError as e:
        raise RuntimeError(f"fs_close_callback({fs_file.__cast__()['path']}) exception {e}")


def _fs_read_cb(drv, fs_file, buf, btr, br):
    try:
        tmp_data = fs_file.__cast__()['file'].read(btr)
        buf.__dereference__(btr)[0:len(tmp_data)] = tmp_data
        br.__dereference__(4)[0:4] = struct.pack('<L', len(tmp_data))
        return lv.FS_RES.OK
    except OSError as e:
        raise RuntimeError(f"fs_read_callback({fs_file.__cast__()['path']}) exception {e}")


def _fs_seek_cb(drv, fs_file, pos, whence):
    try:
        fs_file.__cast__()['file'].seek(pos, whence)
        return lv.FS_RES.OK
    except OSError as e:
        raise RuntimeError(f"fs_seek_callback({fs_file.__cast__()['path']}) exception {e}")


def _fs_tell_cb(drv, fs_file, pos):
    try:
        tpos = fs_file.__cast__()['file'].tell()
        pos.__dereference__(4)[0:4] = struct.pack('<L', tpos)
        return lv.FS_RES.OK
    except OSError as e:
        raise RuntimeError(f"fs_tell_callback({fs_file.__cast__()['path']}) exception {e}")


def _fs_write_cb(drv, fs_file, buf, btw, bw):
    try:
        wr = fs_file.__cast__()['file'].write(buf.__dereference__(btw)[0:btw])
        bw.__dereference__(4)[0:4] = struct.pack('<L', wr)
        return lv.FS_RES.OK
    except OSError as e:
        raise RuntimeError(f"fs_write_callback({fs_file.__cast__()['path']}) exception {e}")


def _fs_dir_open_cb(drv, path):
    try:
        import os
        if path != '/':
            path = path.rstrip('/')
        return {'iterator': os.ilistdir(path)}
    except Exception as e:
        print(f"_fs_dir_open_cb exception for path {path}: {e}")
        return None


def _fs_dir_read_cb(drv, lv_fs_dir_t, buf, btr):
    try:
        iterator = lv_fs_dir_t.__cast__()['iterator']
        nextfile = next(iterator)
        filename = nextfile[0]
        entry_type = nextfile[1]
        if entry_type == 16384:  # directory in micropython ilistdir
            filename = f"/{filename}"
        tmp_data_bytes = filename.encode() + b'\x00'
        buf.__dereference__(btr)[0:len(tmp_data_bytes)] = tmp_data_bytes
        return lv.FS_RES.OK
    except StopIteration:
        buf.__dereference__(btr)[0:1] = b'\x00'
        return lv.FS_RES.NOT_EX
    except Exception as e:
        print(f"_fs_dir_read_cb exception: {e}")
        return lv.FS_RES.UNKNOWN


def fs_register(fs_drv, letter, cache_size=500):
    fs_drv.init()
    fs_drv.letter = ord(letter)
    fs_drv.open_cb = _fs_open_cb
    fs_drv.read_cb = _fs_read_cb
    fs_drv.write_cb = _fs_write_cb
    fs_drv.seek_cb = _fs_seek_cb
    fs_drv.tell_cb = _fs_tell_cb
    fs_drv.close_cb = _fs_close_cb
    fs_drv.dir_open_cb = _fs_dir_open_cb
    fs_drv.dir_read_cb = _fs_dir_read_cb
    if cache_size >= 0:
        fs_drv.cache_size = cache_size
    fs_drv.register()
