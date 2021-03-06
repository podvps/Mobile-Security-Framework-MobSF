"""
Django settings for MobSF project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import imp
from MobSF import utils

from install.windows.setup import windows_config_local

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#       MOBSF FRAMEWORK CONFIGURATIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#==============================================

MOBSF_VER = "v0.9.5.4 Beta"
BANNER = """
 __  __       _    ____  _____        ___   ___   ____  
|  \/  | ___ | |__/ ___||  ___|_   __/ _ \ / _ \ | ___| 
| |\/| |/ _ \| '_ \___ \| |_  \ \ / / | | | (_) ||___ \ 
| |  | | (_) | |_) |__) |  _|  \ V /| |_| |\__, | ___) |
|_|  |_|\___/|_.__/____/|_|     \_/  \___(_) /_(_)____/ 
                                                        
"""
#==============================================

#==========MobSF Home Directory=================
USE_HOME = False

# True : All Uploads/Downloads will be stored in user's home directory
# False : All Uploads/Downloads will be stored in MobSF root directory
# If you need multiple users to share the scan results set this to False
#===============================================

MobSF_HOME = utils.getMobSFHome(USE_HOME)
# Logs Directory
LOG_DIR = os.path.join(MobSF_HOME, 'logs/')
# Download Directory
DWD_DIR = os.path.join(MobSF_HOME, 'downloads/')
# Screenshot Directory
SCREEN_DIR = os.path.join(MobSF_HOME, 'downloads/screen/')
# Upload Directory
UPLD_DIR = os.path.join(MobSF_HOME, 'uploads/')
# Database Directory
DB_DIR = os.path.join(MobSF_HOME, 'db.sqlite3')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR,
    }
}
# Postgres DB - Install psycopg2
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mobsf',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
'''
#===============================================

#==========LOAD CONFIG FROM MobSF HOME==========
try:
    # Update Config from MobSF Home Directory
    if USE_HOME:
        USER_CONFIG = os.path.join(MobSF_HOME, 'config.py')
        sett = imp.load_source('user_settings', USER_CONFIG)
        locals().update(
            {k: v for k, v in sett.__dict__.items() if not k.startswith("__")})
        CONFIG_HOME = True
    else:
        CONFIG_HOME = False
except:
    utils.PrintException("[ERROR] Parsing Config")
    CONFIG_HOME = False
#===============================================

#=============ALLOWED EXTENSIONS================
ALLOWED_EXTENSIONS = {
    ".txt": "text/plain",
    ".png": "image/png",
    ".zip": "application/zip",
    ".tar": "application/x-tar"
}
#===============================================

#=============ALLOWED MIMETYPES=================

APK_MIME = [
    'application/octet-stream',
    'application/vnd.android.package-archive',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
IPA_MIME = [
    'application/iphone',
    'application/octet-stream',
    'application/x-itunes-ipa',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
ZIP_MIME = [
    'application/zip',
    'application/octet-stream',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
APPX_MIME = [
    'application/octet-stream',
    'application/vns.ms-appx',
    'application/x-zip-compressed'
]

#===============================================

#=====MOBSF SECRET GENERATION AND MIGRATION=====
# Based on https://gist.github.com/ndarville/3452907#file-secret-key-gen-py
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(MobSF_HOME, "secret")
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            SECRET_KEY = utils.genRandom()
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % SECRET_FILE)
        # Run Once
        # Windows Setup
        windows_config_local(MobSF_HOME)
        utils.make_migrations(BASE_DIR)
        utils.migrate(BASE_DIR)
        utils.kali_fix(BASE_DIR)

#=============================================

#============DJANGO SETTINGS =================

# SECURITY WARNING: don't run with debug turned on in production!
# ^ This is fine Do not turn it off until MobSF moves from Beta to Stable

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'testserver', '*']
# Application definition
INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'StaticAnalyzer',
    'DynamicAnalyzer',
    'MobSF',
    'APITester',
    'MalwareAnalyzer',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
ROOT_URLCONF = 'MobSF.urls'
WSGI_APPLICATION = 'MobSF.wsgi.application'
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS':
            [
                os.path.join(BASE_DIR, 'templates')
            ],
        'OPTIONS':
            {
                'debug': True,
            }
    },
]
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'

#===================
# USER CONFIGURATION
#===================

if CONFIG_HOME:
    print "[INFO] Loading User config from: " + USER_CONFIG
else:
    '''
    IMPORTANT
    If 'USE_HOME' is set to True, then below user configuration settings are not considered.
    The user configuration will be loaded from config.py in MobSF Home directory.
    '''
    #^CONFIG-START^: Do not edit this line
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #          MOBSF USER CONFIGURATIONS
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #-------------------------
    # STATIC ANALYZER SETTINGS
    #-------------------------

    #==========ANDROID SKIP CLASSES==========================
    # Common third party classes that will be skipped during static analysis
    SKIP_CLASSES = [
        r'android[\\\/]{1}support[\\\/]{1}', r'com[\\\/]{1}google[\\\/]{1}', r'android[\\\/]{1}content[\\\/]{1}',
        r'com[\\\/]{1}android[\\\/]{1}', r'com[\\\/]{1}facebook[\\\/]{1}', r'com[\\\/]{1}twitter[\\\/]{1}',
        r'twitter4j[\\\/]{1}', r'org[\\\/]{1}apache[\\\/]{1}', r'com[\\\/]{1}squareup[\\\/]{1}okhttp[\\\/]{1}',
        r'oauth[\\\/]{1}signpost[\\\/]{1}', r'org[\\\/]{1}chromium[\\\/]{1}'
    ]

    #==========DECOMPILER SETTINGS=================

    DECOMPILER = "cfr"

    # Three Decompilers are available
    # 1. jd-core
    # 2. cfr
    # 3. procyon

    #==============================================

    #==========Dex to Jar Converter================
    JAR_CONVERTER = "d2j"

    # Two Dex to Jar converters are available
    # 1. d2j
    # 2. enjarify

    '''
    enjarify requires python3. Install Python 3 and add the path to environment variable
    PATH or provide the Python 3 path to "PYTHON3_PATH" variable in settings.py
    ex: PYTHON3_PATH = "C:/Users/Ajin/AppData/Local/Programs/Python/Python35-32/"
    '''
    PYTHON3_PATH = ""
    #==============================================

    #========DISABLED COMPONENTS===================

    #----------VirusTotal--------------------------
    VT_ENABLED = False
    VT_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    VT_UPLOAD = False
    # Before setting VT_ENABLED to True,
    # Make sure VT_API_KEY is set to your VirusTotal API key
    # register at: https://www.virustotal.com/#/join-us
    # You can get your API KEY from https://www.virustotal.com/en/user/<username>/apikey/
    # VT has a premium features but the free account is just enough for personal use
    # BE AWARE - if you enable VT, in case the file wasn't already uploaded to VirusTotal,
    # It will be uploaded if you set VT_UPLOAD to True!
    #==============================================

    #----------APKiD-------------------------------
    APKID_ENABLED = False
    # Before setting APKID_ENABLED to True,
    # Install rednaga fork of Yara Python
    # git clone https://github.com/rednaga/yara-python
    # cd yara-python
    # python setup.py install
    #==============================================

    #======WINDOWS STATIC ANALYSIS SETTINGS ===========

    # Private key
    WINDOWS_VM_SECRET = 'MobSF/windows_vm_priv_key.asc'
    # IP and Port of the MobSF Windows VM
    # eg: WINDOWS_VM_IP = '127.0.0.1'
    WINDOWS_VM_IP = None
    WINDOWS_VM_PORT = '8000'
    #==================================================

    #==============3rd Party Tools=================
    '''
    If you want to use a different version of 3rd party tools used by MobSF.
    You can do that by specifying the path here. If specified, MobSF will run
    the tool from this location.
    '''

    # Android 3P Tools
    DEX2JAR_BINARY = ""
    BACKSMALI_BINARY = ""
    AXMLPRINTER_BINARY = ""
    CFR_DECOMPILER_BINARY = ""
    JD_CORE_DECOMPILER_BINARY = ""
    PROCYON_DECOMPILER_BINARY = ""
    AAPT_BINARY = ""
    ADB_BINARY = ""
    ENJARIFY_DIRECTORY = ""

    # iOS 3P Tools
    OTOOL_BINARY = ""
    CLASSDUMPZ_BINARY = ""

    # COMMON
    JAVA_DIRECTORY = ""
    VBOXMANAGE_BINARY = ""

    '''
    Examples:
    JAVA_DIRECTORY = "C:/Program Files/Java/jdk1.7.0_17/bin/"
    JAVA_DIRECTORY = "/usr/bin/"
    DEX2JAR_BINARY = "/Users/ajin/dex2jar/d2j-dex2jar.sh"
    ENJARIFY_DIRECTORY = "D:/enjarify/"
    VBOXMANAGE_BINARY = "/usr/bin/VBoxManage"
    CFR_DECOMPILER_BINARY = "/home/ajin/tools/cfr.jar"
    '''
    #===============================================

    #-------------------------
    # DYNAMIC ANALYZER SETTINGS
    #-------------------------

    #========ANDROID DYNAMIC ANALYSIS SETTINGS================================

    ANDROID_DYNAMIC_ANALYZER = "MobSF_VM"

    # You can choose any of the below
    # 1. MobSF_VM
    # 2. MobSF_AVD
    # 3. MobSF_REAL_DEVICE

    '''
    MobSF_VM - x86 Android 4.4.2 running on VirtualBox (Fast, not all Apps work)
    MobSF_AVD - ARM Android 4.1.2 running on Android Emulator (Slow, Most Apps work)
    MobSF_REAL_DEVICE - Rooted Android 4.03 - 4.4 Device (Very Fast, All Apps work)
    '''

    #=========================================================================

    #=======ANDROID REAL DEVICE SETTINGS===========
    DEVICE_IP = '192.168.1.18'
    DEVICE_ADB_PORT = 5555
    DEVICE_TIMEOUT = 300
    #==============================================

    #===========ANDROID EMULATOR SETTINGS ===========
    # generated by mobsfy_AVD.py, do not edit the
    # below AVD settings yourself.
    AVD_EMULATOR = "avd_emulator"
    AVD_PATH = "avd_path"
    AVD_REFERENCE_NAME = r'Nexus5API16'
    AVD_DUP_NAME = r'Nexus5API16_1'
    AVD_ADB_PORT = 5554
    #================================================

    #====ANDROID MOBSF VIRTUALBOX VM SETTINGS =====
    # VM UUID
    UUID = '408e1874-759f-4417-9453-53ef21dc2ade'
    # Snapshot UUID
    SUUID = '5c9deb28-def6-49c0-9233-b5e03edd85c6'
    # IP of the MobSF VM
    VM_IP = '192.168.56.101'
    VM_ADB_PORT = 5555
    VM_TIMEOUT = 100
    #==============================================

    #--------------------------
    # MobSF MITM PROXY SETTINGS
    #--------------------------

    #================HOST/PROXY SETTINGS ===============
    PROXY_IP = '192.168.56.1'  # Host/Server/Proxy IP
    PORT = 1337  # Proxy Port
    ROOT_CA = '0025aabb.0'
    SCREEN_IP = PROXY_IP  # ScreenCast IP
    SCREEN_PORT = 9339  # ScreenCast Port(Do not Change)
    #===================================================

    #========UPSTREAM PROXY SETTINGS ==============
    # If you are behind a Proxy
    UPSTREAM_PROXY_IP = None
    UPSTREAM_PROXY_PORT = None
    UPSTREAM_PROXY_USERNAME = None
    UPSTREAM_PROXY_PASSWORD = None
    #==============================================

    #------------------------
    # WEB API FUZZER SETTINGS
    #------------------------

    #==============RESPONSE VALIDATION==============
    XXE_VALIDATE_STRING = "m0bsfxx3"
    #===============================================

    #=========Path Traversal - API Testing==========
    CHECK_FILE = "/etc/passwd"
    RESPONSE_REGEX = "root:|nobody:"
    #===============================================

    #=========Rate Limit Check - API Testing========
    RATE_REGISTER = 20
    RATE_LOGIN = 20
    #===============================================

    #===============MobSF Cloud Settings============
    CLOUD_SERVER = 'http://opensecurity.in:8080'
    '''
    This server validates SSRF and XXE during Web API Testing
    See the source code of the cloud server from APITester/cloud/cloud_server.py
    You can also host the cloud server. Host it on a public IP and point CLOUD_SERVER to that IP.
    '''

    #^CONFIG-END^: Do not edit this line

# The below code should be loaded last.
#============JAVA SETTINGS======================
JAVA_PATH = utils.FindJava(False)
#===============================================

#================VirtualBox Settings============
VBOX = utils.FindVbox(False)
#===============================================
