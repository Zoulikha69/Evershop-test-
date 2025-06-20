import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestProduct:
    @pytest.fixture(scope="function")
    def driver(self):
        """Initialise le driver Chrome pour les tests"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def wait_for_element(self, driver, by, value, timeout=10, clickable=False):
        """Attend qu'un élément soit présent et optionnellement cliquable"""
        if clickable:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def login(self, driver):
        """Se connecte à l'interface d'administration"""
        driver.get("http://localhost:3000/admin/login")
        
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        submit_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        
        email_input.send_keys("admin@admin.com")
        password_input.send_keys("admin777")
        submit_button.click()

    def test_product_exists(self, driver):
        """Teste si le produit Monstera Deliciosa existe"""
        # Se connecter
        self.login(driver)
        
        # Aller à la page des produits
        catalog_link = self.wait_for_element(driver, By.XPATH, "//a[contains(text(), 'Catalogue')]", clickable=True)
        catalog_link.click()
        
        products_link = self.wait_for_element(driver, By.XPATH, "//a[contains(text(), 'Produits')]", clickable=True)
        products_link.click()
        
        # Vérifier si le produit existe
        product_name = self.wait_for_element(driver, By.XPATH, "//td[contains(text(), 'Monstera Deliciosa')]")
        assert product_name is not None, "Le produit Monstera Deliciosa n'a pas été trouvé"

    def test_product_details(self, driver):
        """Teste les détails du produit Monstera Deliciosa"""
        # Se connecter
        self.login(driver)
        
        # Aller à la page des produits
        catalog_link = self.wait_for_element(driver, By.XPATH, "//a[contains(text(), 'Catalogue')]", clickable=True)
        catalog_link.click()
        
        products_link = self.wait_for_element(driver, By.XPATH, "//a[contains(text(), 'Produits')]", clickable=True)
        products_link.click()
        
        # Cliquer sur le produit
        product_link = self.wait_for_element(driver, By.XPATH, "//td[contains(text(), 'Monstera Deliciosa')]", clickable=True)
        product_link.click()
        
        # Vérifier les détails du produit
        name_field = self.wait_for_element(driver, By.NAME, "name")
        assert name_field.get_attribute("value") == "Monstera Deliciosa", "Le nom du produit ne correspond pas"
        
        # Vérifier que l'image est présente
        image = self.wait_for_element(driver, By.CSS_SELECTOR, "img.product-image")
        assert image is not None, "L'image du produit n'est pas présente" 