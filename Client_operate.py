import grpc
import meeting_pb2
import meeting_pb2_grpc
def setstub(ipport):
    channel = grpc.insecure_channel(ipport)
    stub = meeting_pb2_grpc.MeetingServiceStub(channel)
    return stub
def checkfreeroom(stub):
    room_list = stub.GetFreeRooms(meeting_pb2.EmptyRequest())
    if not room_list.rooms:
        return False
    return room_list
def isinrooms(selected, room_list):
    if meeting_pb2.Room(roomName=selected) in room_list.rooms:
        return True
    else:
        return False
def querybyid(stub, ID):
    m = stub.QueryByID(meeting_pb2.QueryByIDRequest(meetingID=ID))
    if m.meetingID != '':
        return m
    else:
        return False
def querbyname(stub, name):
    res = stub.QueryByOrganizer(meeting_pb2.QueryByOrganizerRequest(organizerName=name))
    for m in res.meetings:
        print(f"ID:{m.meetingID}, 主题:{m.topic}, 时间:{m.startTime} - {m.endTime}")
    if not res.meetings:
        print("未找到会议")
def cancelmeeting(stub, ID):
    id = ID.upper()
    res = stub.CancelMeeting(meeting_pb2.CancelRequest(meetingID=id))
    print("取消成功" if res.success else "取消失败")

def bookmeeting(stub, organizer, roomName, topic, startTime, endTime, peopleCount):
    meeting = (meeting_pb2.Meeting
    (
        organizer=organizer,
        roomName=roomName,
        topic=topic,
        startTime=startTime,
        endTime=endTime,
        peopleCount=peopleCount
    ))
    res = stub.BookMeeting(meeting_pb2.MeetingRequest(meeting=meeting))
    if res.success:
        m = querybyid(stub, res.meetingID)
        print(f'预约成功！ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}')
        return res.meetingID
    else:
        print("预约失败")
