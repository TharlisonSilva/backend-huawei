import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

class ax3000:

    def check_login(_chorme, host_login, port_login, password_login):
        try:
            logging.info("3.1 - Iniciando tenttativa de login com a senha: "+password_login)
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='local-login-pwd']/div/div/span/input[@type='password']"))
            )

            pass_input = _chorme.find_element(By.XPATH, "//div[@id='local-login-pwd']/div/div/span/input[@type='password']")
            for _ in range(150):
                pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(password_login)
            
            _chorme.find_element(By.XPATH, "//div[@id='local-login-button']/div/div/a[@type='button']").click()        

            WebDriverWait(_chorme, 5).until(
                EC.presence_of_element_located((By.ID, "main-menu"))
            )
            
            logging.info("3.2 - Login bem sucedico com a senha: "+password_login)
            return True

        except Exception as e:
            logging.info("3.2 - Senha: "+password_login+" para o login no equipamento")
            return False


    def change_password(_chorme, host_login, port_login, username_login, password_login, newNameSSID, newPasswordSSID, unificarRedes):
        try:
            logging.info("4 - Iniciando processo de troca de senha!")
            _chorme.get("http://"+host_login+":"+port_login)
            
            logging.info("4.1 - Confirmando se a pagina aida cotinua logada!")
            if esta_visivel(_chorme, By.XPATH, "//div[@id='local-login-button']/div/div/a[@type='button']"):
                
                _chorme.find_element(By.XPATH, "//div[@id='local-login-pwd']/div/div/span/input[@type='password']").send_keys(password_login)
                _chorme.find_element(By.XPATH, "//div[@id='local-login-button']/div/div/a[@type='button']").click()        

            logging.info("4.2 - Verificando se o menu já está carregado na pagina.")
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.ID, "main-menu"))
            )

            logging.info("4.3 - Item wireless do menu clicado")
            sleep(2)
            _chorme.find_element(By.XPATH, "//div[@id='main-menu']/div/div/ul/li[@navi-value='wirelessBasic']").click()
            WebDriverWait(_chorme, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-bind='{wireless24g.ssid}']/div/div/span/input[@type='text']"))
            )
            sleep(5)

            check = _chorme.find_element(By.XPATH, "//div[@data-bind='{wirelessSmartConn.smartEnable}']/div/div/ul/li/div/label")
            classes = check.get_attribute("class")
            if "checked" not in classes.split():
                check.click()


            logging.info("4.4 - Informações da pagina de troca de senha e nome do wise carregado!")
            ssid_input = _chorme.find_element(By.XPATH, "//div[@data-bind='{wireless24g.ssid}']/div/div/span/input[@type='text']")
            for _ in range(150):
                ssid_input.send_keys(Keys.BACKSPACE)
            ssid_input.send_keys(newNameSSID)

            logging.info("4.5 - Novo nome da rede wifi atribuido. Nome: "+newNameSSID)
            sleep(1)
            senha_input = _chorme.find_element(By.XPATH, "//div[@data-bind='{wireless24g.pskKey}']/div/div/span/input[@type='text']")
            senha_input.clear()
            senha_input.send_keys(newPasswordSSID)

            logging.info("4.6 - Nova senha da rede wifi atribuido. Senha: "+newPasswordSSID)

            sleep(1)
            if esta_visivel(_chorme, By.XPATH, "//div[@id='save-data']/div/div/a[@type='button' and @title='SALVAR']") :
                _chorme.find_element(By.XPATH, "//div[@id='save-data']/div/div/a[@type='button' and @title='SALVAR']").click()
            
                logging.info("4.7 - botão de salvar clicado!")
                sleep(3)
                if esta_visivel(_chorme, By.XPATH, "//div[@data-bind='{wirelessOnSmartOffNote}']") :
                    logging.info("4.8 - Nome e senha alterados com sucesso!")
                    return True
                else :
                    logging.info("4.8 - senha não alterada.")
                    return False
            else:
                logging.info("4.7 - Nome do WIFI e SENHA já estão no equipamento")
                return True
            
        except Exception as e:
            logging.info("4.ERROR - Erro ao tentar realizar a troca de senha. Error:"+e)
            return False

        finally:
            _chorme.quit()


def esta_visivel(driver, by, seletor):
    try:
        elemento = driver.find_element(by, seletor)
        return elemento.is_displayed()
    except Exception as e:
        return False