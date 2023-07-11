from work_queue import WorkQueue
from model_controller import ModelController
from gpt_thread import GptThread
import threading
import time



def main():
    while True:
        WorkQueue.inputQueue.put("thesis\\thesis1.pdf")
        # WorkQueue.inputQueue.put("thesis\\thesis2.pdf")
        # WorkQueue.inputQueue.put("thesis\\no_text.pdf")
        # WorkQueue.inputQueue.put("thesis\\image_thesis.pdf")
        time.sleep(1000)

    


model = ModelController()
gpt = GptThread()

modelThread = threading.Thread(target= lambda: model.work())
gptThread = threading.Thread(target = lambda: gpt.work())

modelThread.start()
gptThread.start()

main()
