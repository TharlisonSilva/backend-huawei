from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class px3321_t1:

    def check_login(_chorme, host_login, port_login, username_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "loginBtn"))
            )

            _chorme.find_element(By.ID, "username").send_keys(username_login)
            _chorme.find_element(By.ID, "userpassword").send_keys(password_login)
            _chorme.find_element(By.ID, "loginBtn").click()        

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "card_wifi"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False
        
    def change_password(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "loginBtn"))
            )

            _chorme.find_element(By.ID, "username").send_keys(username_login)
            _chorme.find_element(By.ID, "userpassword").send_keys(password_login)
            _chorme.find_element(By.ID, "loginBtn").click()        

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "card_wifi"))
            )

            _chorme.find_element(By.CSS_SELECTOR, "div#card_wifi.border-icon").click()
            
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wifisettingbox"))        
            )

            if unificarRedes:

                sleep(1)
                check = _chorme.find_element(By.ID, "WiFiSettings_wifikeepsame")
                jaEstaMarcado = check.is_selected()

                if not jaEstaMarcado:
                    _chorme.find_element(By.ID, "WiFiSettings_wifikeepsame_label").click()

                sleep(1)
                ssid_booth_input = _chorme.find_element(By.ID, "WiFiSettings_both_wifiname")
                for _ in range(50):  # apaga até 30 caracteres
                    ssid_booth_input.send_keys(Keys.BACKSPACE)
                ssid_booth_input.send_keys(newNameSSID)

                sleep(1)
                senha_booth_input = _chorme.find_element(By.ID, "WiFiSettings_both_wifipassword")
                senha_booth_input.clear()
                senha_booth_input.send_keys(newPasswordSSID)
                
            else:
                sleep(1)
                check = _chorme.find_element(By.ID, "WiFiSettings_wifikeepsame")
                if check.is_selected():
                    _chorme.find_element(By.ID, "WiFiSettings_wifikeepsame_label").click()

                sleep(1)
                ssid_24_input = _chorme.find_element(By.ID, "WiFiSettings_24g_wifiname")
                for _ in range(50):
                    ssid_24_input.send_keys(Keys.BACKSPACE)
                ssid_24_input.send_keys(newNameSSID)

                sleep(1)
                ssid_25_input = _chorme.find_element(By.ID, "WiFiSettings_5g_wifiname")
                for _ in range(50):
                    ssid_25_input.send_keys(Keys.BACKSPACE)
                ssid_25_input.send_keys(newNameSSID+"_5G")

                sleep(1)
                senha_24_input = _chorme.find_element(By.ID, "WiFiSettings_24g_wifipassword")
                senha_24_input.clear()
                senha_24_input.send_keys(newPasswordSSID)

                sleep(1)
                senha_25_input = _chorme.find_element(By.ID, "WiFiSettings_5g_wifipassword")
                senha_25_input.clear()
                senha_25_input.send_keys(newPasswordSSID)
        
            sleep(3)
            _chorme.find_element(By.ID, "WiFiSettings_btnsave").click()
            WebDriverWait(_chorme, 70).until(
                lambda d: d.find_element(By.ID, "card_24gwifiname").text == newNameSSID
            )

            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False

        finally:
            _chorme.quit()