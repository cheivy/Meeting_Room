#from datetime import datetime, timedelta
import grpc
import meeting_pb2
import meeting_pb2_grpc
#import Clear_Screen

def checkfreeroom(stub):
    room_list = stub.GetFreeRooms(meeting_pb2.EmptyRequest())
    if not room_list.rooms:
        print("暂无可用会议室！")
        return False
    for i, r in enumerate(room_list.rooms):
        print(f"{i + 1}. 会议室{r.roomName}")
    return True


def querybyid(stub, ID):
    m = stub.QueryByID(meeting_pb2.QueryByIDRequest(meetingID=ID))
    if m.meetingID != '':
        #print(f"查询成功 ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}, 主题:{m.topic}, 时间{m.startTime} - {m.endTime}")
        return m
    else:
        print("未找到会议")
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
        #m = stub.QueryByID(meeting_pb2.QueryByIDRequest(meetingID=res.meetingID))
        m = querybyid(stub, res.meetingID)
        # print("预约成功！")
        # print("预约信息：")
        # print(f"ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}, 主题:{m.topic}")
        # print(f"时间{m.startTime} - {m.endTime}")
        print(f'预约成功！ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}')
        return res.meetingID
    else:
        print("预约失败")
