# -*- conding: utf-8 -*-
import pygubu, frida
import tkinter as tk
import threading
import fridump

logo = """
 ______ ___________ _____           ___ _____   ______ 
|___  /|  ___| ___ \\  _  |         / _ \\_   _|  | ___ \\
   / / | |__ | |_/ / | | |_      _/ /_\\ \\| | ___| |_/ /
  / /  |  __||    /| | | \\ \\ /\\ / /  _  || |/ _ \\    / 
./ /___| |___| |\\ \\ \\_/ /\\ V  V /| | | || |  __/ |\\ \\ 
\\_____/\\____/\\_| \\_|\\___/  \\_/\\_/ \\_| |_/\\_/\\___\\_| \\_|
- made by zer0water(blog.naver.com/sshohan, 2020/05/13)
- 본 도구를 불법적으로 사용 시 책임은 본인에게 있습니다.
"""
class HookThread(threading.Thread):
    def __init__(self,app):
        threading.Thread.__init__(self)
        self.zerowater = app

    def run(self):
        for device in self.zerowater.devices:
            if device.name == self.zerowater.dev_Combo.get():
                while(1):
                    #print(device)
                    #print(self.zerowater.prlist_Combo.get())
                    try:
                        session = device.attach(self.zerowater.prlist_Combo.get())
                    except:
                        continue
                    #print(self.zerowater.create_hookcode())
                    try:
                        script = session.create_script(self.zerowater.create_hookcode())
                    except:
                        self.zerowater.hooklog_Text.insert(tk.END,'[ERROR] 잘못된 후킹코드 삽입\n')
                        break
                    script.on('message', self.on_message)
                    script.load()
                    break
                break

    def on_message(self, message, data):
        try:
            if message:
                self.zerowater.hooklog_Text.insert(tk.END,'[LOG] {}\n'.format(message["payload"]))
        except Exception as e:
            self.zerowater.hooklog_Text.insert(tk.END,'[ERROR]'+str(message)+'\n')
            self.zerowater.hooklog_Text.insert(tk.END,'[ERROR]'+str(e)+'\n')
        

class ZerowaterApp:
    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('zerowater.ui')
        master.title('Mobile Hooking Tool v1.0')
        self.set_Frame = builder.get_object('set_Frame', master)

        # Arch Combo
        self.arch_Combo = builder.get_object('arch_Combo', master)
        self.arch_Combo['values'] = ("Android","iOS")
        
        # Scroll Bar 붙이기
        
        self.hookcode_Text = builder.get_object('hookcode_Text', master)
        self.hookcode_xScroll = builder.get_object('hookcode_xScroll', master)
        self.hookcode_yScroll = builder.get_object('hookcode_yScroll', master)
        self.hookcode_Text['xscrollcommand'] = self.hookcode_xScroll.set
        self.hookcode_Text['yscrollcommand'] = self.hookcode_yScroll.set
        self.hookcode_xScroll['command'] = self.hookcode_Text.xview
        self.hookcode_yScroll['command'] = self.hookcode_Text.yview
        self.hooklog_Text = builder.get_object('hooklog_Text', master)
        self.hooklog_xScroll = builder.get_object('hooklog_xScroll', master)
        self.hooklog_yScroll = builder.get_object('hooklog_yScroll', master)
        self.hooklog_Text['xscrollcommand'] = self.hooklog_xScroll.set
        self.hooklog_Text['yscrollcommand'] = self.hooklog_yScroll.set
        self.hooklog_xScroll['command'] = self.hooklog_Text.xview
        self.hooklog_yScroll['command'] = self.hooklog_Text.yview

        # HookFunc
        self.hfnc_Entry = builder.get_object('hfnc_Entry', master)
        # HookClass
        self.hcls_Entry = builder.get_object('hcls_Entry', master)
        # HookParamCount
        self.hkcnt_Entry = builder.get_object('hkcnt_Entry', master)
        self.hookcode = ''

        # HookParam Type, Name 객체
        self.hkptype1_Entry = builder.get_object('hkptype1_Entry', master)
        self.hkptype2_Entry = builder.get_object('hkptype2_Entry', master)
        self.hkptype3_Entry = builder.get_object('hkptype3_Entry', master)
        self.hkptype4_Entry = builder.get_object('hkptype4_Entry', master)
        self.hkptype5_Entry = builder.get_object('hkptype5_Entry', master)
        self.hkptype6_Entry = builder.get_object('hkptype6_Entry', master)
        self.hkptype7_Entry = builder.get_object('hkptype7_Entry', master)
        self.hkptype8_Entry = builder.get_object('hkptype8_Entry', master)
        self.hkptype9_Entry = builder.get_object('hkptype9_Entry', master)
        self.hkptype10_Entry = builder.get_object('hkptype10_Entry', master)
        self.hkpname1_Entry = builder.get_object('hkpname1_Entry', master)
        self.hkpname2_Entry = builder.get_object('hkpname2_Entry', master)
        self.hkpname3_Entry = builder.get_object('hkpname3_Entry', master)
        self.hkpname4_Entry = builder.get_object('hkpname4_Entry', master)
        self.hkpname5_Entry = builder.get_object('hkpname5_Entry', master)
        self.hkpname6_Entry = builder.get_object('hkpname6_Entry', master)
        self.hkpname7_Entry = builder.get_object('hkpname7_Entry', master)
        self.hkpname8_Entry = builder.get_object('hkpname8_Entry', master)
        self.hkpname9_Entry = builder.get_object('hkpname9_Entry', master)
        self.hkpname10_Entry = builder.get_object('hkpname10_Entry', master)

        # CheckBox 객체
        self.cntzero_bool = tk.IntVar()
        self.cntzero_Check = builder.get_object('cntzero_Check', master)
        self.cntzero_Check['variable'] = self.cntzero_bool


        # Combobox 객체
        self.dev_Combo = builder.get_object('dev_Combo',master)
        self.prlist_Combo = builder.get_object('prlist_Combo',master)

        self.hookcount = 1


        # 콜백설정
        callbacks = {
                'on_clear_clicked': self.on_clear_clicked,
                'on_device_clicked': self.on_device_clicked,
                'on_process_clicked': self.on_process_clicked,
                'on_cntzero_change':self.on_cntzero_change,
                'on_sslpin_click':self.on_sslpin_click,
                'on_hookadd_click':self.on_hookadd_click,
                'on_hookstart_click':self.on_hookstart_click,
                'on_dump_click':self.on_dump_click
            }
        builder.connect_callbacks(callbacks)

    def on_clear_clicked(self):
        for a in range(1,11):
            eval('self.hkpname{}_Entry.delete(0, tk.END)'.format(a))
            eval('self.hkptype{}_Entry.delete(0, tk.END)'.format(a))

    def on_device_clicked(self):
        self.devices = frida.get_device_manager().enumerate_devices()
        self.dev_Combo['values'] = ()
        devList = []
        for device in self.devices:
            devList.append(device.name)
        self.dev_Combo['values'] = devList

    def on_process_clicked(self):
        self.prlist_Combo['values'] = ()
        processList = []
        for device in self.devices:
            if device.name.strip() == self.dev_Combo.get().strip():
                processes = device.enumerate_processes()
                for process in processes:
                    processList.append(process.name)
                self.prlist_Combo['values'] = processList
                break

    def on_dump_click(self):
        for device in self.devices:
            if device.name.strip() == self.dev_Combo.get().strip():
                t = threading.Thread(target=fridump.start, args=(device, self.prlist_Combo.get(), self.hooklog_Text))
                t.start()

    def on_cntzero_change(self):
        if(self.cntzero_bool.get()):
            for a in range(1,11):
                eval("self.hkpname{}_Entry.configure(state=tk.DISABLED)".format(a))
                eval("self.hkptype{}_Entry.configure(state=tk.DISABLED)".format(a))
                self.hkcnt_Entry.delete(0, tk.END)
                self.hkcnt_Entry.insert(0,"0")
        else:
            for a in range(1,11):
                eval("self.hkpname{}_Entry.configure(state=tk.NORMAL)".format(a))
                eval("self.hkptype{}_Entry.configure(state=tk.NORMAL)".format(a))

    def create_hookcode(self):
        self.hookcode = self.hookcode_Text.get("1.0",tk.END)
        if self.arch_Combo.get().strip() == "Android":
            self.fullhookcode = """
    Java.perform(function () {{
        {}
    }});
    """.format(self.hookcode)
        elif self.arch_Combo.get().strip() == "iOS":
            self.fullhookcode = """
    if(ObjC.available){
        {}
    } else {
        send("Object-C Runtime is not available!");
    }
    """.format(self.hookcode)

        return self.fullhookcode

    def get_hook_type(self):
        param_count = int(self.hkcnt_Entry.get())
        if param_count == 0:
            return "."
        returnValue = []
        for a in range(1,param_count+1):
            eval("returnValue.append('\"'+self.hkptype{}_Entry.get()+'\"')".format(a))
        return ".overload({})".format(",".join(returnValue))

    def get_hook_name(self):
        param_count = int(self.hkcnt_Entry.get())
        if param_count == 0:
            return ""
        returnValue = []
        for a in range(1,param_count+1):
            eval("returnValue.append(self.hkpname{}_Entry.get())".format(a))
        return ",".join(returnValue)

    def on_sslpin_click(self):
        self.hookcode = self.hookcode_Text.get("1.0",tk.END)
        self.hookcode = self.hookcode + """
        var System = Java.use("java.lang.System");
        if (System.getProperty){
            System.getProperty.overloads[0].implementation = function(prop){
                send("called : system.getProperty("+ prop.toString() +")");
                if (prop.toString().toLowerCase().indexOf("proxy") > -1){
                    send("bypass proxy check : " + prop);
                    return;
                }
                var ret = this.getProperty(prop);
                send("ret value : " + ret.toString());
                return ret;
            };
        }
    """
        self.hookcode_Text.delete(1.0, tk.END)
        self.hookcode_Text.insert(tk.END,self.hookcode)

    def on_hookadd_click(self):
        self.hookcode = self.hookcode_Text.get("1.0",tk.END)
        if self.arch_Combo.get().strip() == "Android":
            self.hookcode = self.hookcode + """
        var c{0} = Java.use("{1}");
        c{0}.{2}{3}.implementation = function({4}){{
            send("*************{2} HOOK START*****************");
            [INPUT YOUR CODE]
        }};
        """.format(self.hookcount, self.hcls_Entry.get(), self.hfnc_Entry.get(), self.get_hook_type(), self.get_hook_name())
            self.hookcount = self.hookcount + 1
            self.hookcode_Text.delete(1.0, tk.END)
            self.hookcode_Text.insert(tk.END,self.hookcode)
        elif self.arch_Combo.get().strip() == "iOS":
            self.hookcode = self.hookcode + """
        var c{0} = Objc.classes.{1};
        Interceptor.attach(c{0}["- {2}"].implementation, {{
            onEnter: function(args){{
                [INPUT YOUR CODE]
            }},
            onLeave: function(retVal){{
                [INPUT YOUR CODE]
            }}
        }});
        """.format(self.hookcount, self.hcls_Entry.get(), self.hfnc_Entry.get())
            self.hookcount = self.hookcount + 1
            self.hookcode_Text.delete(1.0, tk.END)
            self.hookcode_Text.insert(tk.END,self.hookcode)

    def on_hookstart_click(self):
        th = HookThread(self)
        th.start()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    app = ZerowaterApp(root)
    root.mainloop()


