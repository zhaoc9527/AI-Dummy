from exceptiongroup import catch

from src.iot.thing import Thing, Parameter, ValueType
import serial
import time

class Lamp(Thing):
    def __init__(self):
        super().__init__("Lamp", "AI 的机械臂")
        self.connect=False
        self.enable = False
        self.ser=None
        self.dstepValue=25.0;
        print(f"机械臂初始化完成")
        # 定义属性
        self.add_property("enable", "机械臂是否已经使能", lambda: self.enable)

        # 定义方法
        self.add_method("CONNECT", "连接机械臂", [],
                        lambda params: self.Connect())


        self.add_method("ENABLE", "使能机械臂", [],
                        lambda params: self.Enable())

        self.add_method("GoHome", "到初始位", [],
                        lambda params: self.gohome())

        self.add_method("RESET", "到休息位", [],
                        lambda params: self.reset())


        self.add_method("Forward", "往前走", [],
                        lambda params: self.Forward())

        self.add_method("Back", "往后走", [],
                        lambda params: self.Back())

        self.add_method("Left", "往左走", [],
                        lambda params: self.Left())

        self.add_method("Right", "往右走", [],
                        lambda params: self.Right())

        self.add_method("Up", "往上走", [],
                        lambda params: self.Up())

        self.add_method("Down", "往下走", [],
                        lambda params: self.Down())


    def Connect(self):
        try:
            self.ser = serial.Serial('COM4', 115200, timeout=1)
            self.connect = True
            print(f"机械臂已连接")
            return {"success": True, "message": "机械臂已连接"}
        except Exception as e:
            print(f"机械臂连接失败")
            return {"success": False, "message": "机械臂连接失败"}


    def Enable(self):
        try:
             self.ser.write(b'!START\n')
             time.sleep(0.2)
             response = self.ser.readline().decode('utf-8').strip()
             self.enable = True
             print(f"机械臂已使能")
             return {"success": True, "message": "机械臂已使能"}
        except Exception as e:
            print(f"机械臂使能失败")
            return {"success": False, "message": "机械臂使能失败"}


    def gohome(self):
        try:
            self.ser.write(b'!HOME\n')
            time.sleep(0.2)
            response = self.ser.readline().decode('utf-8').strip()
            print(f"机械臂已回到初始位")
            return {"success": True, "message": "机械臂已回到初始位"}
        except Exception as e:
            print(f"机械臂回初始位失败")
            return {"success": False, "message": "机械臂回初始位失败"}

    def reset(self):
        try:
            self.ser.write(b'!REST\n')
            time.sleep(0.2)
            response = self.ser.readline().decode('utf-8').strip()
            print(f"机械臂回休息位")
            return {"success": True, "message": "机械臂已回休息位"}
        except Exception as e:
            print(f"机械臂回休息位失败")
            return {"success": False, "message": "机械臂回休息位失败"}




    def Forward(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X_number = float(numbers[0])  # 转换为浮点数
            Y=numbers[1]
            Z=numbers[2]
            A=numbers[3]
            B=numbers[4]
            C=numbers[5]
            cmd="@"+str(X_number+self.dstepValue)+","+str(Y)+","+str(Z)+","+str(A)+","+str(B)+","+str(C)+"\n"
            self.ser.write(cmd.encode())
            print(f"机械臂已往前走50")
            return {"success": True, "message": "机械臂已往前走50"}
        except Exception as e:
            print(f"机械臂往前走失败:"+str(e))
            return {"success": False, "message": "机械臂往前走失败"}

    def Back(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(1)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X_number = float(numbers[0])  # 转换为浮点数
            Y = numbers[1]
            Z = numbers[2]
            A = numbers[3]
            B = numbers[4]
            C = numbers[5]
            cmd = "@" + str(X_number - self.dstepValue) + "," + str(Y) + "," + str(Z) + "," + str(A) + "," + str(
                B) + "," + str(C) + "\n"
            self.ser.write(cmd.encode())
            print(f"机械臂已往后走50")
            return {"success": True, "message": "机械臂已往后走50"}
        except Exception as e:
            print(f"机械臂往后走失败:"+str(e))
            return {"success": False, "message": "机械臂往后走失败"}

    def Left(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X = numbers[0]  # 转换为浮点数
            Y_number =float(numbers[1])
            Z = numbers[2]
            A = numbers[3]
            B = numbers[4]
            C = numbers[5]
            cmd = "@" + str(X) + "," + str(Y_number - self.dstepValue) + "," + str(Z) + "," + str(A) + "," + str(
                B) + "," + str(C) + "\n"
            self.ser.write(cmd.encode())
            print(f"机械臂已往左走50")
            return {"success": True, "message": "机械臂已往左走50"}
        except Exception as e:
            print(f"机械臂往左走失败")
            return {"success": False, "message": "机械臂往左走失败"}

    def Right(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X= numbers[0]  # 转换为浮点数
            Y_number = float(numbers[1])
            Z = numbers[2]
            A = numbers[3]
            B = numbers[4]
            C = numbers[5]
            cmd = "@" + str(X) + "," + str(Y_number + self.dstepValue) + "," + str(Z) + "," + str(A) + "," + str(
                B) + "," + str(C) + "\n"
            self.ser.write(cmd.encode())
            print(f"机械臂右走50")
            return {"success": True, "message": "机械臂已往右走50"}
        except Exception as e:
            print(f"机械臂往右走失败")
            return {"success": False, "message": "机械臂往右走失败"}
    def Up(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X = numbers[0]  # 转换为浮点数
            Y = numbers[1]
            Z_number = float(numbers[2])
            A = numbers[3]
            B = numbers[4]
            C = numbers[5]
            cmd = "@" + str(X) + "," + str(Y) + "," + str(Z_number + self.dstepValue) + "," + str(A) + "," + str(B) + "," + str(C) + "\n"
            self.ser.write(cmd.encode())
            print(f"机械臂已往上走50")
            return {"success": True, "message": "机械臂已往上走50"}
        except Exception as e:
            print(f"机械臂往上走失败")
            return {"success": False, "message": "机械臂往上走失败"}

    def Down(self):
        try:
            self.ser.write(b'#GETLPOS\n')
            time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
            response = self.ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
            numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
            X = numbers[0]  # 转换为浮点数
            Y = numbers[1]
            Z_number =  float(numbers[2])
            A = numbers[3]
            B = numbers[4]
            C = numbers[5]
            cmd = "@" + str(X) + "," + str(Y) + "," + str(Z_number - self.dstepValue) + "," + str(A) + "," + str(B) + "," + str(C) + "\n"
            self.ser.write(cmd.encode())
            print(f"机械臂下走50")
            return {"success": True, "message": "机械臂已往下走50"}
        except Exception as e:
            print(f"机械臂往下走失败")
            return {"success": False, "message": "机械臂往下走失败"}


if __name__ == "__main__":
    try:
        ser=serial.Serial('COM4', 115200, timeout=1)
        ser.write(b'#GETLPOS\n')
        time.sleep(0.2)  # 根据需要等待一定的时间，给串口设备一些时间来响应
        response = ser.readline().decode('utf-8').strip()  # 读取一行返回的数据，并解码为字符串
        numbers = response.split()[1:]  # 使用 split() 分割字符串，去掉 'ok' 部分
        X_number = float(numbers[0])  # 转换为浮点数
        Y = numbers[1]
        Z = numbers[2]
        A = numbers[3]
        B = numbers[4]
        C = numbers[5]
        cmd = "@" + str(X_number - 5) + "," + str(Y) + "," + str(Z) + "," + str(A) + "," + str(
            B) + "," + str(C) + "\n"
        ser.write(cmd.encode())

    except Exception as e:
        print(f"机械臂往前走失败")