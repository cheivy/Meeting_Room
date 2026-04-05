import grpc
from concurrent import futures
import meeting_pb2
import meeting_pb2_grpc
#import time
import meetIDget

class MeetingService(meeting_pb2_grpc.MeetingServiceServicer):
    def __init__(self):
        self.meetings = {}  # 存储会议：key=meetingID, value=Meeting对象
        #self.current_id = ''

        # ====================== 初始化 5 个空闲会议室 ======================
        self.free_rooms = ['A', 'B', 'C', 'D', 'E']

    def GetFreeRooms(self, request, context):
        print("执行了一次查询")
        rooms = [meeting_pb2.Room(roomName=name) for name in self.free_rooms]
        return meeting_pb2.RoomList(rooms=rooms)

    def BookMeeting(self, request, context):
        meeting = request.meeting

        # 如果会议室空闲，才允许预约
        if meeting.roomName in self.free_rooms:
            self.free_rooms.remove(meeting.roomName)  # 从空闲列表删除
            meeting.meetingID = meetIDget.generate_meeting_id()
            self.meetings[meeting.meetingID] = meeting
            #self.current_id += 1
            print(f"[服务端] 预约成功：ID={meeting.meetingID}, 会议室={meeting.roomName}")
            return meeting_pb2.BookResponse(success=True, meetingID = meeting.meetingID)
        else:
            print(f"[服务端] 预约失败：会议室 {meeting.roomName} 已被占用")
            return meeting_pb2.BookResponse(success=False)

        # meeting.meetingID = self.current_id
        # self.meetings[self.current_id] = meeting
        # self.current_id += 1
        # print(f"[服务端] 预约成功：ID={meeting.meetingID}, 组织者={meeting.organizer}")
        # return meeting_pb2.BookResponse(success=True)

    def QueryByID(self, request, context):
        mid = request.meetingID
        print(f"查询id为：{mid}的会议")
        return self.meetings.get(mid, meeting_pb2.Meeting())

    def QueryByOrganizer(self, request, context):
        name = request.organizerName
        print(f"查询{name}的会议")
        result = [m for m in self.meetings.values() if m.organizer == name]
        return meeting_pb2.MeetingList(meetings=result)

    def CancelMeeting(self, request, context):
        mid = request.meetingID

        if mid in self.meetings:
            canceled_meeting = self.meetings[mid]
            self.free_rooms.append(canceled_meeting.roomName)  # 归还
            # for i in self.free_rooms:
            #     print(i)
            self.free_rooms.sort()
            del self.meetings[mid]
            print(f"[服务端] 取消会议成功：会议室 {canceled_meeting.roomName} 已归还")
            return meeting_pb2.CancelResponse(success=True)
        return meeting_pb2.CancelResponse(success=False)

        # if mid in self.meetings:
        #     del self.meetings[mid]
        #     return meeting_pb2.CancelResponse(success=True)
        # return meeting_pb2.CancelResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    meeting_pb2_grpc.add_MeetingServiceServicer_to_server(MeetingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ 会议室预约服务已启动 (端口 50051)")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()