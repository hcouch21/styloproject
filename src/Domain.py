import os.path
#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Stylo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Stylo.  If not, see <http://www.gnu.org/licenses

import sys
import os

try:
    import Crypto
except:
    print "PyCrypto not installed, corpus encryption is not available"

try:
    import nltk
except:
    print "NLTK must be installed for Stylo to run."
    sys.exit(1)

class Corpus(object):
    """Stores data about a corpus
    name -- Name of the corpus (folder name)
    authors -- List of Authors associated with corpus
    path -- Relative path to corpus folder

    """

    name = None
    authors = None
    uses_encryption = False
    path = None
    
    _loaded = False
    
    def __init__(self, name):
        self.name = name
        self.path = "./corpora/%s/" % name
        self.authors = []
    
    def file_count(self):
        if not self._loaded:
            self.load()
        
        count = 0
        for author in self.authors:
            count += len(author.samples)
        
        return count
    
    def author_count(self):
        if not self._loaded:
            self.load()
        
        return len(self.authors)

    def load(self, password=None):
        author_names = os.listdir(self.path)

        try:
            author_names.remove("stylo")
        except ValueError:
            os.mkdir(self.path + "stylo/")

        for name in author_names:
            author = Author(self.path, name)
            self.authors.append(author)
        
        self._loaded = True

    def __str__(self):
        return "%s - %d authors" % (self.name, len(self.authors))

    def save(self, password=None):
        pass

    def _encrypt(self, password):
        pass

    def _decrypt(self, password):
        pass

    @staticmethod
    def get_all_corpora():
        avail_corpora = []
        corpora_names = os.listdir("./corpora/")

        for name in corpora_names:
            avail_corpora.append(Corpus(name))

        return avail_corpora

class Author(object):
    """Stores data related to an author in a corpus
    name -- Name of the author
    path -- Relative path to author folder
    samples -- List of Samples associated with author

    """

    name = None
    path = None
    samples = None

    def __init__(self, path, name):
        self.name = name
        self.path = path + name + "/"
        self.samples = []

        #print "Loading author: %s" % self.path
        for sample_file in os.listdir(self.path):
            self.samples.append(Sample(self.path, sample_file))

    def __str__(self):
        return "%s - %d samples" % (self.name, len(self.samples))

class Sample(object):
    """Stores data and state of a sample document
    name -- The name of the sample (filename)
    path -- Relative path to the file (including filename)
    feature_results -- List of FeatureResults for extracted features

    plain_text -- Raw characters that make up the sample
    nltk_text -- ntlk.Text object which is a list of tokens
    """

    name = None
    path = None
    feature_results = None

    plain_text = None
    nltk_text = None

    def __init__(self, path, name=None):
        if name is not None:
            self.name = name
            self.path = path + name
        else:
            self.name = os.path.basename(path)
            self.path = path

        with open(self.path, "r") as f:
            self.plain_text = (f.read().decode('latin-1')).encode('utf-8')

        tokenized = []
        for sentence in nltk.sent_tokenize(self.plain_text) :
            tokenized += nltk.word_tokenize(sentence)
        self.nltk_text = nltk.Text(tokenized)

class FeatureResult(object):
    """Stores the value after a linguistic feature is extracted
    name -- The name of the feature this result belongs to
    value -- The actual extracted value
    weight -- The weight of the feature in authorship prediction

    """

    name = None
    value = None
    weight = None

    def __init__(self, name):
        """Creates a feature result

        name -- Name of the feature this result belongs to
        """
        
        self.name = name

    def __str__(self):
        return "%s - %s [%s]" % (self.name, self.value, self.weight)

# Code from:
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

# Code from:
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
