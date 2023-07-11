from work_queue import WorkQueue
from model_controller import ModelController
from model_event import ModelEvent
import threading
import time 

class GptThread:
    def work(self):
        print("GPT Thread Started")
        while True:
            # TODO: GPT Queue를 모니터링 하고, 값이 들어오면 GPT API를 이용해 데이터 분류
            #       성공 시, Thread Model에게 분류한 데이터를 전달 후 event set
            #       실패 시, Thread Model에게 논문 추가 데이터 요청 후 event set
            datas = WorkQueue.gptQueue.get()
            texts: list = datas[0]
            event: ModelEvent = datas[1]

            # for t in texts:
            #     print('=======================================')
            #     print(t)

            # TODO: GPT API를 통해 데이터 분류

            #################################
            time.sleep(3)
            event.set(ModelController.SIGNAL)