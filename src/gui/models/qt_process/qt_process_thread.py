import traceback

from src.core.pyqt_core import *


class QtProcessThread(QObject):
    progress_signal = pyqtSignal(int)
    error_signal = pyqtSignal(list)

    def __init__(self, method, model_options: list[dict]) -> None:
        super().__init__()
        self.method = method
        self.model_options = model_options

    def run(self, return_queue):
        try:
            plots = self.method(self.model_options, self.progress_signal)
            return_queue.put(plots)
        except Exception as e:
            exception_traceback = traceback.format_exc()
            var = [e, exception_traceback]
            self.error_signal.emit(var)
