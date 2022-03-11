from modules.src.zipfile import ZipFile
import sqlite3
from hashlib import md5, sha256, pbkdf2_hmac
import cryptocode
from subprocess import call
from sys import platform
import os
import shutil
import base64

class encDir():
    def __init__(self):
        super(encDir, self).__init__()
        self.dirPath = 'modules/DATA/main.zip'
        self.tmpPath = 'modules/DATA/files/tmp/'
        if not os.path.isfile(self.dirPath):
            zip = ZipFile(self.dirPath, 'w')
            zip.close()
    def getData(self, arcname):
        zip = ZipFile(self.dirPath, 'r')
        data = zip.open(arcname, 'r').read()
        zip.close()
        return data
    def add(self, data, arcname):
        zip = ZipFile(self.dirPath, 'a')
        if arcname not in zip.namelist():
            zip.writestr(arcname, data)
        else:
            pass
        zip.close()
    def ls(self):
        zip = ZipFile(self.dirPath, 'r')
        files = zip.namelist()
        print(files)
        zip.close()
        return files
    def rm(self, arcname):
        zip = ZipFile(self.dirPath, 'a')
        zip.remove(arcname)
        zip.close()
    def clear(self):
        zip = ZipFile(self.dirPath, 'w')
        zip.close()
        try:
            shutil.rmtree(self.tmpPath)
            os.mkdir(self.tmpPath)
        except Exception as e:
            print('tmp does not exist')

class fileDB():
    def __init__(self):
        super(fileDB, self).__init__()
        # Configs
        self.dbPath = 'modules/DATA/main.db'
        self.tmpPath = 'modules/DATA/files/tmp/'
        # Create database if missing
        if not os.path.isfile(self.dbPath):
            conn = sqlite3.connect(self.dbPath)
            cur = conn.cursor()
            with open('config.sql') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
    def dbConnect(self):
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        return conn, cur
    def add(self, filename, arcname, type, directory):
        conn, cur = self.dbConnect()
        existing = cur.execute('SELECT * FROM files WHERE filename = ? AND arcname = ? AND directory = ?', (filename, arcname, directory)).fetchone()
        if existing != None:
            pass
        else:
            cur.execute('INSERT INTO files (filename, arcname, type, directory) VALUES (?,?,?,?)', (filename, arcname, type, directory))
        conn.commit()
        conn.close()
    def rm(self, filename, directory, type):
        conn, cur = self.dbConnect()
        # Delete entries
        if type == 'file':
            arcname = str(cur.execute('SELECT arcname FROM files WHERE filename = ? AND directory = ?', (filename, directory)).fetchone()[0])
            cur.execute('DELETE FROM files WHERE filename = ? AND directory = ?', (filename, directory))
        if type == 'folder':
            folder = str(directory + '%')
            cur.execute('DELETE FROM files WHERE directory LIKE ?', (folder,))
        conn.commit()
        conn.close()
        return arcname
    def ls(self, directory):
        conn, cur = self.dbConnect()
        files = cur.execute('SELECT filename FROM files WHERE directory = ?', (directory,)).fetchall()
        conn.close()
        return files
    def clear(self):
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        with open('modules/config.sql') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
class fileManager():
    """docstring for fileManager."""

    def __init__(self, password):
        super(fileManager, self).__init__()
        self.zipCur = encDir()
        self.dbCur = fileDB()
        self.uploadDir = 'modules/DATA/files/upload/'
        self.tmpPath = 'modules/DATA/files/tmp/'
        self.password = password
    def getMD5(self, plaintext):
        m = md5()
        m.update(plaintext.encode('utf-8'))
        hash = str(m.hexdigest())
        return hash
    def encrypt(self, plaintext):
        encodedtext = base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
        ciphertext = cryptocode.encrypt(encodedtext, self.password)
        return ciphertext
    def decrypt(self, ciphertext):
        encodedtext = cryptocode.decrypt(ciphertext.decode('utf-8'), self.password)
        plaintext = base64.b64decode(encodedtext).decode('utf-8')
        return plaintext
    def add(self, filename):
        # Get parameters
        path = str(self.uploadDir + filename)
        arcname = self.getMD5(filename)
        plaindata = open(path, 'r').read()
        cipherdata = self.encrypt(plaindata)
        # Adding to databasde and zip
        self.zipCur.add(cipherdata, arcname)
        self.dbCur.add(filename, arcname, 'file', '/')
    def open(self, filename):
        tmp = str(self.tmpPath + filename)
        # Getting the data
        arcname = self.getMD5(filename)
        ciphertext = self.zipCur.getData(arcname)
        plaindata = self.decrypt(ciphertext)
        # Writing the data
        open(tmp, 'w').write(plaindata)
        # Opening file
        if platform == 'linux':
            opener = 'xdg-open'
        elif platform == 'darwin':
            opener = 'open'
        call([opener ,tmp])
    def rm(self, filename):
        arcname = self.dbCur.rm(filename, '/', 'file')
        self.zipCur.rm(arcname)
    def clear(self):
        self.zipCur.clear()
        self.dbCur.clear()
    def ls(self, directory):
        files = self.dbCur.ls(directory)
        fileList = []
        for file in files:
            fileList.append(file[0])
        return fileList
