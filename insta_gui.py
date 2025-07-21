import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class InstagramBot:
    drive_path = 'C:\\Python_ilk_deneme\\Driverİnsta\\chromedriver'  # kendi driver yolunla değiştir

    def __init__(self, username, password, log_callback=None):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(InstagramBot.drive_path)
        self.log = log_callback  # GUI'den log fonksiyonu
        if self.log:
            self.log("Tarayıcı başlatıldı.")

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        if self.log:
            self.log("Instagram giriş sayfası açıldı.")
        time.sleep(5)
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        if self.log:
            self.log("Giriş bilgileri gönderildi, giriş bekleniyor...")
        time.sleep(5)

    def getFollowers(self):
        if self.log:
            self.log(f"{self.username} profil sayfasına gidiliyor...")
        self.browser.get(f"https://www.instagram.com/{self.username}/")
        time.sleep(3)

        # Takipçilere tıklama
        followers_link = self.browser.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_link.click()
        if self.log:
            self.log("Takipçi penceresi açıldı, takipçiler çekiliyor...")
        time.sleep(3)

        # Takipçi popup'ı içindeki takipçi isimlerini çek
        followers_popup = self.browser.find_element(By.XPATH, "//div[@role='dialog']//ul/div")
        followers = set()
        last_height = 0
        scroll_box = followers_popup

        # Takipçileri tam çekmek için scroll yapabiliriz, basit örnek için birkaç kere scroll
        for _ in range(5):
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
            time.sleep(2)
            users = scroll_box.find_elements(By.TAG_NAME, "li")
            for user in users:
                try:
                    username = user.find_element(By.TAG_NAME, "a").text
                    followers.add(username)
                except:
                    pass

        if self.log:
            self.log(f"Toplam {len(followers)} takipçi bulundu.")

        return followers

    def __del__(self):
        if self.log:
            self.log("Tarayıcı kapanıyor...")
        time.sleep(5)
        self.browser.quit()


def start_bot():
    user = entry_user.get()
    pwd = entry_pass.get()
    if not user or not pwd:
        messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz.")
        return

    def log_to_gui(msg):
        txt_log.configure(state='normal')
        txt_log.insert(tk.END, msg + "\n")
        txt_log.see(tk.END)
        txt_log.configure(state='disabled')

    try:
        bot = InstagramBot(user, pwd, log_callback=log_to_gui)
        bot.signIn()
        followers = bot.getFollowers()
        log_to_gui("Takipçiler listelendi:")
        for f in followers:
            log_to_gui(f" - {f}")
        messagebox.showinfo("Başarılı", f"{len(followers)} takipçi listelendi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Giriş yapılamadı veya takipçiler alınamadı: {e}")


# Tkinter GUI
root = tk.Tk()
root.title("Instagram Giriş Botu")

tk.Label(root, text="Kullanıcı Adı:").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Şifre:").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Giriş Yap ve Takipçileri Listele", command=start_bot).pack(pady=10)

# Log kutusu (scrolledtext)
txt_log = scrolledtext.ScrolledText(root, width=50, height=15, state='disabled')
txt_log.pack(pady=10)

root.mainloop()
