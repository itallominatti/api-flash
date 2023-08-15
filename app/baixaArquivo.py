import glob
import os
from time import sleep
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class ArquivoExcel:
    def __init__(self) -> None:
        self.work_dir = os.getcwd()
        self.excel_path = os.path.join(self.work_dir, "excel")
        # gecko_path = os.path.join(self.work_dir, "firefox_folder")

        options = Options()
        options.headless = True
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", self.excel_path)
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/x-gzip"
        )

        self.driver = webdriver.Firefox(options=options)
        self.nome_arquivo_zip = None

    def acessarPaginaLogar(self, page):
        try:
            self.driver.get(page)
            self.driver.find_element(By.ID, "username").send_keys("ti@propig.com.br")
            self.driver.find_element(By.ID, "password").send_keys("40cfw4VTolUY")
            self.driver.find_element(By.ID, "buttonLogin").click()
            sleep(4)
        except Exception as err:
            self.driver.close()
            return (err, "ocorreu um erro na função acessarPaginaLogar()")

    def acessarPaginaDownloadBaixarZip(self, page, baixar=True):
        try:
            self.driver.get(page)
            sleep(4)
            if baixar:
                self.driver.find_element(By.ID, "buttonPesquisar").click()
            sleep(3)
        except Exception as err:
            self.driver.close()
            return err, "ocorreu um erro na função acessarPaginaDownloadBaixarZip()"

    def retornarArquivoBaixado(self):
        try:
            list_of_files = glob.glob(os.path.join(self.excel_path, "*"))
            latest_file = max(list_of_files, key=os.path.getctime)

            self.driver.close()

            return os.path.basename(latest_file)
        except Exception as err:
            print(err, "ocorreu um erro na função retornarArquivoBaixado()")
            self.driver.close()
            return str(type(err))

    def baixarArquivo(self):
        try:
            self.acessarPaginaLogar(
                "https://phoenix.jall.com.br/FlashPhoenix/pages/_defaultPages/empty-page.xhtml"
            )

            self.acessarPaginaDownloadBaixarZip(
                "https://phoenix.jall.com.br/FlashPhoenix/pages/relatorios/relatorioPicking.xhtml"
            )

            self.nome_arquivo_zip = self.retornarArquivoBaixado()
        except Exception as err:
            self.driver.close()
            return err, "ocorreu um erro na função baixarArquivo()"

    def extrairArquivoZip(self):
        try:
            print("BAIXANDO ARQUIVO")
            self.baixarArquivo()
            zip = self.nome_arquivo_zip
            with ZipFile(f"excel/{zip}", "r") as zip_object:
                zip_object.extractall(path="./excel")

            self.excel = zip_object.namelist()

            return self.excel
        except Exception as err:
            print(err, "ocorreu um erro na função extrairArquivoZip()")
            self.driver.close()
            return str(type(err))

    def removerZip(self):
        excel = self.extrairArquivoZip()
        zip = self.nome_arquivo_zip

        try:
            if os.path.exists(f"./excel/{zip}"):
                os.remove(f"./excel/{zip}")

            else:
                raise OSError(f"o Zip não foi encontrado.")

        except Exception as err:
            if isinstance(err, OSError):
                if os.path.exists(f"./{zip}"):
                    os.remove(f"./{zip}")
                    print("o excel foi removido")
                else:
                    print(f"o Zip não foi removido, erro : {OSError}")
                return

            raise err

        print("ARQUIVO BAIXADO")

        return excel


def extraiArquivo():
    try:
        arquivo = ArquivoExcel()
        return arquivo.removerZip()
    except Exception as err:
        return err, "ocorreu um erro na função extraiArquivo()"


if __name__ == "__main__":
    extraiArquivo()
