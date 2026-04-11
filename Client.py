from datetime import datetime, timedelta
import Clear_Screen
import Client_operate

RED = "\033[31m"  # 红
GREEN = "\033[32m"  # 绿
YELLOW = "\033[33m"  # 黄
BLUE = "\033[34m"  # 蓝
PURPLE = "\033[35m"  # 紫
RESET = "\033[0m"  #重置

logo = r'''
 ____    ____               _    _                    _______                                  
|_   \  /   _|             / |_ (_)                  |_   __ \                                 
  |   \/   |  .---.  .---.`| |-'__   _ .--.   .--./)   | |__) |   .--.    .--.   _ .--..--.    
  | |\  /| | / /__\\/ /__\\| | [  | [ `.-. | / /'`\;   |  __ /  / .'`\ \/ .'`\ \[ `.-. .-. |   
 _| |_\/_| |_| \__.,| \__.,| |, | |  | | | | \ \._//  _| |  \ \_| \__. || \__. | | | | | | |   
|_____||_____|'.__.' '.__.'\__/[___][___||__].',__`  |____| |___|'.__.'  '.__.' [___||__||__]  
                                            ( ( __))               
'''

def run():
    stub = Client_operate.setstub('127.0.0.1:50051')
    while True:
        Clear_Screen.clear_screen()
        print(BLUE+logo+RESET)
        menu = [
            "1. 查看空闲会议室",
            "2. 预约会议室",
            "3. 根据ID查询会议",
            "4. 根据组织者查询会议",
            "5. 取消会议",
            "0. 退出"
        ]
        for item in menu:
            print(GREEN+f"<{item}>"+RESET)
        choice = input(YELLOW+"请选择操作："+RESET)
        if choice == "1":
            Clear_Screen.clear_screen()
            if not Client_operate.checkfreeroom(stub):
                print(RED+"暂无可用会议室！")
                input("按回车键继续..."+RESET)
                continue
            print(GREEN+"[可用会议室]:")
            room_list = Client_operate.checkfreeroom(stub)
            for i, r in enumerate(room_list.rooms):
                print(GREEN+f"{i + 1}. 会议室{r.roomName}"+RESET)
            input(YELLOW+"按回车键继续..."+RESET)
        elif choice == "2":
            Clear_Screen.clear_screen()
            if not Client_operate.checkfreeroom(stub):
                print(RED+"暂无可用会议室！"+RESET)
                continue
            room_list = Client_operate.checkfreeroom(stub)
            while True:
                selected = input(YELLOW+"请输入会议室编号："+RESET).upper()
                if Client_operate.isinrooms(selected, room_list):
                    break
                else:
                    print(RED+"没有这样的会议室"+RESET)
            organizer = input(GREEN+"组织者姓名："+RESET)
            topic = input(GREEN+"会议主题："+RESET)
            start = input(GREEN+"开始时间(例：2025-04-01 10:00)："+RESET)
            dtstart = datetime.strptime(start, "%Y-%m-%d %H:%M")
            strstart = dtstart.strftime("%Y-%m-%d %H:%M")
            while True:
                during = int(input(GREEN+"会议时长(H)："+RESET))
                if during <= 5 and during >= 1:
                    break
                if during > 5:
                    print(RED+"时间不得大于5小时"+RESET)
                elif during < 1:
                    print(RED+"时间不得小于1小时"+RESET)
                else:
                    print(RED+"非法输入"+RESET)
            dtend = dtstart + timedelta(hours=during)
            result = dtend.strftime("%Y-%m-%d %H:%M")
            cnt = int(input(GREEN+"参与人数："+RESET))
            Client_operate.bookmeeting(stub, organizer, selected, topic, strstart, result, cnt)
            input(YELLOW+"按回车键继续..."+RESET)
        elif choice == "3":
            Clear_Screen.clear_screen()
            mid = input(GREEN+"输入会议ID："+RESET)
            if not Client_operate.querybyid(stub, mid):
                print(RED+"未找到会议")
                input("按回车键继续..."+RESET)
                continue
            m = Client_operate.querybyid(stub, mid)
            print(PURPLE+f"ID:{m.meetingID}, 组织者:{m.organizer}, 会议室:{m.roomName}, 主题:{m.topic}")
            print(f"时间{m.startTime} - {m.endTime}")
            input("按回车键继续..."+RESET)
        elif choice == "4":
            Clear_Screen.clear_screen()
            name = input(GREEN+"输入组织者姓名："+RESET)
            Client_operate.querbyname(stub, name)
            input(YELLOW+"按回车键继续..."+RESET)
        elif choice == "5":
            Clear_Screen.clear_screen()
            mid = input(GREEN+"输入会议ID："+RESET).upper()
            Client_operate.cancelmeeting(stub, mid)
            input(YELLOW+"按回车键继续..."+RESET)
        elif choice == "0":
            break
        else:
            print(RED+"无效操作")
            input("按回车键继续..."+RESET)
if __name__ == '__main__':
    run()