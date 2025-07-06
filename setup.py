#!/usr/bin/env python3
"""
setup.py

Setup script for MCP Database stack. Clones Supabase repository and prepares environment.
"""

import os
import subprocess
import shutil
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_source_path = ".env"
    
    if not os.path.exists(env_source_path):
        print("Warning: .env file not found. Please copy .env.example to .env and configure it first.")
        return
    
    print("Copying .env to supabase/docker/.env...")
    shutil.copyfile(env_source_path, env_path)

def check_env_file():
    """Check if .env file exists, if not prompt user to create it."""
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and configure your secrets:")
        print("  cp .env.example .env")
        print("  # Edit .env with your secure passwords and keys")
        sys.exit(1)
    else:
        print("✅ .env file found")

def main():
    print("Setting up MCP Database stack...")
    
    check_env_file()
    clone_supabase_repo()
    prepare_supabase_env()
    
    print("\n✅ Setup complete!")
    print("You can now start the services with:")
    print("  docker compose up -d")
    print("\nService URLs:")
    print("  - Supabase Studio: http://localhost:8000")
    print("  - Neo4j Browser: http://localhost:7474")

if __name__ == "__main__":
    main()