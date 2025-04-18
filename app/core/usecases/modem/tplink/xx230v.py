from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class xx230v:

    def check_login(_chorme, host_login, port_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "pc-login-password"))
            )

            _chorme.find_element(By.ID, "pc-login-password").send_keys(password_login)
            _chorme.find_element(By.ID, "pc-login-btn").click()        

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "wireless"))
            )

            _chorme.find_element(By.ID, "wireless").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "ssid_bs"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False


    def change_password(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "pc-login-password"))
            )

            _chorme.find_element(By.ID, "pc-login-password").send_keys(password_login)
            _chorme.find_element(By.ID, "pc-login-btn").click()        

            WebDriverWait(_chorme, 20).until(
                EC.presence_of_element_located((By.ID, "wireless"))
            )

            _chorme.find_element(By.ID, "wireless").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "ssid_bs"))
            )

            ssid_input = _chorme.find_element(By.ID, "ssid_bs")
            ssid_input.clear()
            ssid_input.send_keys(newNameSSID)

            senha_input = _chorme.find_element(By.ID, "wpa2PersonalPwd_bs")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)

            _chorme.find_element(By.ID, "save_bs").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "ssid_bs"))
            )

            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False

        finally:
            _chorme.quit()