from kivy.config import Config
Config.set('kivy','window_icon','XC.png')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 960)
Config.set('graphics', 'height', 600)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os
import easygui
import shutil
from config import *
"""
pip install google-api-python-client oauth2client
pip install --upgrade oauth2client
"""
date = datetime.datetime.now().strftime("%d-%m")


def write_result(url, date):
    with open('result.txt', 'a', encoding='utf-8') as result_file:
        string_write = f"{url};{date}\n"
        result_file.write(string_write)


SCOPES = ["https://www.googleapis.com/auth/indexing"]


Builder.load_string('''
<MainScreen>:
    limits_text: limits_text
    results_text: results_text
    urls_text: urls_text
    FloatLayout:
        canvas:
            Color:
                rgba: 0, 0, 0, 1
            Line:
                points: [250, 0, 250, 600]
                width: 0.6
        Label:
            text: "Добавьте URL"
            color: 0, 0, 0, 1
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.32, 'y': 0.9}
            halign: "right"
            font_size: 20
        TextInput:
            size_hint: None, None
            pos_hint: {"x": 0.3, "y": 0.5}
            size: 600, 240
            text: root.show_urls()
            id: urls_text
        Label:
            text: "Результат"
            color: 0, 0, 0, 1
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.30, 'y': 0.37}
            halign: "right"
            font_size: 20
        TextInput:
            size_hint: None, None
            pos_hint: {"x": 0.3, "y": 0.05}
            size: 600, 190
            id: results_text
        Button:
            size_hint: None, None
            size: 100, 40
            text: "Запуск"
            pos_hint: {'center_x': 0.874, 'y': 0.39}
            on_press:
                root.logic()
        Button:
            size_hint: None, None
            size: 250, 70
            text: "Индексирование"
            pos_hint: {"x": -0.0007, "y": 0.88}
        Button:
            size_hint: None, None
            size: 250, 70
            text: "JSON"
            pos_hint: {"x": -0.0007, "y": 0.75}
            on_press: root.manager.current = "json"
        Button:
            size_hint: None, None
            size: 250, 70
            text: "FAQ"
            pos_hint: {"x": -0.0007, "y": 0.62}
            on_press: root.manager.current = "faq"
            
        Label:
            text: root.show_limits()
            color: 0, 0, 0, 1
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.63, 'y': 0.37}
            font_size: 19
            halign: "right"
            id: limits_text
        Button:
            size_hint: None, None
            size: 150, 40
            text: "Сохранить результат"
            pos_hint: {'center_x': 0.49, 'y': 0.39}
            on_press:
                root.save_file()
            
                
        
<JsonScreen>:
    jsons_text: jsons_text
    FloatLayout:
        canvas:
            Color:
                rgba: 0, 0, 0, 1
            Line:
                points: [250, 0, 250, 600]
                width: 0.6
        Button:
            size_hint: None, None
            size: 250, 70
            text: "Индексирование"
            pos_hint: {"x": -0.0007, "y": 0.88}
            on_press: root.manager.current = "main"
        Button:
            size_hint: None, None
            size: 250, 70
            text: "JSON"
            pos_hint: {"x": -0.0007, "y": 0.75}
        Button:
            size_hint: None, None
            size: 250, 70
            text: "FAQ"
            pos_hint: {"x": -0.0007, "y": 0.62}
            on_press: root.manager.current = "faq"
        Label:
            text: "JSON ключи"
            color: 0, 0, 0, 1
            size_hint: 0.1, 0.1
            pos_hint: {'x': 0.3, 'y': 0.9}
            halign: "right"
        TextInput:
            size_hint: None, None
            pos_hint: {"x": 0.3, "y": 0.5}
            size: 600, 240
            text: root.show_jsons()
            id: jsons_text
        Button:
            size_hint: None, None
            size: 100, 40
            text: "Загрузить"
            pos_hint: {'center_x': 0.874, 'y': 0.39}
            on_press:
                root.load_jsons()
<FaqScreen>:
    FloatLayout:
        canvas:
            Color:
                rgba: 0, 0, 0, 1
            Line:
                points: [250, 0, 250, 600]
                width: 0.6
        Button:
            size_hint: None, None
            size: 250, 70
            text: "Индексирование"
            pos_hint: {"x": -0.0007, "y": 0.88}
            on_press: root.manager.current = "main"
        Button:
            size_hint: None, None
            size: 250, 70
            text: "JSON"
            pos_hint: {"x": -0.0007, "y": 0.75}
            on_press: root.manager.current = "json"
        Button:
            size_hint: None, None
            size: 250, 70
            text: "FAQ"
            pos_hint: {"x": -0.0007, "y": 0.62}

        
            
            
            
            
''')


class FaqScreen(Screen):
    pass


class JsonScreen(Screen):
    def show_jsons(self):
        file = open("system.txt", "r")
        path = file.readline()
        file.close()
        json_name_list = ""
        for root, dirs, files in os.walk(path):
            for json_name in files:
                json_name_list += f'{json_name}\n'
        return json_name_list

    def load_jsons(self):
        path = easygui.diropenbox()
        json_name_list = ""
        for root, dirs, files in os.walk(path):
            for json_name in files:
                json_name_list += f'{json_name}\n'
        self.jsons_text.text = json_name_list
        file = open("system.txt", "w")
        file.write(path)
        file.close()


class MainScreen(Screen):
    def show_urls(self):
        file = open("urls.csv", "r")
        lff = file.readlines()
        file.close()
        urls = ""
        for item in lff:
            urls += f"{item}"
        return urls

    def show_limits(self):
        file = open("limits.txt", "r")
        lff = file.readlines()
        file.close()
        return f"0/{lff[1]} (лимиты)"

    def indexURL2(self, u, http):
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        content = {'url': u.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
        result = json.loads(content.decode())
        # For debug purpose only
        if "error" in result:
            self.results_text.text += "Error({} - {}): {}\n".format(result["error"]["code"], result["error"]["status"],
                                              result["error"]["message"])
            return "Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                               result["error"]["message"])
        else:
            self.results_text.text += "urlNotificationMetadata.url: {}\n".format(result["urlNotificationMetadata"]["url"])
            self.results_text.text += "urlNotificationMetadata.latestUpdate.url: {}\n".format(
                result["urlNotificationMetadata"]["latestUpdate"]["url"])
            self.results_text.text += "urlNotificationMetadata.latestUpdate.type: {}\n".format(
                result["urlNotificationMetadata"]["latestUpdate"]["type"])
            self.results_text.text += "urlNotificationMetadata.latestUpdate.notifyTime: {}\n".format(
                result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"])
            return "OK"

    def logic(self):
        count_urls = 0
        system_file = open("system.txt")
        path_data = system_file.readline()
        system_file.close()
        urls_text = self.urls_text.text
        lstdate = open("date.txt", "r")
        lastdate = lstdate.readline()
        lstdate.close()
        for i in urls_text.split():
            with open("urls.csv", "a") as file:
                file.write(f'{i}\n')
        colvo_of_jsons = 0
        for root, dirs, files in os.walk(path_data):
            for json_key_path_name in files:
                colvo_of_jsons += 1
                if lastdate != date:
                    self.limits_text.text = f"0/{colvo_of_jsons * 200} (лимиты)"
                    lstdate = open("date.txt", "w")
                    lstdate.write(date)
                    lstdate.close()
                else:
                    limitsfile = open("limits.txt", "r")
                    limits = limitsfile.readline()
                    limitsfile.close()
                    self.limits_text.text = f"{limits}/{colvo_of_jsons * 200} (лимиты)"
                json_key = f"{path_data}/" + json_key_path_name
                credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scopes=SCOPES)
                http = credentials.authorize(httplib2.Http())
                a_file = open("urls.csv", "r")  # get list of lines
                urls = a_file.readlines()
                a_file.close()
                new_file = open("urls.csv", "w")
                flag = False
                request_google_api = ''
                for url in urls:
                    url_new = url.rstrip("\n")
                    if flag:
                        new_file.write(url)
                    else:
                        request_google_api = MainScreen.indexURL2(self, url_new, http)

                    if 'Error' in request_google_api:
                        flag = True
                        new_file.write(url)
                        request_google_api = ''
                    else:
                        if not flag:
                            write_result('txt_file', url_new)
                            count_urls += 1

                new_file.close()
        self.results_text.text += "Отправлено на индексацию: " + str(count_urls) + " шт.\n"
        if lastdate != date:
            pass
        else:
            limitsfile = open("limits.txt", "r")
            limits = limitsfile.readline()
            limitsfile.close()
            self.limits_text.text = f"{int(limits) + count_urls}/{colvo_of_jsons * 200} (лимиты)"
        filefile = open("limits.txt", "w")
        filefile.write(f"{count_urls}\n{colvo_of_jsons * 200}")
        filefile.close()

    def save_file(self):
        place = easygui.diropenbox()
        shutil.copyfile("result.txt", place + "/result.txt")


class IndexingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(JsonScreen(name='json'))
        sm.add_widget(FaqScreen(name="faq"))
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        return sm


IndexingApp().run()
