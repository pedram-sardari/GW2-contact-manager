import pickle
import pathlib

import constants as cs


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
            self.__file_obj = self.__file_path.open('rb')
            return pickle.load(self.__file_obj)
        else:
            raise TypeError(cs.Messages.CANNOT_READ_MSG)

    def write(self, data):
        if self.__mode == 'w':
            self.__file_obj = self.__file_path.open('wb')
            pickle.dump(data, self.__file_obj)
        else:
            raise TypeError(cs.Messages.CANNOT_WRITE_MSG)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file_obj.close()
