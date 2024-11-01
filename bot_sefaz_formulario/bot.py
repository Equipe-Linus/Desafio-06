import requests
from botcity.web import WebBot, Browser, By
from botcity.maestro import *

# Desativa erros caso o BotCity Maestro não esteja conectado
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Chave da API do 2Captcha


# Classe que herda de WebBot para adicionar funcionalidades específicas
class BotSefaz(WebBot):
    def __init__(self):
        super().__init__()
        self.headless = False
        self.browser = Browser.CHROME
        self.driver_path = r"resources\chromedriver.exe"

    # Função para resolver o CAPTCHA com 2Captcha
    def solucionando_captcha(self, imagem):
        with open(imagem, "rb") as arquivo:
            resposta = requests.post("http://2captcha.com/in.php", data={
                'key': chave,
                'method': 'post',
                'json': 1
            }, files={'file': arquivo})

        identificador = resposta.json().get('request')
        solucao = None
        while True:
            resultado = requests.get(f"http://2captcha.com/res.php?key={chave}&action=get&id={identificador}&json=1")
            if resultado.json().get('status') == 1:
                solucao = resultado.json().get('request')
                break
            print("Solucionando captcha...")
            self.wait(3000)

        return solucao

# Função principal do bot
def main():
    ############################ iniciando try ########################################################
    try:
        # Configuração do Maestro e obtenção dos parâmetros da tarefa
        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()
        
        print(f"Task ID: {execution.task_id}")
        print(f"Task Parameters: {execution.parameters}")
        
        # Instancia a classe derivada BotSefaz
        bot = BotSefaz()
        
        # Notifando um pequeno exemplo de alerta 
        '''exemplo'''
        maestro.alert(
            task_id=execution.task_id,
            title="BotSefaz - Inicio",
            message="Estamos iniciando o processo de automação do Desafio 06",
            alert_type=AlertType.INFO
        )
        
        # Acessa o portal do governo
        bot.browse("https://sistemas1.sefaz.ma.gov.br/portalsefaz/jsp/principal/principal.jsf")
        bot.sleep(3000)
        
#         # procura o botao fechar
#         while len(bot.find_elements('//*[@id="form:mdAvisos"]/div[3]/a', By.XPATH)) < 1:
#             bot.wait(2000)
#             print('carregando....')
            
#         # Procurando um elemento por ID e clica.
#         btn = bot.find_element(selector='//*[@id="form:mdAvisos"]/div[3]/a', by=By.XPATH)
        
# ###################### LOGS ######################################

#         if btn:  # Verifica se o botão foi encontrado
#             btn.click()  # Clica no botão
            
#             # Log de sucesso ao encontrar e clicar no botão
#             maestro.new_log_entry(
#                 activity_label="SucessoCliqueBotao",
#                 values={
#                     "status": "SUCESSO"
#                 }
#             )
#         else:
#             # Log de erro se o botão não foi encontrado
#             maestro.new_log_entry(
#                 activity_label="ErroCliqueBotao",
#                 values={
#                     "status": "ERRO"
#                 }
#             )
###################### FIM LOGS ######################################       
        # Navegação para o formulário de download de XML
        bot.find_element("/html/body/div[2]/div/form/div[2]/div[2]/div[1]/div/div[1]/a[2]", by=By.XPATH).click()
        bot.find_element("/html/body/div[2]/div/form/div/ul/li[4]/a", by=By.XPATH).click()
        bot.find_element("/html/body/div[2]/div/form/div/div[2]/div/span[1]/span/div/ul/li[6]/a", by=By.XPATH).click()
        
        # Acessa o iframe e preenche o formulário
        iframe = bot.find_element('/html/frameset/frame', By.XPATH)
        bot.enter_iframe(iframe)

        bot.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[1]/td[2]/input', By.XPATH)
        bot.paste('00002222')
        bot.tab()
        bot.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[2]/td[2]/input', By.XPATH)
        bot.paste('55550000')
        bot.tab()
        bot.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[3]/td[2]/input', By.XPATH)
        bot.paste('00000000')
        bot.tab()
        bot.tab()

        # Define e insere as datas
        data_inicial = '20/10/2024'
        bot.execute_javascript(f"""
            var campo = document.evaluate('//*[@id="form1:dtIniInputDate"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            campo.value = '{data_inicial}';
            campo.dispatchEvent(new Event('input'));
            campo.dispatchEvent(new Event('change'));
        """)
        bot.sleep(2000)

        data_final = '31/10/2024'
        bot.execute_javascript(f"""
            var campo = document.evaluate('//*[@id="form1:dtFinInputDate"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            campo.value = '{data_final}';
            campo.dispatchEvent(new Event('input'));
            campo.dispatchEvent(new Event('change'));
        """)

        # Captura e solução do CAPTCHA
        captcha = bot.find_element('//*[@id="form1:captcha"]', By.XPATH)
        captcha.screenshot("captcha.png")  # Salva o CAPTCHA como 'captcha.png'
        bot.find_element('//*[@class="senha"]', By.XPATH).click()
        bot.wait(5000)

        captcha_resolvido = bot.solucionando_captcha("captcha.png")
        print(f"CAPTCHA resolvido: {captcha_resolvido}")
        
        # Insere a solução do CAPTCHA no campo
        bot.find_element('//*[@class="senha"]', By.XPATH).send_keys(captcha_resolvido)
        bot.wait(5000)
        
        # clica no botao BaixaXML
        btn_baixar = bot.find_element(selector='//*[@id="form1:j_id6_body"]/table[4]/tbody/tr/td[2]/input', by=By.XPATH)
        btn_baixar.click()
            
        # Limpeza e finalização do navegador
        bot.find_element('//*[@id="form1:j_id6_body"]/table[4]/tbody/tr/td[1]/input', By.XPATH).click()
        bot.wait(10000)
        
        status = AutomationTaskFinishStatus.SUCCESS
        mensagem = "Tarefa BotSefaz finalizada com sucesso"
    
###########################FIM TRY########################################

########################## INICIO EXCEPT  ################################  
    except Exception as ex:
        # Salvando captura de tela do erro
        bot.save_screenshot("erro.png")

        # Registrando o erro
        maestro.error(
            task_id=execution.task_id,
            exception=ex,
            screenshot="erro.png"
        )
        
        status = AutomationTaskFinishStatus.FAILED
        mensagem = "Tarefa BotSefaz finalizada com erro"
########################## FIM EXCEPT  ################################

    finally:
        # Wait 3 seconds before closing
        bot.wait(3000)

        # Finish and clean up the Web Browser
        # You MUST invoke the stop_browser to avoid
        # leaving instances of the webdriver open
        bot.stop_browser()

        # Uncomment to mark this task as finished on BotMaestro
        #se ele definiu tudo com sucesso, resultado sucesso
        maestro.finish_task(
            task_id=execution.task_id,
            status=status,
            message=mensagem
        )
        #fim finally

# Função para lidar com elementos não encontrados
def not_found(label):
    print(f"Elemento não encontrado: {label}")

if __name__ == '__main__':
    main()
