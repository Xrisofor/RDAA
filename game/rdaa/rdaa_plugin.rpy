init offset = -5

init python:
    import os, wget, threading, ssl, re, requests, zipfile, os.path

    def searchpath():
        path = (config.gamedir if renpy.windows else os.environ["ANDROID_PUBLIC"] + "/game")
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    class SharedCloudGetFile(threading.Thread):
        """This class is responsible for getting the final URL of the file stored in
        some cloud that displays the final URL on the file upload page"""

        def __init__(self, shared_url):
            super(SharedCloudGetFile, self).__init__()
            self.daemon = True
            self.shared_url = shared_url
            self.fetch_finish = False
            self.url_end = None
            self.fetch_exception = None

        def status(self):
            """Returns bool regardless of whether the recovery is completed or not"""
            return self.fetch_finish

        def end_url(self):
            """Returns the final download URL"""
            return self.url_end

        def runtime_exception(self):
            """Returns True regardless of whether there was an exception or not during recovery"""
            if isinstance(self.fetch_exception, Exception):
                return True
            return False

        def run(self):
            """Cleans up the shared URL"""

            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
            url_prefixes = ("https://download", "https://cdn-")

            try:
                ssl._create_default_https_context = ssl._create_unverified_context

                r = requests.get(self.shared_url, headers = headers)
                url = re.findall('"((http|ftp)s?://.*?)"', r.text)
                
                for i in url:
                    if i[0].startswith(url_prefixes):
                        self.url_end = i[0]
                        break
                    else:
                        pass

            except Exception as fetcherr:
                self.fetch_exception = fetcherr
                print("[Error - SharedCloudGetFile]: %s" % fetcherr)

            finally:
                self.fetch_finish = True
                renpy.restart_interaction()

    class DownloadHandler(threading.Thread):
        """This class is responsible for executing and tracking the requested download"""

        def __init__(self, url, savepath = None, auto_extract = False):
            """Constructor of the class. Gets the following arguments:

            url (necessarily):
                The URL of the file you want to download. It should be a physical file,
                not the planned site

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

                renpy.restart_interaction()
