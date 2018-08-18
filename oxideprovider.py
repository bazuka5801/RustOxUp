import config
import urllib.request
import zipfile
import ssl
import os
import json
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context

def download(destination):
	for filename in os.listdir(config.ORIGINALS_PATH):
		os.remove(os.path.join( config.ORIGINALS_PATH, filename))
	tempFile = config.BASE_DIRECTORY +'oxide.zip'

	print("Downloading OXIDE to "+tempFile)

	urllib.request.urlretrieve(config.OXIDE_URL, tempFile)
	with zipfile.ZipFile(tempFile, 'r') as zip_ref:
		zip_ref.extractall(destination)
	os.remove(tempFile)
	
def updateOriginals():
	f = open(config.OPJ_PATH)
	js = json.loads(f.read())
	f.close()
	
	for v in js['Manifests']:
		filename = v.get('AssemblyName')
		copy(os.path.join( config.MANAGED_PATH, filename.replace('.dll', '_Original.dll')), config.ORIGINALS_PATH)

def manual():
	patch(input("Silent Path(y/n): ") == "y")
		
def patch(silent):
	prePatchProcess()
	startPatcher(silent)
	postPatchProcess()
		
def startPatcher(silent):
	print(os.path.join(config.MANAGED_PATH, "OxidePatcher.exe"));
	if not silent:
		cmd = [os.path.join(config.MANAGED_PATH, "OxidePatcher.exe"), os.path.join(config.MANAGED_PATH, config.OPJ_FILE)]
		subprocess.call(cmd, cwd=config.MANAGED_PATH)
	else:		
		cmd = [os.path.join(config.MANAGED_PATH, "OxidePatcher.exe"), os.path.join(config.MANAGED_PATH, config.OPJ_FILE), "-c"]
		subprocess.call(cmd, cwd=config.MANAGED_PATH)

def prePatchProcess():
	for filename in os.listdir(config.ORIGINALS_PATH):
		copy(os.path.join( config.ORIGINALS_PATH, filename), config.MANAGED_PATH)
	
	copy(config.OPJ_PATH, config.MANAGED_PATH)
	replaceInFile(os.path.join(config.MANAGED_PATH,config.OPJ_FILE), "{TargetDirectory}", "D:\\\\OnionRust\\\\"+config.SERVER+"\\\\RustDedicated_Data\\\\Managed")
	copy(os.path.join(config.PATCH_PATH, "OxidePatcher.exe"), config.MANAGED_PATH)
	
def postPatchProcess():	
	os.remove(os.path.join(config.MANAGED_PATH, "OxidePatcher.exe"))
	
	opjPath = os.path.join(config.MANAGED_PATH, config.OPJ_FILE)
	replaceInFile(opjPath, config.MANAGED_PATH.replace("/", "\\").replace("\\", "\\\\"), "{TargetDirectory}")
	copy(opjPath, config.PATCH_PATH)
	os.remove(opjPath)
	os.remove(os.path.join(config.MANAGED_PATH, "log.txt"))
	
	updateOriginals();	
	
	for filename in os.listdir(config.MANAGED_PATH):
		if filename.endswith("_Original.dll"):
			f = os.path.join(config.MANAGED_PATH, filename)
			os.remove(f)

def replaceInFile(fs, rep1, rep2):
	with open(fs, "r") as fin:
		with open(fs+'.temp', "w") as fout:
			for line in fin:
				fout.write(line.replace(rep1, rep2))
	os.remove(fs)
	os.rename(fs+'.temp', fs)

def copy(source, destDir):
	os.system("copy \"%s\" \"%s\" /y" % (source, destDir))