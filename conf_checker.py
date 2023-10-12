import os
import shutil
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
from datetime import datetime
from configparser import ConfigParser
import re


# definition des acronyme
#btn : bouton
#lsb : listbox
#lab : label

class App:
    def __init__(self, root):
        #setting title
        root.title("Splunk App Stanza validator")
        #setting window size
        self.folder_selected=""
        self.now = datetime.now()
        self.date_str=self.now.strftime("%Y-%m-%d")
        width=582
        height=467
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.btn_select_app=tk.Button(root)
        self.btn_select_app["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_select_app["font"] = ft
        self.btn_select_app["fg"] = "#000000"
        self.btn_select_app["justify"] = "center"
        self.btn_select_app["text"] = "Select app directory"
        self.btn_select_app.place(x=10,y=10,width=141,height=40)
        self.btn_select_app["command"] = self.btn_select_app_command

        self.lsb_default=tk.Listbox(root)
        self.lsb_default["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lsb_default["font"] = ft
        self.lsb_default["fg"] = "#333333"
        self.lsb_default["justify"] = "center"
        self.lsb_default.place(x=10,y=80,width=250,height=250)

        self.lsb_local=tk.Listbox(root)
        self.lsb_local["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lsb_local["font"] = ft
        self.lsb_local["fg"] = "#333333"
        self.lsb_local["justify"] = "center"
        self.lsb_local.place(x=320,y=80,width=250,height=250)

        self.lab_default_lsb=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.lab_default_lsb["font"] = ft
        self.lab_default_lsb["fg"] = "#333333"
        self.lab_default_lsb["justify"] = "center"
        self.lab_default_lsb["text"] = "default stanza files"
        self.lab_default_lsb.place(x=10,y=50,width=252,height=31)

        self.lab_local_lsb=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.lab_local_lsb["font"] = ft
        self.lab_local_lsb["fg"] = "#333333"
        self.lab_local_lsb["justify"] = "center"
        self.lab_local_lsb["text"] = "Local stanza files"
        self.lab_local_lsb.place(x=320,y=50,width=249,height=30)

        self.lab_app_path=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.lab_app_path["font"] = ft
        self.lab_app_path["fg"] = "#333333"
        self.lab_app_path["justify"] = "left"
        self.lab_app_path["text"] = "Path : ..."
        self.lab_app_path.place(x=160,y=20,width=435,height=30)

        self.btn_detect_double=tk.Button(root)
        self.btn_detect_double["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_detect_double["font"] = ft
        self.btn_detect_double["fg"] = "#000000"
        self.btn_detect_double["justify"] = "center"
        self.btn_detect_double["text"] = "Detect double stanza"
        self.btn_detect_double.place(x=10,y=340,width=250,height=30)
        self.btn_detect_double["command"] = self.btn_detect_double_command

        self.btn_merge=tk.Button(root)
        self.btn_merge["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_merge["font"] = ft
        self.btn_merge["fg"] = "#000000"
        self.btn_merge["justify"] = "center"
        self.btn_merge["text"] = "Merge default and local"
        #self.btn_merge["state"] = "disabled"
        self.btn_merge.place(x=10,y=420,width=250,height=30)
        self.btn_merge["command"] = self.btn_merge_command

        self.btn_backup_file=tk.Button(root)
        self.btn_backup_file["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_backup_file["font"] = ft
        self.btn_backup_file["fg"] = "#000000"
        self.btn_backup_file["justify"] = "center"
        self.btn_backup_file["text"] = "backup selected files"
        self.btn_backup_file.place(x=320,y=380,width=250,height=30)
        self.btn_backup_file["command"] = self.btn_backup_file_command

        self.btn_backup_all_file=tk.Button(root)
        self.btn_backup_all_file["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_backup_all_file["font"] = ft
        self.btn_backup_all_file["fg"] = "#000000"
        self.btn_backup_all_file["justify"] = "center"
        self.btn_backup_all_file["text"] = "backup all default files"
        self.btn_backup_all_file.place(x=320,y=420,width=250,height=30)
        self.btn_backup_all_file["command"] = self.btn_backup_all_file_command

        self.lab_file_info=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.lab_file_info["font"] = ft
        self.lab_file_info["fg"] = "#333333"
        self.lab_file_info["justify"] = "left"
        self.lab_file_info["text"] = "version 0.0.4"
        self.lab_file_info.place(x=320,y=330,width=250,height=30)

        # self.lab_default_last_update=tk.Label(root)
        # ft = tkFont.Font(family='Times',size=10)
        # self.lab_default_last_update["font"] = ft
        # self.lab_default_last_update["fg"] = "#333333"
        # self.lab_default_last_update["justify"] = "left"
        # self.lab_default_last_update["text"] = "Default last update :"
        # self.lab_default_last_update.place(x=320,y=360,width=256,height=30)

        # self.lab_local_last_update=tk.Label(root)
        # ft = tkFont.Font(family='Times',size=10)
        # self.lab_local_last_update["font"] = ft
        # self.lab_local_last_update["fg"] = "#333333"
        # self.lab_local_last_update["justify"] = "left"
        # self.lab_local_last_update["text"] = "Local Last update :"
        # self.lab_local_last_update.place(x=320,y=390,width=255,height=32)


    #select app path
    def btn_select_app_command(self):
        self.folder_selected = filedialog.askdirectory()
        # print(self.folder_selected)
        self.lab_app_path["text"]=self.folder_selected
        
        self.lsb_default.delete(0,END)
        self.lsb_local.delete(0,END)
        # default_appconf_path=self.folder_selected+"/default/app.conf"
        # isExisting = os.path.exists(default_appconf_path)
        for root, dirs, files in os.walk(self.folder_selected + "/default/" ):
            for file in files:
                if file.endswith('.conf'):
                    print(os.path.join(root, file))
                    self.lsb_default.insert(0,file)
        for root, dirs, files in os.walk(self.folder_selected + "/metadata/" ):
            for file in files:
                if file.endswith('default.meta'):
                    print(os.path.join(root, file))
                    self.lsb_default.insert(0,file)
        for root, dirs, files in os.walk(self.folder_selected + "/local/" ):
            for file in files:
                if file.endswith('.conf'):
                    print(os.path.join(root, file))
                    self.lsb_local.insert(0,file)
        for root, dirs, files in os.walk(self.folder_selected + "/metadata/" ):
            for file in files:
                if file.endswith('local.meta'):
                    print(os.path.join(root, file))
                    self.lsb_local.insert(0,file)


    def get_root_focus_values(self):
        val={}
        val["selected_listbox"]=str(root.focus_get())
        if val["selected_listbox"] == ".!listbox":
            val["dir"]="/default/"
            val["new_dir"]="/default_"+self.date_str+"/"
            for i in self.lsb_default.curselection():
                #print(self.lsb_default.get(i))
                val["selected_file"]=self.lsb_default.get(i)
                val["short_name"] = "default_" + val["selected_file"]
                if val["selected_file"] == "default.meta" : 
                    val["dir"]="/metadata/"
                    val["short_name"] = "metadata_" + val["selected_file"]

        elif val["selected_listbox"]  == ".!listbox2":
            val["dir"]="/local/"
            val["new_dir"]="/local_"+self.date_str+"/"
            for i in self.lsb_local.curselection():
                #print(self.lsb_local.get(i))
                val["selected_file"]=self.lsb_local.get(i)
                val["short_name"] = "local_" + val["selected_file"]
                if val["selected_file"] == "local.meta" : 
                    val["dir"]="/metadata/"
                    val["short_name"] = "metadata_" + val["selected_file"]
        else:
            val["dir"]=None
            val["new_dir"]=None
            val["selected_file"]=None
            val["short_name"]=None
            #print("no file selected")
        return val
    
    

    def btn_detect_double_command(self):
        values=self.get_root_focus_values()
        print(values["selected_file"])
        # config_parser = ConfigParser()
        # config_parser.optionxform = str
        # config_parser.read(self.folder_selected+values["dir"]+values["selected_file"])
        # for section in config_parser.sections():
        #     for key in dict(config_parser.items(section)):
        #         print(key)
        self.check_validate_no_duplicate_stanzas(self.folder_selected+values["dir"]+values["selected_file"],values["short_name"],values["selected_file"])


    def btn_merge_command(self):
        values=self.get_root_focus_values()
        print(values["selected_file"])
        self.check_validate_merge_stanzas(self.folder_selected+"/default/"+values["selected_file"],self.folder_selected+"/local/"+values["selected_file"],values["selected_file"])
        
    def check_validate_merge_stanzas(self,path_default,path_local,file):
        stanzas_regex = r"^\[([^\[\]]*)\]"
        if file == "default.meta" or file == "local.meta" :
            path_default=self.folder_selected+"/metadata/default.meta"
            path_local=self.folder_selected+"/metadata/local.meta"
            short = "metadata_"+file
        else:
            short = "default_"+file
        self.current_stanza=short
        self.stanzas={}
        self.stanzas[short]={}
        self.stanzas[short]["stanza_found"]={}
        self.stanzas[short]["stanza_data"]={}
        self.stanzas[short]["stanza_list"]=[]
        reporter_output=""
        stanza_line=1
        if os.path.exists(path_default):
            with open(path_default) as f:
                line_number = 1
                line = f.readline()

                while line:
                    m = re.search(stanzas_regex,line)
                    
                    if m != None:
                        print(m.group(0),"<======== MATCH")
                        #print(m.group(1))
                        #print(m)
                        stanza_line = str(line_number)
                        self.stanzas[short]["stanza_list"].append((path_default,line_number, m.group(1)))
                        self.stanzas[short]["stanza_data"][stanza_line] = {}
                        self.stanzas[short]["stanza_data"][stanza_line]["title"]= str(m.group(1))
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] = "["+str(m.group(1))+"]\n"
                        #print(stanzas)
                    else:
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] += str(line)
                    while '\n\n' in self.stanzas[short]["stanza_data"][stanza_line]["data"]:
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] = self.stanzas[short]["stanza_data"][stanza_line]["data"].replace("\n\n", "\n")
                    line = f.readline()
                    line_number += 1
        if os.path.exists(path_local):
            with open(path_local) as f:
                line_number = 10000
                line = f.readline()

                while line:
                    m = re.search(stanzas_regex,line)
                    
                    if m != None:
                        print(m.group(0),"<======== MATCH")
                        #print(m.group(1))
                        #print(m)
                        stanza_line = str(line_number)
                        self.stanzas[short]["stanza_list"].append((path_local,line_number, m.group(1)))
                        self.stanzas[short]["stanza_data"][stanza_line] = {}
                        self.stanzas[short]["stanza_data"][stanza_line]["title"]= str(m.group(1))
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] = "["+str(m.group(1))+"]\n"
                        #print(stanzas)
                    else:
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] += str(line)
                    while '\n\n' in self.stanzas[short]["stanza_data"][stanza_line]["data"]:
                        self.stanzas[short]["stanza_data"][stanza_line]["data"] = self.stanzas[short]["stanza_data"][stanza_line]["data"].replace("\n\n", "\n")
                    line = f.readline()
                    line_number += 1 
        for fileref, line_num, match in self.stanzas[short]["stanza_list"]:
            # print("----")
            # print(fileref)
            # print(line_num)
            # print(match)
            if not match in self.stanzas[short]["stanza_found"]:
                self.stanzas[short]["stanza_found"][match]=[]
            self.stanzas[short]["stanza_found"][match].append(line_num)

        for key, linenos in self.stanzas[short]["stanza_found"].items():
            if len(linenos) > 1:
                reporter_output += ("\n\nDuplicate [{}] stanzas were found. ").format(key)
                for lineno in linenos:
                    reporter_output += ("\n In line: {}.").format(lineno)
                    reporter_output += self.stanzas[short]["stanza_data"][str(lineno)]["data"]
        if reporter_output == "":
            showinfo(title="Verification de fichier", message="fichier " + file + " ne contient pas d'item en double")
            self.create_window_double_mgmt()
        else:
            # showwarning(title="Verification de fichier", message="fichier " + file + "contient des items en doublons\n"+reporter_output)
            self.create_window_double_mgmt()

    #backup files
    def btn_backup_file_command(self):
        values=self.get_root_focus_values()
        if values["selected_file"]:
            try:
                if not os.path.exists(self.folder_selected+values["new_dir"]):
                    os.mkdir(self.folder_selected+values["new_dir"])
                shutil.copyfile(self.folder_selected+values["dir"]+values["selected_file"], self.folder_selected+values["new_dir"]+values["selected_file"])
                showinfo(title="Copie de fichier", message="fichier " + values["selected_file"] + " copié dans le dossier " + self.folder_selected+values["new_dir"])
            except:
                showwarning(title="Copie de fichier", message="ERREUR de copie du fichier " + values["selected_file"] + " dans le dossier " + self.folder_selected+values["new_dir"])


    def btn_backup_all_file_command(self):
        values=self.get_root_focus_values()
        try:
            for root, dirs, files in os.walk(self.folder_selected + "/default/" ):
                for file in files:
                    if file.endswith('.conf'):
                        print(os.path.join(root, file))
                        if not os.path.exists(self.folder_selected+"/default_"+self.date_str+"/"):
                            os.mkdir(self.folder_selected+"/default_"+self.date_str+"/")
                        shutil.copyfile(self.folder_selected+"/default/"+file, self.folder_selected+"/default_"+self.date_str+"/"+file)
            showinfo(title="Copie des fichiers", message=" Les fichiers de configuration du dossier default ont été cloné dans le dossier " + self.folder_selected + "/default_" + self.date_str + "/")
        except:
            showwarning(title="Copie des fichiers", message="ERREUR de copie des fichiers dans le dossier " + self.folder_selected + "/default_" + self.date_str + "/")

    def check_validate_no_duplicate_stanzas(self,path,short,file):
        stanzas_regex = r"^\[([^\[\]]*)\]"
        self.current_stanza=short
        self.stanzas={}
        self.stanzas[short]={}
        self.stanzas[short]["stanza_found"]={}
        self.stanzas[short]["stanza_data"]={}
        self.stanzas[short]["stanza_list"]=[]
        reporter_output=""
        stanza_line=1
        with open(path) as f:
            line_number = 1
            line = f.readline()

            while line:
                m = re.search(stanzas_regex,line)
                
                if m != None:
                    print(m.group(0),"<======== MATCH")
                    #print(m.group(1))
                    #print(m)
                    stanza_line = str(line_number)
                    self.stanzas[short]["stanza_list"].append((path,line_number, m.group(1)))
                    self.stanzas[short]["stanza_data"][stanza_line] = {}
                    self.stanzas[short]["stanza_data"][stanza_line]["title"]= str(m.group(1))
                    self.stanzas[short]["stanza_data"][stanza_line]["data"] = "["+str(m.group(1))+"]\n"
                    #print(stanzas)
                else:
                    self.stanzas[short]["stanza_data"][stanza_line]["data"] += str(line)
                line = f.readline()
                line_number += 1 
        for fileref, line_num, match in self.stanzas[short]["stanza_list"]:
            # print("----")
            # print(fileref)
            # print(line_num)
            # print(match)
            if not match in self.stanzas[short]["stanza_found"]:
                self.stanzas[short]["stanza_found"][match]=[]
            self.stanzas[short]["stanza_found"][match].append(line_num)

        for key, linenos in self.stanzas[short]["stanza_found"].items():
            if len(linenos) > 1:
                reporter_output += ("\n\nDuplicate [{}] stanzas were found. ").format(key)
                for lineno in linenos:
                    reporter_output += ("\n In line: {}.").format(lineno)
                    reporter_output += self.stanzas[short]["stanza_data"][str(lineno)]["data"]
        if reporter_output == "":
            showinfo(title="Verification de fichier", message="fichier " + file + " ne contient pas d'item en double",parent=root)
        else:
            # showwarning(title="Verification de fichier", message="fichier " + file + "contient des items en doublons\n"+reporter_output)
            self.create_window_double_mgmt()
            

    def create_window_double_mgmt(self):
        self.mgmt_window = Toplevel(root)
        self.mgmt_window.title("Double selection window")
        self.mgmt_window.geometry("550x428")
        #setting title
        #setting window size
        width=550
        height=428
        screenwidth = self.mgmt_window.winfo_screenwidth()
        screenheight = self.mgmt_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, ((screenwidth - width) / 2) + 50, ((screenheight - height) / 2) + 50)
        self.mgmt_window.geometry(alignstr)
        self.mgmt_window.resizable(width=False, height=False)

        self.lsb_mgmt=tk.Listbox(self.mgmt_window)
        self.lsb_mgmt["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lsb_mgmt["font"] = ft
        self.lsb_mgmt["fg"] = "#333333"
        self.lsb_mgmt["justify"] = "center"
        self.lsb_mgmt.place(x=10,y=30,width=380,height=385)

        self.btn_select_one_item=tk.Button(self.mgmt_window)
        self.btn_select_one_item["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_select_one_item["font"] = ft
        self.btn_select_one_item["fg"] = "#000000"
        self.btn_select_one_item["justify"] = "center"
        self.btn_select_one_item["text"] = "Select one"
        self.btn_select_one_item.place(x=400,y=30,width=139,height=30)
        self.btn_select_one_item["command"] = self.btn_select_one_item_command

        self.btn_merge_items=tk.Button(self.mgmt_window)
        self.btn_merge_items["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_merge_items["font"] = ft
        self.btn_merge_items["fg"] = "#000000"
        self.btn_merge_items["justify"] = "center"
        self.btn_merge_items["state"] = "disabled"
        self.btn_merge_items["text"] = "WIP : Merge"
        self.btn_merge_items.place(x=400,y=70,width=139,height=30)
        self.btn_merge_items["command"] = self.btn_merge_items_command

        self.btn_keep_double_items=tk.Button(self.mgmt_window)
        self.btn_keep_double_items["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_keep_double_items["font"] = ft
        self.btn_keep_double_items["fg"] = "#000000"
        self.btn_keep_double_items["justify"] = "center"
        self.btn_keep_double_items["state"] = "disabled"
        self.btn_keep_double_items["text"] = "WIP : Keep double"
        self.btn_keep_double_items.place(x=400,y=110,width=140,height=30)
        self.btn_keep_double_items["command"] = self.btn_keep_double_items_command

        self.btn_export_and_close=tk.Button(self.mgmt_window)
        self.btn_export_and_close["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_export_and_close["font"] = ft
        self.btn_export_and_close["fg"] = "#000000"
        self.btn_export_and_close["justify"] = "center"
        self.btn_export_and_close["text"] = "Export and close"
        self.btn_export_and_close.place(x=400,y=385,width=140,height=30)
        self.btn_export_and_close["command"] = self.btn_export_and_close_command
        
        
        self.lab_mgmt_info=tk.Label(self.mgmt_window)
        ft = tkFont.Font(family='Times',size=10)
        self.lab_mgmt_info["font"] = ft
        self.lab_mgmt_info["fg"] = "#333333"
        self.lab_mgmt_info["justify"] = "left"
        self.lab_mgmt_info["text"] = ""
        self.lab_mgmt_info.place(x=400,y=285,width=140,height=100)
        nb_del = 0
        # verification des stanza identique
        for key, linenos in self.stanzas[self.current_stanza]["stanza_found"].items():
            print(key)
            print(linenos)
            if len(linenos) > 1:
                temp_val=[]
                temp_key=[]
                for num in linenos:
                    val = self.stanzas[self.current_stanza]["stanza_data"][str(num)]["data"]
                    print(val)
                    if val not in temp_val:
                        temp_val.append(val)
                        temp_key.append(num)
                    else:
                        nb_del +=1
                print("##############")
                print(temp_val)
                print(temp_key)
                self.stanzas[self.current_stanza]["stanza_found"][key]=temp_key
                print(self.stanzas[self.current_stanza]["stanza_found"][key])
        #insertion des stanza differents pour traitement
        for key, linenos in self.stanzas[self.current_stanza]["stanza_found"].items():
            # print(key)
            # print(linenos)
            if len(linenos) > 1:
                self.lsb_mgmt.insert(0,key + ": x" + str(len(linenos)))
        # mettre la fentere au premier plan
        self.mgmt_window.attributes('-topmost',True)
        # mettre la fenetre devant la fenetre root
        # self.mgmt_window.lift(root)
        # root.lower(self.mgmt_window)
        if nb_del>0:
            showinfo(title="Stanza identique", message="il y " + str(nb_del) + " stanza identique n'entrant pas en conflit non affiché",parent=self.mgmt_window)
        lastindex=self.lsb_mgmt.index("end")
        print("___lastindex___")
        print(lastindex)
        if lastindex > 0:
            self.btn_export_and_close["state"] = "disabled"
            self.lab_mgmt_info["text"] = "Il y a encore\n" + str(lastindex) + " stanza\nen conflits\nvous ne pouvez pas\nencore exporter le\nfichier"
        else:
            self.btn_export_and_close["state"] = "normal"
            self.lab_mgmt_info["text"] = "Il n'y a plus\nde conflit vous\npouvez exporter le\nfichier"



    def get_mgmt_focus_values(self):
        val={}
        val["dir"]="/default/"
        val["new_dir"]="/default_"+self.date_str+"/"
        for i in self.lsb_mgmt.curselection():
            #print(self.lsb_default.get(i))
            val["selected_stanza"]=self.lsb_mgmt.get(i)
        if not val["selected_stanza"]:
            val["dir"]=None
            val["new_dir"]=None
            val["selected_stanza"]=None
            #print("no file selected")
        return val


    def btn_select_one_item_command(self):
        values=self.get_mgmt_focus_values()
        print(values)
        self.current_selected_stanza_item = values["selected_stanza"].split(":")[0]
        self.create_window_double_selection()
        self.mgmt_window.destroy()
       

    def btn_merge_items_command(self):
        print("command")


    def btn_keep_double_items_command(self):
        print("command")


    def btn_export_and_close_command(self):
        print("command")
        export_data=""
        #file_path="C:\\Users\\B0027937\Desktop\\git_splunk_secu\\app_inf_did\inf_did\\test.txt"
        print(self.current_stanza)
        file_term = self.current_stanza.replace('_',"/")
        print(file_term)
        file_complete_path = self.folder_selected + "/" + file_term
        print(file_complete_path)
        print(self.stanzas[self.current_stanza]["stanza_found"])
        sorted_dict = dict(sorted(self.stanzas[self.current_stanza]["stanza_found"].items()))
        print(sorted_dict)
        for key, data in sorted_dict.items():
            export_data+=str(self.stanzas[self.current_stanza]["stanza_data"][str(data[0])]["data"])+"\n"
        try: 
            f = open(file_complete_path, "w")
            f.write(export_data)
            f.close()
            self.mgmt_window.destroy()
            showinfo(title="ecriture du nouveau fichier", message="fichier " + file_complete_path + " enregistré")
        except:
            showinfo(title="ecriture du nouveau fichier", message="fichier " + file_complete_path + " en erreur")


    def create_window_double_selection(self):
        self.select_window = Toplevel(root)
        self.select_window.title("Double selection window")
        self.select_window.geometry("1024x768")
        
        self.lsb_first_double=tk.Text(self.select_window)
        self.lsb_first_double["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lsb_first_double["font"] = ft
        self.lsb_first_double["fg"] = "#333333"
        #self.lsb_first_double["justify"] = "center"
        self.lsb_first_double.place(x=10,y=80,width=500,height=650)

        self.lsb_second_double=tk.Text(self.select_window)
        self.lsb_second_double["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lsb_second_double["font"] = ft
        self.lsb_second_double["fg"] = "#333333"
        #self.lsb_second_double["justify"] = "center"
        self.lsb_second_double.place(x=515,y=80,width=500,height=650)

        self.btn_keep_single=tk.Button(self.select_window)
        self.btn_keep_single["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.btn_keep_single["font"] = ft
        self.btn_keep_single["fg"] = "#000000"
        self.btn_keep_single["justify"] = "center"
        self.btn_keep_single["text"] = "Keep selected"
        self.btn_keep_single.place(x=910,y=740,width=100,height=25)
        self.btn_keep_single["command"] = self.btn_keep_single_command

        self.chb_first_var = tk.IntVar()
        self.chb_second_var = tk.IntVar()

        self.chb_first=tk.Checkbutton(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.chb_first["font"] = ft
        self.chb_first["fg"] = "#333333"
        self.chb_first["justify"] = "center"
        self.chb_first["text"] = "CheckBox"
        self.chb_first.place(x=250,y=740,width=70,height=25)
        self.chb_first["variable"] = self.chb_first_var 
        self.chb_first["offvalue"] = "0"
        self.chb_first["onvalue"] = "1"
        self.chb_first["command"] = self.chb_first_command

        self.chb_second=tk.Checkbutton(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.chb_second["font"] = ft
        self.chb_second["fg"] = "#333333"
        self.chb_second["justify"] = "center"
        self.chb_second["text"] = "CheckBox"
        self.chb_second.place(x=755,y=740,width=70,height=25)
        self.chb_second["variable"] = self.chb_second_var 
        self.chb_second["offvalue"] = "0"
        self.chb_second["onvalue"] = "1"
        self.chb_second["command"] = self.chb_second_command

        self.GLabel_257=tk.Label(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_257["font"] = ft
        self.GLabel_257["fg"] = "#333333"
        self.GLabel_257["justify"] = "center"
        self.GLabel_257["text"] = "label"
        self.GLabel_257.place(x=10,y=40,width=500,height=35)

        self.GLabel_734=tk.Label(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_734["font"] = ft
        self.GLabel_734["fg"] = "#333333"
        self.GLabel_734["justify"] = "center"
        self.GLabel_734["text"] = "label"
        self.GLabel_734.place(x=415,y=40,width=500,height=35)

        self.GButton_381=tk.Button(self.select_window)
        self.GButton_381["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_381["font"] = ft
        self.GButton_381["fg"] = "#000000"
        self.GButton_381["justify"] = "center"
        self.GButton_381["text"] = "<"
        self.GButton_381.place(x=10,y=10,width=35,height=30)
        self.GButton_381["command"] = self.GButton_381_command

        self.GButton_220=tk.Button(self.select_window)
        self.GButton_220["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_220["font"] = ft
        self.GButton_220["fg"] = "#000000"
        self.GButton_220["justify"] = "center"
        self.GButton_220["text"] = ">"
        self.GButton_220.place(x=984,y=10,width=33,height=30)
        self.GButton_220["command"] = self.GButton_220_command

        self.GLabel_8=tk.Label(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_8["font"] = ft
        self.GLabel_8["fg"] = "#333333"
        self.GLabel_8["justify"] = "center"
        self.GLabel_8["text"] = "label"
        self.GLabel_8.place(x=50,y=10,width=70,height=25)

        self.GLabel_361=tk.Label(self.select_window)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_361["font"] = ft
        self.GLabel_361["fg"] = "#333333"
        self.GLabel_361["justify"] = "center"
        self.GLabel_361["text"] = "label"
        self.GLabel_361.place(x=680,y=10,width=70,height=25)
        self.lsb_first_double.insert(END,self.stanzas[self.current_stanza]["stanza_data"][str(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][0])]["data"])
        self.lsb_second_double.insert(END,self.stanzas[self.current_stanza]["stanza_data"][str(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][1])]["data"])


    def btn_keep_single_command(self):
        if  (self.chb_first_var.get() == 1) & (self.chb_second_var.get()  == 0):  
            del self.stanzas[self.current_stanza]["stanza_data"][str(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][1])]
            del self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][1]
            self.select_window.destroy()
            self.create_window_double_mgmt()
        elif (self.chb_first_var.get() == 0) & (self.chb_second_var.get()  == 1):  
            print(self.stanzas[self.current_stanza]["stanza_data"])
            del self.stanzas[self.current_stanza]["stanza_data"][str(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][0])]
            print(self.stanzas[self.current_stanza]["stanza_data"])
            print(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item])
            del self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item][0]
            print(self.stanzas[self.current_stanza]["stanza_found"][self.current_selected_stanza_item])
            self.select_window.destroy()
            self.create_window_double_mgmt()
        else : 
            showwarning(title="Verification de fichier", message="Aucune séléction n'a été faite impossible de poursuivre")


    def chb_first_command(self):
        self.chb_second.deselect()


    def chb_second_command(self):
        self.chb_first.deselect()


    def GButton_381_command(self):
        print("command")


    def GButton_220_command(self):
        print("command")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
