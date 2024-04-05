import base64
import pickle
import pathlib

import constants as cs
import security

class PickleHandler:
    __valid_modes = ['r', 'w']

    def __init__(self, file_path: str, mode: str):
        self.__file_path = pathlib.Path(file_path)
        self.__mode = self.__validate_mode(mode)
        self.__file_obj = None

    def __validate_mode(self, mode):
        if mode not in self.__valid_modes:
            raise ValueError(cs.Messages.INVALID_MODE_MSG.format(self.__valid_modes))
        return mode

    def read(self):
        if self.__mode == 'r':
            if self.__file_path.exists():
                self.__file_obj = self.__file_path.open('rb')
                encrypted_data = self.__file_obj.read()
                pickled_date = security.decrypt(encrypted_content=encrypted_data)
                return pickle.loads(pickled_date)
            else:
                raise ValueError(cs.Messages.FILE_NOT_FOUND_MSG.format(self.__file_path.name))
        else:
            raise TypeError(cs.Messages.CANNOT_READ_MSG)

    def write(self, data):
        if self.__mode == 'w':
            self.__file_obj = self.__file_path.open('wb')
            pickled_data = pickle.dumps(data)
            encrypted_data = security.encrypt(content=pickled_data)
            self.__file_obj.write(encrypted_data)
        else:
            raise TypeError(cs.Messages.CANNOT_WRITE_MSG)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__file_obj:
            self.__file_obj.close()
