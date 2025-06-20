import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
import logging
import random

# Configuration du logging pour supprimer les messages de Selenium
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

class TestProductCreation:
    @pytest.fixture(scope="function")
    def driver(self):
        """Initialise le driver Chrome pour les tests"""
        print("\n=== Initialisation du navigateur ===")
        options = webdriver.ChromeOptions()
        # Options de base
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        # Options pour supprimer les messages d'erreur
        options.add_argument('--log-level=3')  # Supprime les logs de Chrome
        options.add_argument('--silent')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Supprime les logs de DevTools
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # Supprime le message "Chrome is being controlled by automated software"
        
        # Désactive complètement le GPU et ses logs
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument('--disable-gpu-compositing')
        options.add_argument('--disable-gpu-rasterization')
        options.add_argument('--disable-gpu-driver-bug-workarounds')
        options.add_argument('--disable-gpu-program-cache')
        options.add_argument('--disable-gpu-shader-disk-cache')
        options.add_argument('--disable-gpu-vsync')
        options.add_argument('--disable-gpu-memory-buffer-compositor-resources')
        options.add_argument('--disable-gpu-memory-buffer-video-frames')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-2')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-3')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-4')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-5')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-6')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-7')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-8')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-9')
        options.add_argument('--disable-gpu-memory-buffer-video-frames-10')
        
        # Désactive les notifications
        options.add_argument('--disable-notifications')
        
        # Désactive les extensions
        options.add_argument('--disable-extensions')
        
        # Désactive les popups
        options.add_argument('--disable-popup-blocking')
        
        # Désactive les infobulles
        options.add_argument('--disable-infobars')
        
        # Désactive les logs de DevTools
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        yield driver
        print("\n=== Fermeture du navigateur ===")
        driver.quit()

    def wait_for_element(self, driver, by, value, timeout=10, clickable=False):
        """Attend qu'un élément soit présent et optionnellement cliquable"""
        try:
            print(f"\nRecherche de l'élément: {by}={value}")
            if clickable:
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
            else:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            print(f"✓ Élément trouvé: {by}={value}")
            return element
        except TimeoutException:
            print(f"✗ Élément non trouvé: {by}={value}")
            print(f"URL actuelle: {driver.current_url}")
            print("Source de la page:")
            print(driver.page_source[:1000])  # Affiche les 1000 premiers caractères
            raise

    def login_to_admin(self, driver):
        """Connexion à l'interface admin"""
        print("\n=== Début de la connexion admin ===")
        driver.get("http://localhost:3000/admin/login")
        print(f"URL de connexion: {driver.current_url}")
        
        # Vérification de la présence des éléments de connexion
        print("\nVérification des champs de connexion...")
        email_input = self.wait_for_element(driver, By.NAME, "email")
        password_input = self.wait_for_element(driver, By.NAME, "password")
        submit_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']", clickable=True)
        
        print("\nSaisie des identifiants...")
        email_input.send_keys("admin@admin.com")
        password_input.send_keys("admin777")
        print("Clic sur le bouton de connexion...")
        submit_button.click()
        
        # Vérification de la connexion réussie
        print("\nVérification de la connexion...")
        self.wait_for_element(driver, By.CSS_SELECTOR, "h1.page-heading-title")
        print("✓ Connexion admin réussie!")

    def test_create_product(self, driver):
        """Test de création d'un nouveau produit"""
        # Connexion à l'interface admin
        self.login_to_admin(driver)
        
        # Navigation vers la page de création de produit
        print("\n=== Navigation vers la page de création de produit ===")
        driver.get("http://localhost:3000/admin/products/new")
        print(f"URL de création de produit: {driver.current_url}")
        
        # Remplir le formulaire avec les données du produit
        print("\n=== Remplissage du formulaire ===")
        
        print("\nChamp nom...")
        name_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#name")
        name_input.send_keys("monstera deliciosa")
        print(f"Valeur saisie: {name_input.get_attribute('value')}")
        
        print("\nChamp SKU...")
        sku_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#sku")
        unique_sku = f"sku{random.randint(10000, 99999)}"
        sku_input.send_keys(unique_sku)
        print(f"Valeur saisie: {sku_input.get_attribute('value')}")
        
        print("\nChamp prix...")
        price_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#price")
        price_input.send_keys("30")
        print(f"Valeur saisie: {price_input.get_attribute('value')}")
        
        print("\nChamp URL key...")
        url_key_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#urlKey")
        unique_url_key = f"plante{random.randint(10000, 99999)}"
        url_key_input.send_keys(unique_url_key)  # URL sans espace
        print(f"Valeur saisie: {url_key_input.get_attribute('value')}")
        
        print("\nChamp quantité...")
        qty_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#qty")
        qty_input.send_keys("10")
        print(f"Valeur saisie: {qty_input.get_attribute('value')}")
        
        print("\nChamp poids...")
        weight_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input#weight")
        weight_input.send_keys("1.5")  # Poids en kg
        print(f"Valeur saisie: {weight_input.get_attribute('value')}")
        
        # Uploader une image
        print("\n=== Upload de l'image ===")
        image_input = self.wait_for_element(driver, By.CSS_SELECTOR, "input[type='file']")
        image_path = os.path.abspath("images/monstera.jpg")
        print(f"Chemin de l'image: {image_path}")
        print(f"L'image existe: {os.path.exists(image_path)}")
        image_input.send_keys(image_path)
        
        # Cliquer sur le bouton Save
        print("\n=== Sauvegarde du produit ===")
        save_button = self.wait_for_element(driver, By.CSS_SELECTOR, "button.button.primary", clickable=True)
        print("Clic sur le bouton Save...")
        save_button.click()

        # Vérification du toast de confirmation
        print("\nVérification du toast de confirmation...")
        try:
            # Étape 1 : attendre la présence du toast dans le DOM
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "div.Toastify__toast-body")
            )
            toast = driver.find_element(By.CSS_SELECTOR, "div.Toastify__toast-body")
            # Étape 2 : attendre que le texte du toast soit non vide et contienne le message attendu
            WebDriverWait(driver, 5).until(
                lambda d: "Product saved successfully!" in toast.text and toast.text.strip() != ""
            )
            print(f"✓ Toast de confirmation affiché : '{toast.text}'")
        except TimeoutException:
            print(f"✗ Toast trouvé mais texte non conforme ou vide ! Texte actuel : '{toast.text if 'toast' in locals() else ''}'")
            raise

        # Vérification de la sauvegarde (présence du titre)
        print("\nVérification de la sauvegarde...")
        self.wait_for_element(driver, By.CSS_SELECTOR, "h1.page-heading-title")
        print("✓ Produit créé avec succès!")

        # Suppression du produit créé
        print("\n=== Suppression du produit créé ===")
        print(f"Navigation vers la page des produits...")
        driver.get("http://localhost:3000/admin/products")
        print("Attente du chargement du tableau...")
        self.wait_for_element(driver, By.CSS_SELECTOR, "table")
        try:
            print(f"\nRecherche du produit avec le SKU: {unique_sku}")
            # Trouver la ligne contenant le SKU unique
            row = driver.find_element(By.XPATH, f"//table//tr[td[text()='{unique_sku}']]")
            print("✓ Produit trouvé dans le tableau")

            print("\nRecherche de la case à cocher...")
            # Cocher la case dans la première colonne
            checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            print("✓ Case à cocher trouvée")
            # Utiliser JavaScript pour cliquer sur la case à cocher
            driver.execute_script("arguments[0].click();", checkbox)
            print("✓ Case à cocher cochée via JavaScript")

            print("\nRecherche du lien Delete dans la barre d'action...")
            # Attendre que le lien Delete apparaisse dans la barre d'action
            action_delete_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[span[text()='Delete']]"))
            )
            print("✓ Lien Delete trouvé, clic...")
            action_delete_link.click()

            print("\nRecherche du bouton de confirmation Delete...")
            # Attendre le bouton de confirmation (modal)
            confirm_delete_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.critical"))
            )
            print("✓ Bouton de confirmation trouvé, clic...")
            # Utiliser JavaScript pour cliquer sur le bouton Delete (modale)
            driver.execute_script("arguments[0].click();", confirm_delete_button)
            print("✓ Clic JS sur le bouton de confirmation Delete")

            # Vérifier que le produit a bien été supprimé
            print("\nVérification de la suppression...")
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, f"//table//tr[td[text()='{unique_sku}']]"))
            )
            print("✓ Produit supprimé avec succès!")

        except Exception as e:
            print(f"✗ Impossible de supprimer le produit (SKU: {unique_sku}) : {str(e)}")
            print("\nÉtat actuel de la page :")
            print(driver.page_source)
            raise

if __name__ == "__main__":
    pytest.main([__file__]) 