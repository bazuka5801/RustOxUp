import os

# Oxide URL
OXIDE_URL = "http://github.com/OxideMod/Oxide/releases/download/latest/Oxide-Rust.zip"

# Server folder
SERVER = "onion-modded"

# SteamCMD path
STEAMCMD_PATH = "steamcmd/steamcmd.exe"

# Path folder
PATCH_PATH = "patch"

# Patch file
OPJ_FILE = "PatchData.opj"


BASE_DIRECTORY = os.getcwd()+"\\"

SERVER_PATH = os.path.join(BASE_DIRECTORY, SERVER)
MANAGED_PATH = os.path.join(SERVER_PATH, "RustDedicated_Data", "Managed")
ORIGINALS_PATH = os.path.join(PATCH_PATH, "Originals")

OPJ_PATH = os.path.join(PATCH_PATH, OPJ_FILE)


