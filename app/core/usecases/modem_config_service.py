import time
import re
import tempfile
import shutil
import atexit
import os
import shutil
import uuid
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.core.usecases.modem.huawei.ax2 import ax2
from app.core.usecases.modem.huawei.eg8145x6_10 import eg8145x6_10
from app.core.usecases.modem.mercusys import ax1500, ax3000, mr30g
from app.core.usecases.modem.raisecom import ht803g_ws2
from app.core.usecases.modem.think import tkonu2pdpx
from app.core.usecases.modem.tplink import xc220_g3, xx230v, xx530v
from app.core.usecases.modem.unknow import unknow_default
from app.core.usecases.modem.vsol import v2804ac_z, v2804ax
from app.core.usecases.modem.zte import f6600p
from app.core.usecases.modem.zyxel import px3321_t1
from app.core.usecases.modem.shoreline import shoreline_default
import logging

class modem_config_service:  
    
    logging.basicConfig(
        level=logging.INFO,  # nível mínimo que será exibido
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    def ConfigPasswordModem(host_login, ports_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):

        logging.info("1 - Iniciando objeto webdriver!")
        driver = create_clean_driver()

        logging.info("2 - Objeto criado e cookies limpados!")

        try:
            port_login = "00"
            for itemPort in ports_login :
                correctUrl = check_url_login(driver, host_login, itemPort)
                if correctUrl :
                    port_login = itemPort
                    break


            if(port_login == ""):
                driver.get("http://"+host_login)
            else:
                driver.get("http://"+host_login+":"+port_login)
            
            driver.refresh()
            time.sleep(3)
            

            marca = identificar_marca(driver.page_source)
            modelo = indentifcar_modelo(marca, driver)

            if "Desconhecido" in marca : 
                driver.refresh()
                marca = identificar_marca(driver.page_source)
                modelo = indentifcar_modelo(marca, driver)

            
            logging.info("3 - [ Marca: "+marca+" / Modelo: "+modelo+" ] do equipamento encontrados!")

            if marca == "TP-Link":
                if modelo == "XX230v":
                    logged = False              
                    for itemPass in password_login:
                        logged = xx230v.check_login(driver, host_login, port_login, itemPass)
                        if logged :
                            return xx230v.change_password(driver, host_login, port_login, username_login, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
                
                elif modelo == "XX530v":
                    logged = False
                    for itemPass in password_login:
                        logged = xx530v.check_login(driver, host_login, port_login, itemPass)
                        if logged :
                            return xx530v.change_password(driver, host_login, port_login, username_login, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
                
                elif modelo == "XC220-G3":
                    logged = False
                    for itemPass in password_login:
                        logged = xc220_g3.check_login(driver, host_login, port_login, itemPass)
                        if logged :
                            return xc220_g3.change_password(driver, host_login, port_login, username_login, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
                        
            elif marca == "Zyxel":
                if modelo == "PX3321-T1":
                    logged = False
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = px3321_t1.check_login(driver, host_login, port_login, itemUser, itemPass)
                            if logged:
                                return px3321_t1.change_password(driver, host_login, port_login, itemUser, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
            
            elif marca == "Huawei":
                
                if modelo == "AX2":
                    logged = False
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = ax2.check_login(driver, host_login, port_login, itemUser, itemPass)
                            if logged:
                                return ax2.change_password(driver, newNameSSID, newPasswordSSID, unificarRedes)
                            
                if modelo == "EG8145X6-10":
                    logged = False
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = eg8145x6_10.check_login(driver, host_login, port_login, itemUser, itemPass)
                            if logged:
                                return eg8145x6_10.change_password(driver, newNameSSID, newPasswordSSID, unificarRedes)
                            
                
            
            elif marca == "Shoreline":
                if modelo == "Default" :
                    logged = False
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = shoreline_default.check_login(driver, host_login, port_login, itemUser, itemPass)
                            if logged :
                                return shoreline_default.change_password_SH1015W_and_SH3000WF(driver, host_login, port_login, itemUser, itemPass, newNameSSID, newPasswordSSID, unificarRedes)

            elif marca == "ZTE":

                if modelo == "F6600P" :
                    logged = False
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = f6600p.check_login(driver, host_login, port_login, itemUser, itemPass)
                            if logged :
                                return f6600p.change_password(driver, newNameSSID, newPasswordSSID)

            elif marca == "Mercusys" :
                
                if modelo == "AX3000" :
                    
                    driver.get("http://"+host_login+":"+port_login)
                    driver.refresh()
                    logged = False
                    
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = ax3000.check_login(driver, host_login, port_login, itemPass)
                            if logged :
                                return ax3000.change_password(driver, host_login, port_login, itemUser, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
                            
                elif modelo == "AX1500" :
                    
                    driver.get("http://"+host_login+":"+port_login)
                    driver.refresh()
                    logged = False
                    
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = ax1500.check_login(driver, host_login, port_login, itemPass)
                            if logged :
                                return ax1500.change_password(driver, host_login, port_login, itemUser, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
                            
                elif modelo == "MR30G" :
                    
                    driver.get("http://"+host_login+":"+port_login)
                    driver.refresh()
                    logged = False
                    
                    for itemUser in username_login:
                        for itemPass in password_login:
                            logged = mr30g.check_login(driver, itemPass)
                            if logged :
                                return mr30g.change_password(driver, itemPass, newNameSSID, newPasswordSSID, unificarRedes)
            
            else:
                logged = False
                unknow_default.force_close(driver)
                for itemUser in username_login:
                    for itemPass in password_login:
                        logging.info("3.1 - Iniciando tentativas de log-in. Senha ["+itemPass+"]")

                        time.sleep(1)
                        logged = unknow_default.check_login_v__AX1500ONT(driver, host_login, port_login, itemUser, itemPass)
                        logging.info("3.2 - Resultado de tentativa de login ["+str(logged)+"]")
                        if logged :
                            return shoreline_default.change_password_SH1505W(driver, host_login, port_login, username_login, itemPass, newNameSSID, newPasswordSSID)
                        
                        time.sleep(1)
                        logged = unknow_default.check_login_raisecom_v__HT803G_WS2(driver, host_login, port_login, itemUser, itemPass)
                        logging.info("3.3 - Resultado de tentativa de login ["+str(logged)+"]")
                        if logged :
                            return ht803g_ws2.change_password(driver, newNameSSID, newPasswordSSID)
                        
                        time.sleep(1)
                        logged = unknow_default.check_login_Think_v__TKONU2PDPX(driver, host_login, port_login, itemUser, itemPass)
                        logging.info("3.4 - Resultado de tentativa de login ["+str(logged)+"]")
                        if logged :
                            return tkonu2pdpx.change_password(driver, newNameSSID, newPasswordSSID)
                        
                        time.sleep(1)
                        logged = unknow_default.check_login_VSOL_v__V2804AX(driver, host_login, port_login, itemUser, itemPass)
                        logging.info("3.5 - Resultado de tentativa de login ["+str(logged)+"]")
                        if logged :
                            return v2804ax.change_password(driver, newNameSSID, newPasswordSSID)
                        
                        time.sleep(1)
                        logged = unknow_default.check_login_VSOL_v__V2804AC_Z(driver, host_login, port_login, itemUser, itemPass)
                        logging.info("3.5 - Resultado de tentativa de login ["+str(logged)+"]")
                        if logged :
                            return v2804ac_z.change_password(driver, newNameSSID, newPasswordSSID)
                        

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)

        finally:
            driver.quit()


def identificar_marca(html):
    if re.search(r'TP-Link|TL-WR|Archer', html, re.I):
        return "TP-Link"
    elif re.search(r'Intelbras', html, re.I):
        return "Intelbras"
    elif re.search(r'D-Link|d-link|DLink', html, re.I):
        return "D-Link"
    elif re.search(r'Tenda', html, re.I):
        return "Tenda"
    elif re.search(r'Mercusys', html, re.I):
        return "Mercusys"
    elif re.search(r'Netgear|Nighthawk|Orbi', html, re.I):
        return "Netgear"
    elif re.search(r'Linksys', html, re.I):
        return "Linksys"
    elif re.search(r'Asus', html, re.I):
        return "Asus"
    elif re.search(r'Huawei', html, re.I):
        return "Huawei"
    elif re.search(r'ZTE|ZXHN|F660|F620', html, re.I):
        return "ZTE"
    elif re.search(r'Fiberhome|AN5506', html, re.I):
        return "Fiberhome"
    elif re.search(r'Nokia|Alcatel', html, re.I):
        return "Nokia"
    elif re.search(r'Mikrotik', html, re.I):
        return "Mikrotik"
    elif re.search(r'Ubiquiti|UniFi|EdgeRouter', html, re.I):
        return "Ubiquiti"
    elif re.search(r'Arris|Touchstone', html, re.I):
        return "Arris"
    elif re.search(r'Cisco', html, re.I):
        return "Cisco"
    elif re.search(r'Technicolor|Thomson', html, re.I):
        return "Technicolor"
    elif re.search(r'Dasan|Zhone', html, re.I):
        return "Dasan"
    elif re.search(r'shoreline|shorowifi', html, re.I):
        return "Shoreline"
    elif re.search(r'zyxel|zywall', html, re.I):
        return "Zyxel"
    elif re.search(r'think|thinkwifi|thinkrouter', html, re.I):
        return "Think"
    elif re.search(r'raisecom|iscom', html, re.I):
        return "Raisecom"
    elif re.search(r'Sumec|sumecwifi|sumecrouter|sumecont', html, re.I):
        return "Sumec"
    elif re.search(r'VSOL|vsol|v-solution|vsolution|vsolwifi', html, re.I):
        return "VSOL"
    
    else:
        return "Desconhecido"

def indentifcar_modelo(marca, driver):
    modelo = ""
    if marca == "TP-Link":
        modelo = driver.find_element(By.ID, "pc-bot-productName").text
        return modelo
    
    elif marca == "Intelbras":
        return "Intelbras"
    
    elif marca == "D-Link":
        return "D-Link"
    
    elif marca == "Tenda":
        return "Tenda"
    
    elif marca == "Mercusys":

        if esta_visivel(driver, By.CSS_SELECTOR, ".text-wrap-display") :
            modelo = check_versao_Mercusys_AX3000_AX1500(driver)
        
        return modelo
    
    elif marca == "Netgear":
        return "Netgear"
    
    elif marca == "Linksys":
        return "Linksys"
    
    elif marca == "Asus":
        return "Asus"
    
    elif marca == "Huawei":
        modelo = ""
        
        try:
            itensTitle = driver.title.split()
            if itensTitle[2] == "AX2" :
                modelo = "AX2"
        except Exception as e:
            modelo = ""
        
        if modelo == "" :
            try:
                itensTitle = driver.title
                if itensTitle == "EG8145X6-10" :
                    modelo = "EG8145X6-10"
            except Exception as e:
                modelo = ""

        return modelo
    
    elif marca == "ZTE":
        if esta_visivel(driver, By.ID, "pdtVer") :
            modelo = driver.find_element(By.ID, "pdtVer").text

        return modelo
    
    elif marca == "Fiberhome":
        return "Fiberhome"
    
    elif marca == "Nokia":
        return "Nokia"
    
    elif marca == "Mikrotik":
        return "Mikrotik"
    
    elif marca == "Ubiquiti":
        return "Ubiquiti"
    
    elif marca == "Arris":
        return "Arris"
    
    elif marca == "Cisco":
        return "Cisco"
    
    elif marca == "Technicolor":
        return "Technicolor"
    
    elif marca == "Dasan":
        return "Dasan"
    
    elif marca == "Sheroline":
        return "Sheroline"
    
    elif marca == "Zyxel":
        modelo = driver.find_element(By.CSS_SELECTOR, '#cardpage h3').text
        return modelo
    
    elif marca == "Think":
        return "Think"
    
    elif marca == "Raisecom":
        return "Raisecom"
    
    elif marca == "Sumec":
        return "Sumec"
    
    elif marca == "VSOL":
        return "VSOL"

    else:
        return "Default"

def esta_visivel(driver, by, seletor):
    try:
        elemento = driver.find_element(by, seletor)
        return elemento.is_displayed()
    except Exception as e:
        return False

def check_versao_Mercusys_AX3000_AX1500(driver):
    try:
        DescVersao = driver.find_elements(By.CSS_SELECTOR, ".text-wrap-display")[0]
        versao = DescVersao.text.split()[0]
        return versao
    except Exception as e:
        return ""

def kill_chrome_instances():
    # Finaliza processos antigos (plataforma: Linux/Mac)
    #os.system("pkill chromedriver")
    #os.system("pkill -f 'Google Chrome'")
    teste = ""

def create_clean_driver(headless=False):
    
    # Mata processos anteriores
    kill_chrome_instances()

    excluir_pasta("chrome_profiles")

    # Cria perfil único com UUID
    profile_dir = os.path.abspath(f"chrome_profiles/{uuid.uuid4()}")
    os.makedirs(profile_dir, exist_ok=True)
    
    options = uc.ChromeOptions()
    #options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"  # ajuste aqui
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-translate")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--user-agent=Mozilla/5.0")

    # Desativa recursos irritantes (só por segurança)
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if headless:
        options.headless = True

    driver = uc.Chrome(options=options, use_subprocess=True)

    # Mata cookies/cache via DevTools
    try:
        driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        driver.delete_all_cookies()
    except:
        pass

    # Quando terminar, apaga tudo
    def cleanup():
        try:
            driver.quit()
        except:
            pass
        shutil.rmtree(profile_dir, ignore_errors=True)

    import atexit
    atexit.register(cleanup)

    return driver

def check_url_login(driver, host_login, port_login):
    try:
        driver.get("http://"+host_login+":"+port_login)
        title = driver.title
        
        if esta_visivel(driver, By.ID, "main-frame-error") and title == host_login :
            return False    
        
        return True
    except Exception as e:
        return False
    
def esperar_texto_em_tag(driver, tagType, texto_procurado, timeout=30, intervalo=0.5):
    fim = time.time() + timeout

    while time.time() < fim:
        try:
            tds = driver.find_elements(By.TAG_NAME, tagType)
            for td in tds:
                if texto_procurado in td.text:
                    return True
        except Exception:
            pass

        time.sleep(intervalo)

    return False

def excluir_pasta(pasta_path):
    if os.path.exists(pasta_path):
        shutil.rmtree(pasta_path)
        print(f"✅ Pasta '{pasta_path}' excluída com sucesso.")
    else:
        print(f"❌ Pasta '{pasta_path}' não existe.")