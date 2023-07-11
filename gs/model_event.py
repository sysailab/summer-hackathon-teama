import threading


class ModelEvent:
    def __init__(self) -> None:
        self.__event = threading.Event()
        self.__Lock = threading.Lock()
        self.__retValue = None              # 직접 접근 권장 X, getter 이용

    def set(self, retValue) -> None:
        self.__setReturnValue(retValue)
        self.__event.set()

    def wait(self) -> None:
        self.__event.wait()

    def clear(self) -> None:
        self.__event.clear()

    def __setReturnValue(self, retValue):
        self.__Lock.acquire()
        try:
            self.__retValue = retValue
        finally:
            self.__Lock.release()

    @property
    def retValue(self) -> object:
        self.__Lock.acquire()
        try:
            return self.__retValue
        finally:
            self.__Lock.release()