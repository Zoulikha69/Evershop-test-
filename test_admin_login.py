import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestAdminLogin:
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


    def is_login_url(self, driver):
        """Vérifie si l'URL actuelle est celle de la page de login"""
        return "login" in driver.current_url.lower()

    def test_successful_login(self, driver):
        """Test de connexion réussie avec les identifiants valides"""
        # Accès à la page de connexion
        driver.get("http://localhost:3000/admin/login")
        assert self.is_login_url(driver), "La page de connexion n'est pas chargée"

        # Remplissage du formulaire
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        submit_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        
        email_input.send_keys("admin@admin.com")
        password_input.send_keys("admin777")
        submit_button.click()
        
        # Vérification du titre Dashboard
        heading = self.wait_for_element(driver, By.CSS_SELECTOR, "h1.page-heading-title")
        assert "Dashboard" in heading.text or "Tableau de bord" in heading.text, f"Titre inattendu après login: {heading.text}"

    def test_failed_login(self, driver):
        """Test de connexion échouée avec des identifiants invalides"""
        # Accès à la page de connexion
        driver.get("http://localhost:3000/admin/login")
        
        # Remplissage du formulaire avec des identifiants invalides
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        submit_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        
        email_input.send_keys("invalid@mail.com")
        password_input.send_keys("wrongpassword")
        submit_button.click()
        
        # Vérification que nous sommes toujours sur la page de login
        assert self.is_login_url(driver), "La page a été redirigée alors qu'elle ne devrait pas l'être"
        
        # Vérification du message d'erreur (toast ou message sous le formulaire)
        try:
            # Toastify ou message d'erreur classique
            error = self.wait_for_element(driver, By.CSS_SELECTOR, "div.Toastify__toast-body, .error-message, .alert-danger, .text-critical", timeout=5)
            assert error.text.strip() != "", "Invalid email or password"
            print(f"Message d'erreur affiché : {error.text}")
        except TimeoutException:
            raise AssertionError("Aucun message d'erreur affiché après un login échoué")
        
        # Vérification que les champs sont vides (optionnel, dépend du comportement de l'UI)
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        
        