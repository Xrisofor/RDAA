init offset = -5

define client_version = "0.0.0.0"
define server_version = "0.0.0.0"
define version_f = "0.0.0.0"

init python:
    import os, wget, threading, ssl, re, requests, zipfile, os.path, urllib3, json

    def searchpath():
        path = None
        if renpy.windows:
            path = config.gamedir
        elif renpy.linux:
            path = config.gamedir
        else:
            path = os.environ["ANDROID_PUBLIC"] + "/game"

        if not os.path.exists(path):
            os.mkdir(path)
        return path

    version_f = searchpath() + "/version.txt"

    class UpdateConfig(threading.Thread):
        def __init__(self, url):
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = response.data.decode('utf-8')
            data = json.loads(data)
            server_version = data['version']

            self.server_version = server_version
            self.client_version = client_version
            self.version_f = version_f

        def checkVersion(self):
            if os.path.isfile(self.version_f):
                version_file = open(self.version_f, 'r')
                self.client_version = version_file.read()
                version_file.close()

            print("Server: " + self.server_version)
            print("Client: " + self.client_version)

            if self.client_version != self.server_version:
                return False
            else:
                return True

    class DownloadHandler(threading.Thread):
        """This class is responsible for executing and tracking the requested download"""

        def __init__(self, url, uc, savepath = None, auto_extract = False):
            """Constructor of the class. Gets the following arguments:

            url (necessarily):
                The URL of the file you want to download. It should be a physical file,
                not the planned site

            uc (necessarily):
                The UpdateConfig class through which some information is checked and obtained

            savepath:
                If it is not None, it is a string with the physical path to the device on
                which it will be saved archive
                
            auto_extract:
                Automatic unpacking of the archive after downloading"""

            super(DownloadHandler, self).__init__()
            self.daemon = True

            self.endpoint_url = url
            self.dl_path = savepath

            self.dl_current = 0.0
            self.dl_total = 0.0
            self.dl_percent = 0.0

            self.dl_status = False
            self.exception_output = None

            self.server_version = server_version
            self.version_f = version_f

        @property
        def gauge(self):
            """Returns the loaded percentage that will be displayed by the progress bar"""
            return (self.dl_percent or 0.0)

        @property
        def sizelist(self):
            """Returns a list with the downloaded MB and the total number of MB of the downloaded file"""
            return [self.dl_current, self.dl_total]

        def status(self):
            """Returns True if the download is completed, otherwise returns False"""
            return self.dl_status

        def runtime_exception(self):
            """Returns True if an error occurs during loading"""

            if isinstance(self.exception_output, Exception):
                return True
            return False

        def progress_handler(self, current, total, *args, **kwargs):
            """Calculates the download progress"""
            current, total = map(float, (current, total))
            if total > .0:
                self.dl_percent = (current / total)
                self.dl_current = round((current / 1048576), 2)
                self.dl_total = round((total / 1048576), 2)
                renpy.restart_interaction()

        def run(self):
            """Starts the download in an unverified SSL context to avoid download errors
            for conflicts with security certificates"""

            ssl._create_default_https_context = ssl._create_unverified_context

            try:
                wget.download(self.endpoint_url, self.dl_path, bar = self.progress_handler)
                    
            except Exception as ex:
                self.exception_output = ex
                self.dl_percent = 0.0
                print("[Error - DownloadHandler]: %s" % ex)
            finally:
                self.dl_status = True

                if os.path.isfile(self.dl_path):
                    with zipfile.ZipFile(self.dl_path, 'r') as zip_file:
                        zip_file.extractall(searchpath() + "/")
                        zip_file.close()
                    os.remove(self.dl_path)

                version_file = open(uc.version_f, "w+")
                version_file.write(uc.server_version)
                version_file.close()

                renpy.restart_interaction()