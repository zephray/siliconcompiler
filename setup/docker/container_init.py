# Initialization script for siliconcompiler docker containers.
# This installs some open-source EDA tools using scripts from the sc repository.

import subprocess
import sys

installs = ['surelog', 'klayout', 'magic', 'openroad', 'sv2v', 'netgen']
for i in installs:
    print(f'Installing {i}...')
    script_path = 'setup/install-'+i+'.sh'
    # Commands run as root from the Docker setup script; no 'sudo' required.
    subprocess.run('sed -i "s/sudo //g" ' + script_path, shell=True)
    proc = subprocess.run(script_path, shell=True)
    if proc.returncode > 0:
        sys.exit(proc.returncode)
