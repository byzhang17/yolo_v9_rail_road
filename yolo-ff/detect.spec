# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['detect.py'],
    pathex=['D:\\anaconda\\envs\\pytorch\\Lib\\site-packages', 'D:\\anaconda\\envs\\pytorch\\Lib\\site-packages\\torch\\lib'],
    binaries=[],
    datas=[],
    hiddenimports=['torchvision'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='detect',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='detect',
)
