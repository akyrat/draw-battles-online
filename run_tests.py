#!/usr/bin/env python3
"""
Test Runner for Draw Battles Online
Easy way to run tests with proper configuration
"""

import subprocess
import sys
import os


def main():
    """Run the test suite"""
    print("🧪 Running Draw Battles Online Test Suite...")
    print("=" * 50)
    
    # Ensure we're in the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run pytest with verbose output and coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "-x",  # Stop on first failure
    ]
    
    # Add coverage if pytest-cov is available
    try:
        import pytest_cov
        cmd.extend([
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])
        print("📊 Coverage reporting enabled")
    except ImportError:
        print("📊 Coverage reporting not available (install pytest-cov)")
    
    print(f"🚀 Running: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run tests
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        if os.path.exists("htmlcov/index.html"):
            print("📊 Coverage report: htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 