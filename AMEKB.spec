# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main0.py'],
    pathex=[],
    binaries=[],
    datas=[('AMEKB\\forms\\*.py', 'forms'), ('AMEKB\\helper\\*.py', 'helper'), ('catia_integration\\*.py', 'catia_integration')],
    hiddenimports=['helper.sql_helper', 'pyodbc', 'win32com.client', 'PIL.Image', 'PIL.ImageTk', 'loguru', 'catia_integration.catia_operator_0_很久之前'],
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
    a.binaries,
    a.datas,
    [],
    name='AMEKB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)
