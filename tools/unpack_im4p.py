#!/usr/bin/env python3
"""Extract LZFSE-compressed IM4P payloads (DeviceTree.d22ap.im4p and kernelcache.release.iphone10b)."""
import os
import liblzfse

def extract_im4p(im4p_path, out_path):
    import struct
    data = open(im4p_path, 'rb').read()
    idx = data.find(b'bvx2')
    if idx < 0:
        idx = data.find(b'bvxn')
    assert idx >= 0, f'No LZFSE magic found in {im4p_path}'
    raw = liblzfse.decompress(data[idx:])
    if raw[:4] == b'\xca\xfe\xba\xbe':
        _, narch = struct.unpack_from('>II', raw, 0)
        _, _, off, size, _ = struct.unpack_from('>IIIII', raw, 8)
        print(f'[*] Unwrapping FAT Mach-O ({narch} arch): offset={off:#x} size={size:#x}')
        raw = raw[off:off + size]
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    open(out_path, 'wb').write(raw)
    print(f'[+] Extracted {out_path} ({len(raw):,} bytes, magic={raw[:4].hex()})')

if __name__ == '__main__':
    extract_im4p('research/ipsw-x/dt/Firmware/all_flash/DeviceTree.d22ap.im4p',
                 'research/ipsw-x/d22ap.adt')
    extract_im4p('research/ipsw-x/dt/kernelcache.release.iphone10b',
                 'research/ipsw-x/dt/kernel.release.iphone10b.macho')
