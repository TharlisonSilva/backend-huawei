from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class xx530v:

    def check_login(_chorme, host_login, port_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "pc-login-password"))
            )

            _chorme.find_element(By.ID, "pc-login-password").send_keys(password_login)
            _chorme.find_element(By.ID, "pc-login-btn").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "wireless"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False


    def change_password(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:
            # 3. Abre a página do modem
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "pc-login-password"))
            )

            # 4. Faz login (ajuste os IDs conforme o HTML real do seu modem)
            _chorme.find_element(By.ID, "pc-login-password").send_keys(password_login)
            _chorme.find_element(By.ID, "pc-login-btn").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "wireless"))
            )

            # 5. Clica no item do menu <span id="wireless">
            _chorme.find_element(By.ID, "wireless").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "ssid_bs"))
            )

            # 6. Preenche o SSID
            ssid_input = _chorme.find_element(By.ID, "ssid_bs")
            ssid_input.clear()
            ssid_input.send_keys(newNameSSID)

            # 7. Preenche a senha
            senha_input = _chorme.find_element(By.ID, "wpa2PersonalPwd_bs")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)

            # 8. Clica no botão salvar
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