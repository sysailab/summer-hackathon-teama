import threading
from concurrent import futures
import PyPDF2
from PyPDF2 import errors as PdfError
from work_queue import WorkQueue
from model_event import ModelEvent

class ModelController:
    SIGNAL = "request again"

    def __init__(self) -> None:
        self.__poolSize = 5
        self.threadPool = futures.ThreadPoolExecutor(max_workers = self.__poolSize)

    def work(self) -> None:
        # main 클래스에 있는 input queue에서 데이터를 가져와 thread pool에서 thread 할당
        while True:
            pdfData = WorkQueue.inputQueue.get()

            # Input Queue에 있는 PDF(path)를 통해 Thread Pool에 텍스트 추출 thread 요청
            # 추출 완료 시, GPT Queue에 추출한 텍스트와 event Enqueue
            self.threadPool.submit(
                self.extractTextFromPDF, 
                pdfData,
            ).add_done_callback(self.putGPTQueue)

    def extractTextFromPDF(self, filePath, pageNumber:list = [0, -2, -1]) -> list:
        with open(filePath, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf)

            # PDF에서 텍스트 추출 시도
            try:
                numbers = [page for page in pageNumber if page < (len(reader.pages) - 2)]   # PDF 페이지 전처리
                return [filePath] + [                                                       # fliePath + 추출한 텍스트
                    reader.pages[page].extract_text() for page in numbers
                ]
            
            # PDF 암호화 예외
            except PdfError.FileNotDecryptedError:
                print("암호화된 논문입니다.")

            # 이미지 기반 논문 예외
            except IndexError:
                return self.extractTextFromImage(filePath)

    def extractTextFromImage(self, filePath) -> list:
        # TODO: 이미지 기반 논문 텍스트 추출(Google Cloud Vision API)
        pass

    def putGPTQueue(self, future: futures.Future) -> None:
        if future.result() is not None:
            filePath = future.result()[0]                   # PDF 파일 경로
            text = future.result()[1:]                      # 추출한 텍스트
            event = ModelEvent()                            # 이벤트 객체
            WorkQueue.gptQueue.put([text, event])           # GPT Queue에 전달
            event.wait()                                    # 이벤트 발생 대기

            pageStart = 1                                   # 추가 논문 시작 페이지
            step = 3                                        # 추가 논문 페이징 단위
            while event.retValue == ModelController.SIGNAL: # GPT 분류 실패(논문 재요청, 성공까지 반복)
                text = self.extractTextFromPDF(             # 텍스트 추출
                    filePath, 
                    [page for page in range(pageStart, pageStart + step)],
                )[1:]
                pageStart += step                           # 다음 논문 시작 페이지 갱신
                event.clear()                               # 이벤트 초기화
                WorkQueue.gptQueue.put([text, event])       # GPT Queue에 전달
                event.wait()                                # 이벤트 발생 대기
    
    
            WorkQueue.saveQueue.put(event.retValue)         # GPT 분류 성공(saveQueue에 전달)
            event.clear()                                   # 이벤트 초기화 후 thread 반환
