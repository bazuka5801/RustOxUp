import os
import subprocess
import oxideprovider
import config


# Create/Update Rust Server
STEAMCMD_UPDATE_FILE = config.BASE_DIRECTORY+"steamcmd_update.txt"
CMD = [config.STEAMCMD_PATH, "+runscript", STEAMCMD_UPDATE_FILE]

with open(STEAMCMD_UPDATE_FILE, 'w') as f:
    f.write('login anonymous\n')
    f.write('force_install_dir '+config.SERVER_PATH+'\n')
    f.write('app_update 258550 validate\n')
    f.write('quit\n')
exit_code = subprocess.call(CMD, shell=True)
os.remove(STEAMCMD_UPDATE_FILE)

# Update Oxide
oxideprovider.download(config.SERVER_PATH)

oxideprovider.manual()

input("Updating process finished")


