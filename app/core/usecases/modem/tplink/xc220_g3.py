from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class xc220_g3:

    def check_login(_chorme, host_login, port_login, password_login):
        try:
            _chorme.get("http://"+host_login+":"+port_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "pc-login-password"))
            )

            _chorme.find_element(By.ID, "pc-login-password").send_keys(password_login)
            _chorme.find_element(By.ID, "pc-login-btn").click()        

            if esta_visivel(_chorme, By.ID, "confirm-yes"):
                WebDriverWait(_chorme, 10).until(
                    EC.presence_of_element_located((By.ID, "confirm-yes"))
                ).click()
            
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "wireless"))
            )

            _chorme.find_element(By.ID, "wireless").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "ssid_2g"))
            )
            
            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False


    def change_password(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:
            _chorme.get("http://"+host_login+":"+port_login)

            if esta_visivel(_chorme, By.ID, "pc-login-password"):
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
                EC.presence_of_element_located((By.ID, "ssid_2g"))
            )

            div = _chorme.find_element(By.ID, "enableSmartConn")
            classes = div.get_attribute("class")
            if "off" in classes.split():
                WebDriverWait(_chorme, 25).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='enableSmartConn']/div"))
                ).click()
                
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "mask"))    
                )
                
            if esta_visivel(_chorme, By.ID, "ssid_5g") :
                _chorme.refresh()
                WebDriverWait(_chorme, 25).until(
                    EC.invisibility_of_element_located((By.ID, "mask"))    
                )

            ssid_input = _chorme.find_element(By.ID, "ssid_2g")
            ssid_input.clear()
            ssid_input.send_keys(newNameSSID)

            senha_input = _chorme.find_element(By.ID, "wpa2PersonalPwd_2g")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)

            _chorme.find_element(By.ID, "save_2g").click()
            WebDriverWait(_chorme, 25).until(
                EC.invisibility_of_element_located((By.ID, "mask"))    
            )

            return True

        except Exception as e:
            print("❌ Erro ao configurar o Wi-Fi:", e)
            return False

        finally:
            _chorme.quit()


def esta_visivel(driver, by, seletor):
    try:
        elemento = driver.find_element(by, seletor)
        return elemento.is_displayed()
    except Exception as e:
        return False