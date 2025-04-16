import sys
print('Python path:')
print(sys.path)
print('\nChecking imports:')
try:
    import passlib
    print('passlib ✓')
    from passlib.context import CryptContext
    print('CryptContext ✓')
    import bcrypt
    print('bcrypt ✓')
except ImportError as e:
    print(f'Import error: {e}')
