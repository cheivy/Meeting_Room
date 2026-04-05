#from operator import truediv
from datetime import datetime, timedelta
import grpc
import meeting_pb2
import meeting_pb2_grpc
import Clear_Screen

import Client_operate

RED = "\033[31m"  # 红
GREEN = "\033[32m"  # 绿
YELLOW = "\033[33m"  # 黄
BLUE = "\033[34m"  # 蓝
PURPLE = "\033[35m"  # 紫
CYAN = "\033[36m"  # 青
WHITE = "\033[37m"  # 白
RESET = "\033[0m"  #重置

def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = meeting_pb2_grpc.MeetingServiceStub(channel)

    while True:
        Clear_Screen.clear_screen()
        print(BLUE+"==== 会议室预约系统 ===="+RESET)
        print("1. 查看空闲会议室")
        print("2. 预约会议室")
        print("3. 根据ID查询会议")
        print("4. 根据组织者查询会议")
        print("5. 取消会议")
        print("0. 退出")
        choice = input("请选择操作：")

        if choice == "1":
            Clear_Screen.clear_screen()
            # ====================== 先获取空闲会议室 ======================
            print("[可用会议室]")
            #room_list = stub.GetFreeRooms(meeting_pb2.EmptyRequest())
            room_list = Client_operate.checkfreeroom(stub)
            for i, r in enumerate(room_list.rooms):
                print(f"{i + 1}. 会议室{r.roomName}")
            # for i in room_list.rooms:
            #     print(i)
            if not room_list.rooms:
                print("暂无可用会议室！")
            input("按回车键继续...")
        elif choice == "2":
            Clear_Screen.clear_screen()
            # ====================== 先获取空闲会议室 ======================
            #print("\n[可用会议室]")
            room_list = stub.GetFreeRooms(meeting_pb2.EmptyRequest())
            #for i, r in enumerate(room_list.rooms):
            #    print(f"{i + 1}. 会议室{r.roomName}")
            # for i in room_list.rooms:
            #     print(i)
            if not room_list.rooms:
                print("暂无可用会议室！")
                input("按回车键继续...")
                continue

            # while True:
            #     selected = input("请输入会议室编号：").upper()
            #     #selected = selected.upper()
            #     if meeting_pb2.Room(roomName=selected) in room_list.rooms:
            #         break
            #     else:
            #         print("没有这样的会议室")



            # organizer = input("组织者姓名：")
            # #room = input("会议室名称：")
            # topic = input("会议主题：")
            # start = input("开始时间(例：2025-04-01 10:00)：")
            # dtstart = datetime.strptime(start, "%Y-%m-%d %H:%M")
            # strstart = dtstart.strftime("%Y-%m-%d %H:%M")
            # while True:
            #     during = int(input("会议时长(H)："))
            #     if during <= 5 and during >= 1:
            #         break
            #     if during > 5:
            #         print("时间不得大于5小时")
            #     elif during < 1:
            #         print("时间不得小于1小时")
            #     else:
            #         print("非法输入")
            # dtend = dtstart + timedelta(hours=during)
            # result = dtend.strftime("%Y-%m-%d %H:%M")
            # cnt = int(input("参与人数："))
            meeting= Client_operate.bookmeeting('cyw', 'A', 'game', '2023-11-12 10:00', '2023-11-22 11:00', 4)
            # meeting = (meeting_pb2.Meeting
            # (
            #     organizer=organizer,
            #     roomName=selected,
            #     topic=topic,
            #     startTime=strstart,
            #     endTime=result,
            #     peopleCount=cnt
            # ))

            res = stub.BookMeeting(meeting_pb2.MeetingRequest(meeting=meeting))
            if res.success:
                print("预约成功！")
                m = stub.QueryByID(meeting_pb2.QueryByIDRequest(meetingID=res.meetingID))
                print("预约信息：")
                print(f"ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}, 主题:{m.topic}")
                print(f"时间{m.startTime} - {m.endTime}")
            else:
                print("预约失败")
            input("按回车键继续...")
        elif choice == "3":
            Clear_Screen.clear_screen()
            mid = input("输入会议ID：")
            #m = stub.QueryByID(meeting_pb2.QueryByIDRequest(meetingID=mid))
            m = Client_operate.querybyid(stub, mid)
            if m.meetingID != '':
                print(f"ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}, 主题:{m.topic}")
                print(f"时间{m.startTime} - {m.endTime}")
            else:
                print("未找到会议")
            input("按回车键继续...")
        elif choice == "4":
            Clear_Screen.clear_screen()
            name = input("输入组织者姓名：")
            #res = stub.QueryByOrganizer(meeting_pb2.QueryByOrganizerRequest(organizerName=name))
            res = Client_operate.querbyname(stub, name)
            for m in res.meetings:
                print(f"ID:{m.meetingID}, 主题:{m.topic}, 时间:{m.startTime} - {m.endTime}")
            if not res.meetings:
                print("未找到会议")
            input("按回车键继续...")
        elif choice == "5":
            Clear_Screen.clear_screen()
            mid = input("输入会议ID：").upper()
            #res = stub.CancelMeeting(meeting_pb2.CancelRequest(meetingID=mid))
            res = Client_operate.cancelmeeting(stub, mid)
            print("取消成功" if res.success else "取消失败")
            input("按回车键继续...")
        elif choice == "0":
            break

        else:
            print("无效操作")
            input("按回车键继续...")
if __name__ == '__main__':
    run()