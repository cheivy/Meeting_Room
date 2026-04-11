import grpc
from concurrent import futures
import meeting_pb2
import meeting_pb2_grpc
import meetIDget
from datetime import datetime

RED = "\033[31m"  # 红
GREEN = "\033[32m"  # 绿
YELLOW = "\033[33m"  # 黄
BLUE = "\033[34m"  # 蓝
RESET = "\033[0m"  #重置

class MeetingService(meeting_pb2_grpc.MeetingServiceServicer):
    def __init__(self):
        self.meetings = {}
        self.free_rooms = ['A', 'B', 'C', 'D', 'E']

    def GetFreeRooms(self, request, context):
        rooms = [meeting_pb2.Room(roomName=name) for name in self.free_rooms]
        return meeting_pb2.RoomList(rooms=rooms)

    def BookMeeting(self, request, context):
        meeting = request.meeting
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if meeting.roomName in self.free_rooms:
            self.free_rooms.remove(meeting.roomName)
            meeting.meetingID = meetIDget.generate_meeting_id()
            self.meetings[meeting.meetingID] = meeting
            print(GREEN+f"[{current_time}]预约成功：ID={meeting.meetingID}, 会议室={meeting.roomName}"+RESET)
            return meeting_pb2.BookResponse(success=True, meetingID = meeting.meetingID)
        else:
            print(RED+f"[{current_time}]预约失败：会议室 {meeting.roomName} 已被占用"+RESET)
            return meeting_pb2.BookResponse(success=False)

    def QueryByID(self, request, context):
        mid = request.meetingID
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(BLUE+f"[{current_time}]查询id为：{mid}的会议"+RESET)
        return self.meetings.get(mid, meeting_pb2.Meeting())

    def QueryByOrganizer(self, request, context):
        name = request.organizerName
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(BLUE+f"[{current_time}]查询{name}的会议"+RESET)
        result = [m for m in self.meetings.values() if m.organizer == name]
        return meeting_pb2.MeetingList(meetings=result)

    def CancelMeeting(self, request, context):
        mid = request.meetingID
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if mid in self.meetings:
            canceled_meeting = self.meetings[mid]
            self.free_rooms.append(canceled_meeting.roomName)  # 归还
            self.free_rooms.sort()
            del self.meetings[mid]
            print(GREEN+f"[{current_time}]取消会议成功：会议室 {canceled_meeting.roomName} 已归还"+RESET)
            return meeting_pb2.CancelResponse(success=True)
        return meeting_pb2.CancelResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    meeting_pb2_grpc.add_MeetingServiceServicer_to_server(MeetingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(YELLOW+f"[{current_time}]会议室预约服务已启动 (端口 50051)"+RESET)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()