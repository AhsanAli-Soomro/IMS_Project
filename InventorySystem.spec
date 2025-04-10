# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=[('ims.db', '.'), ('logo', 'logo'), ('images', 'images')],
    hiddenimports=['employee', 'supplier', 'category', 'product', 'customer', 'settings', 'sales', 'logs', 'reports', 'selling_history', 'SupplierProductPurchaseHistory', 'utils', 'dashboard', 'login'],
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
    name='InventorySystem',
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
    icon=['logo/icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InventorySystem',
)
app = BUNDLE(
    coll,
    name='InventorySystem.app',
    icon='logo/icon.png',
    bundle_identifier=None,
)
