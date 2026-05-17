import multiprocessing
import time

def get_html(n):
    time.sleep(n)
    print("sub_progress success")
    return n

#多进程编程
if __name__ == "__main__":
    # progress = multiprocessing.Process(target=get_html, args=(2,))
    # print(progress.pid)
    # progress.start()
    #
    # print(progress.pid)
    # progress.join()
    #
    # print("main progress end")

    # 创建进程池
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    # result = pool.apply_async(get_html, args=(3,))
    # # 等待所有任务完成
    # pool.close()
    # pool.join()
    # print(result.get())

    # imap 按顺序处理任务并返回结果
    for result in pool.imap(get_html, [1, 5, 3]):
        print("{} sleeep success".format(result))

    # 哪个任务先完成就先返回哪个结果
    # 不保证输出顺序，只保证效率最高
    for result in pool.imap_unordered(get_html, [1, 5, 3]):
        print("{} imap_unordered sleep success".format(result))

