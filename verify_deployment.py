#!/usr/bin/env python3
"""
🚀 INSTANT DEPLOYMENT VERIFICATION SCRIPT
Run this to verify everything is ready for deployment
"""

import os
import sys

print("=" * 60)
print("🔍 DEPLOYMENT READINESS CHECK")
print("=" * 60)

checks = {
    "✅ app.py": os.path.exists("app.py"),
    "✅ blockchain.py": os.path.exists("blockchain.py"),
    "✅ requirements.txt": os.path.exists("requirements.txt"),
    "✅ Procfile": os.path.exists("Procfile"),
    "✅ runtime.txt": os.path.exists("runtime.txt"),
    "✅ wsgi.py": os.path.exists("wsgi.py"),
    "✅ templates/index.html": os.path.exists("templates/index.html"),
    "✅ .gitignore": os.path.exists(".gitignore"),
}

all_passed = True
for check_name, result in checks.items():
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} - {check_name}")
    if not result:
        all_passed = False

print("\n" + "=" * 60)

# Check requirements.txt content
print("\n📦 CHECKING DEPENDENCIES...")
required_packages = ["Flask", "gunicorn", "web3", "Flask-CORS"]
try:
    with open("requirements.txt", "r") as f:
        content = f.read()
        for pkg in required_packages:
            if pkg.lower() in content.lower():
                print(f"  ✅ {pkg} found in requirements.txt")
            else:
                print(f"  ❌ {pkg} MISSING from requirements.txt")
                all_passed = False
except Exception as e:
    print(f"  ❌ Error reading requirements.txt: {e}")
    all_passed = False

print("\n" + "=" * 60)

# Check Procfile content
print("\n⚙️  CHECKING PROCFILE...")
try:
    with open("Procfile", "r") as f:
        content = f.read().strip()
        if "gunicorn app:app" in content:
            print(f"  ✅ Procfile correctly configured")
            print(f"     Content: {content}")
        else:
            print(f"  ❌ Procfile incorrect: {content}")
            all_passed = False
except Exception as e:
    print(f"  ❌ Error reading Procfile: {e}")
    all_passed = False

print("\n" + "=" * 60)

# Check runtime.txt
print("\n🐍 CHECKING RUNTIME...")
try:
    with open("runtime.txt", "r") as f:
        content = f.read().strip()
        if "python" in content.lower():
            print(f"  ✅ Runtime correctly configured")
            print(f"     Content: {content}")
        else:
            print(f"  ❌ Runtime may be incorrect: {content}")
            all_passed = False
except Exception as e:
    print(f"  ❌ Error reading runtime.txt: {e}")
    all_passed = False

print("\n" + "=" * 60)

if all_passed:
    print("\n✅ ALL CHECKS PASSED!")
    print("\n🚀 DEPLOYMENT READY!")
    print("\nNext steps:")
    print("1. git init")
    print("2. git add .")
    print("3. git commit -m 'Blockchain Academic Record System'")
    print("4. Create GitHub repo and push")
    print("5. Deploy on Render.com or Railway.app")
    print("\n✨ Your system will be live in 5-10 minutes!")
    sys.exit(0)
else:
    print("\n❌ SOME CHECKS FAILED!")
    print("\nPlease fix the issues above before deploying.")
    sys.exit(1)
