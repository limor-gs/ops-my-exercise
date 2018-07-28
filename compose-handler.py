import os
import shutil
import urllib
import tarfile
from distutils.spawn import find_executable


WORKDIR = os.path.expanduser("~/ops")
IMAGES_DIR = "/Users/mac/exercise/public/images"
DB_DIR = "/Users/mac/exercise/public/db"
ORIG_PWD = os.getcwd()


def validate():
    valid = find_executable("docker") and find_executable("docker-compose")
    if not valid:
        raise Exception("Please install docker and docker-compose then rerun the script")


def init_env():
    for dir in [DB_DIR, IMAGES_DIR, WORKDIR]:
        if not os.path.exists(dir):
            os.makedirs(dir)


def download_images():
    url = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
    file_tmp = urllib.urlretrieve(url, filename=None)[0]
    tar = tarfile.open(file_tmp)
    tar.extractall(IMAGES_DIR)
    tar.close()


def download_app():
    os.chdir(WORKDIR)
    if not os.path.exists("ops-exercise"):
        os.system("git clone https://github.com/bigpandaio/ops-exercise")
    shutil.copy2('{}/docker-compose.yml'.format(ORIG_PWD), 'ops-exercise/')


def run_app_db():
    os.chdir("ops-exercise")
    os.system("docker-compose up")


if __name__ == '__main__':
    try:
        validate()
        init_env()
        download_images()
        download_app()
        run_app_db()
    except Exception as error:
        print('error: ' + str(error))
