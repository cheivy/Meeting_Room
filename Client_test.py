from concurrent.futures import ThreadPoolExecutor
import time
import grpc
import meeting_pb2
import meeting_pb2_grpc
import Client_operate

channel = grpc.insecure_channel('127.0.0.1:50051')
stub = meeting_pb2_grpc.MeetingServiceStub(channel)
def task1():
    time.sleep(2)
    meetingID1 = Client_operate.bookmeeting(stub,'cyw','A','game','2023-02-11 10:00','2023-02-12 11:00', 3)
    meetingID2 = Client_operate.bookmeeting(stub, 'cyw', 'D', 'game', '2023-01-11 10:00', '2023-01-12 11:00', 3)
    time.sleep(7)
    Client_operate.cancelmeeting(stub, meetingID1)
    Client_operate.cancelmeeting(stub, meetingID2)
def task2():
    time.sleep(2)
    meetingID1 = Client_operate.bookmeeting(stub, 'wyc', 'B', 'name', '2023-03-11 10:00', '2023-03-12 11:00', 4)
    meetingID2 = Client_operate.bookmeeting(stub, 'wyc', 'C', 'name', '2023-04-11 10:00', '2023-04-12 11:00', 4)
    time.sleep(7)
    Client_operate.cancelmeeting(stub, meetingID1)
    Client_operate.cancelmeeting(stub, meetingID2)
def task3():
    time.sleep(15)
    Client_operate.checkfreeroom(stub)
def task4():
    time.sleep(5)
    Client_operate.querbyname(stub, 'cyw')
def task5():
    time.sleep(5)
    Client_operate.querbyname(stub, 'wyc')
def taskbook():
    while True:
        getfreeroom = stub.GetFreeRooms(meeting_pb2.EmptyRequest())
        if getfreeroom.rooms:
            break
    meetingID1 = Client_operate.bookmeeting(stub, 'wyc', getfreeroom.rooms[0].roomName, 'name', '2023-03-11 10:00', '2023-03-12 11:00', 4)



if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        # for i in range(5):
        #     executor.submit(task1)
        # for i in range(5):
        #     executor.submit(task2)
        # for i in range(3):
        #     executor.submit(task3)
        # for i in range(4):
        #     executor.submit(task4)
        for i in range(4):
            executor.submit(taskbook)
