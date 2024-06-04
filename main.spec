# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app\\main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('app/resources/slots/*.png', 'app/resources/slots'),
        ('app/resources/skills.json', 'app/resources')
    ],
    hiddenimports=[
        'scipy.special._ufuncs',
        'scipy.special._ufuncs_cxx',
        'scipy.special._ellip_harm_2',
        'scipy.special._ellip_harm',
        'scipy.special._comb',
        'scipy.special._ufuncs_cxx',
        'scipy.special._logit',
        'scipy.special._sph_harm',
        'scipy.special._cdflib',
        'scipy.special._xlogy',
        'pytesseract',
        'pyautogui',
        'PIL',
        'scikit-image',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)
