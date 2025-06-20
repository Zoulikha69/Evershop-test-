import os
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestCategoryCreation:
    def wait_for_element(self, driver, by, value, clickable=False, timeout=10):
        if clickable:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def login_to_admin(self, driver):
        print("\n=== Connexion à l'admin ===")
        driver.get("http://localhost:3000/admin/login")
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        email_input.clear()
        email_input.send_keys("admin@admin.com")
        password_input.clear()
        password_input.send_keys("admin777")
        login_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        login_button.click()
        # Vérifier la connexion
        self.wait_for_element(driver, By.CSS_SELECTOR, "h1.page-heading-title")
        print("✓ Connexion réussie !")

    @pytest.fixture
    def driver(self):
        options = Options()
        options.add_argument('--no-sandbox')  # ← désactive la sandbox
        # options.add_argument('--headless=new')  # Désactivé pour voir la fenêtre
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 1024)
        yield driver
        print("\n=== Pause pour observer la fenêtre ===")
        time.sleep(10)  # Pause de 10 secondes pour observer la grande  fenêtre
        print("\n=== Fermeture du navigateur ===")
        driver.quit()

    def test_create_category(self, driver):
        self.login_to_admin(driver)

        print("\n=== Navigation vers la page des catégories ===")
        driver.get("http://localhost:3000/admin/categories")
        self.wait_for_element(driver, By.CSS_SELECTOR, "a.button.primary")

        print("\nClic sur 'New Category'...")
        new_category_btn = driver.find_element(By.CSS_SELECTOR, "a.button.primary")
        new_category_btn.click()

        print("\nRemplissage du formulaire de catégorie...")
        name_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#name")
        url_key_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#urlKey")
        unique_name = f"Catégorie Test {random.randint(10000, 99999)}"
        unique_url_key = f"categorie-test-{random.randint(10000, 99999)}"
        name_input.send_keys(unique_name)
        url_key_input.send_keys(unique_url_key)
        print(f"Nom: {unique_name} | URL Key: {unique_url_key}")

        print("\nClic sur Save...")
        save_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button.button.primary", clickable=True)
        save_button.click()

        print("\nVérification du toast de confirmation...")
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "div.Toastify__toast-body")
            )
            toast = driver.find_element(By.CSS_SELECTOR, "div.Toastify__toast-body")
            WebDriverWait(driver, 5).until(
                lambda d: "Category saved successfully!" in toast.text and toast.text.strip() != ""
            )
            print(f"✓ Toast affiché : '{toast.text}'")
        except TimeoutException:
            print(f"✗ Toast non conforme ou absent !")
            raise

        print("\nVérification de la sauvegarde...")
        self.wait_for_element(driver, By.CSS_SELECTOR, "h1.page-heading-title")
        print("✓ Catégorie créée avec succès !")

        # Suppression temporaire de la catégorie créée pour test (logique identique à test produit)
        print("\n=== Suppression de la catégorie créée ===")
        driver.get("http://localhost:3000/admin/categories")
        self.wait_for_element(driver, By.CSS_SELECTOR, "table")
        try:
            print(f"Recherche de la catégorie avec le nom: {unique_name}")
            # Trouver la ligne contenant le nom unique dans un <a>
            row = driver.find_element(By.XPATH, f"//table//tr[td//a[text()='{unique_name}']]")
            print("✓ Catégorie trouvée dans le tableau")

            print("Recherche de la case à cocher...")
            # Cocher la case dans la première colonne
            checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            driver.execute_script("arguments[0].click();", checkbox)
            print("✓ Case cochée via JavaScript")

            print("Recherche du lien Delete dans la barre d'action...")
            action_delete_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[span[text()='Delete']]"))
            )
            print("✓ Lien Delete trouvé, clic...")
            action_delete_link.click()

            print("Recherche du bouton de confirmation Delete...")
            confirm_delete_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.critical"))
            )
            print("✓ Bouton de confirmation trouvé, clic...")
            driver.execute_script("arguments[0].click();", confirm_delete_button)
            print("✓ Clic JS sur le bouton de confirmation Delete")

            # Vérifier que la catégorie a bien été supprimée
            print("\nVérification de la suppression...")
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, f"//table//tr[td//a[text()='{unique_name}']]") )
            )
            print("✓ Catégorie supprimée avec succès!")
        except Exception as e:
            print(f"✗ Impossible de supprimer la catégorie (nom: {unique_name}) : {str(e)}")
            print(driver.page_source)
            raise 