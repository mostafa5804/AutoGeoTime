import os
import sys
import time
import threading
import subprocess
import winreg
import ctypes
from ctypes import wintypes
import tkinter as tk
import requests
import pystray
from PIL import Image, ImageDraw

# نگاشت جامع مناطق زمانی IANA به فرمت استاندارد ویندوز
IANA_TO_WINDOWS_TZ = {
    "America/New_York": "Eastern Standard Time",
    "America/Detroit": "Eastern Standard Time",
    "America/Toronto": "Eastern Standard Time",
    "America/Montreal": "Eastern Standard Time",
    "America/Indiana/Indianapolis": "US Eastern Standard Time",
    "America/Chicago": "Central Standard Time",
    "America/Winnipeg": "Central Standard Time",
    "America/Mexico_City": "Central Standard Time (Mexico)",
    "America/Denver": "Mountain Standard Time",
    "America/Edmonton": "Mountain Standard Time",
    "America/Phoenix": "US Mountain Standard Time",
    "America/Los_Angeles": "Pacific Standard Time",
    "America/Vancouver": "Pacific Standard Time",
    "America/Anchorage": "Alaskan Standard Time",
    "Pacific/Honolulu": "Hawaiian Standard Time",
    "America/Halifax": "Atlantic Standard Time",
    "America/St_Johns": "Newfoundland Standard Time",
    "America/Sao_Paulo": "E. South America Standard Time",
    "America/Argentina/Buenos_Aires": "Argentina Standard Time",
    "America/Santiago": "Pacific SA Standard Time",
    "America/Bogota": "SA Pacific Standard Time",
    "America/Lima": "SA Pacific Standard Time",
    "America/Caracas": "Venezuela Standard Time",
    "Europe/London": "GMT Standard Time",
    "Europe/Dublin": "GMT Standard Time",
    "Europe/Lisbon": "GMT Standard Time",
    "Atlantic/Reykjavik": "Greenwich Standard Time",
    "Europe/Amsterdam": "W. Europe Standard Time",
    "Europe/Berlin": "W. Europe Standard Time",
    "Europe/Rome": "W. Europe Standard Time",
    "Europe/Stockholm": "W. Europe Standard Time",
    "Europe/Vienna": "W. Europe Standard Time",
    "Europe/Zurich": "W. Europe Standard Time",
    "Europe/Oslo": "W. Europe Standard Time",
    "Europe/Copenhagen": "Romance Standard Time",
    "Europe/Brussels": "Romance Standard Time",
    "Europe/Madrid": "Romance Standard Time",
    "Europe/Paris": "Romance Standard Time",
    "Europe/Warsaw": "Central European Standard Time",
    "Europe/Prague": "Central European Standard Time",
    "Europe/Budapest": "Central European Standard Time",
    "Europe/Belgrade": "Central European Standard Time",
    "Europe/Zagreb": "Central European Standard Time",
    "Europe/Athens": "GTB Standard Time",
    "Europe/Bucharest": "GTB Standard Time",
    "Europe/Sofia": "FLE Standard Time",
    "Europe/Helsinki": "FLE Standard Time",
    "Europe/Kiev": "FLE Standard Time",
    "Europe/Kyiv": "FLE Standard Time",
    "Europe/Riga": "FLE Standard Time",
    "Europe/Tallinn": "FLE Standard Time",
    "Europe/Vilnius": "FLE Standard Time",
    "Europe/Istanbul": "Turkey Standard Time",
    "Europe/Moscow": "Russian Standard Time",
    "Europe/Minsk": "Belarus Standard Time",
    "Asia/Tbilisi": "Georgian Standard Time",
    "Asia/Yerevan": "Caucasus Standard Time",
    "Asia/Baku": "Azerbaijan Standard Time",
    "Asia/Tehran": "Iran Standard Time",
    "Asia/Dubai": "Arabian Standard Time",
    "Asia/Muscat": "Arabian Standard Time",
    "Asia/Riyadh": "Arabian Standard Time",
    "Asia/Kuwait": "Arabian Standard Time",
    "Asia/Qatar": "Arabian Standard Time",
    "Asia/Bahrain": "Arabian Standard Time",
    "Asia/Baghdad": "Arabic Standard Time",
    "Asia/Amman": "Jordan Standard Time",
    "Asia/Beirut": "Middle East Standard Time",
    "Asia/Jerusalem": "Israel Standard Time",
    "Africa/Cairo": "Egypt Standard Time",
    "Africa/Johannesburg": "South Africa Standard Time",
    "Africa/Casablanca": "Morocco Standard Time",
    "Africa/Lagos": "W. Central Africa Standard Time",
    "Africa/Nairobi": "E. Africa Standard Time",
    "Asia/Kabul": "Afghanistan Standard Time",
    "Asia/Karachi": "Pakistan Standard Time",
    "Asia/Tashkent": "West Asia Standard Time",
    "Asia/Almaty": "Central Asia Standard Time",
    "Asia/Kolkata": "India Standard Time",
    "Asia/Colombo": "Sri Lanka Standard Time",
    "Asia/Kathmandu": "Nepal Standard Time",
    "Asia/Dhaka": "Bangladesh Standard Time",
    "Asia/Bangkok": "SE Asia Standard Time",
    "Asia/Jakarta": "SE Asia Standard Time",
    "Asia/Ho_Chi_Minh": "SE Asia Standard Time",
    "Asia/Singapore": "Singapore Standard Time",
    "Asia/Kuala_Lumpur": "Singapore Standard Time",
    "Asia/Manila": "Singapore Standard Time",
    "Asia/Shanghai": "China Standard Time",
    "Asia/Hong_Kong": "China Standard Time",
    "Asia/Taipei": "Taipei Standard Time",
    "Asia/Seoul": "Korea Standard Time",
    "Asia/Tokyo": "Tokyo Standard Time",
    "Australia/Perth": "W. Australia Standard Time",
    "Australia/Adelaide": "Cen. Australia Standard Time",
    "Australia/Darwin": "AUS Central Standard Time",
    "Australia/Brisbane": "E. Australia Standard Time",
    "Australia/Sydney": "AUS Eastern Standard Time",
    "Australia/Melbourne": "AUS Eastern Standard Time",
    "Pacific/Auckland": "New Zealand Standard Time",
}

# نگاشت کامل کدهای GeoID ویندوز
COUNTRY_TO_GEOID = {
    "AF": 3, "AL": 6, "DZ": 4, "AR": 11, "AM": 7, "AU": 12, "AT": 14, "AZ": 5,
    "BH": 17, "BD": 23, "BY": 29, "BE": 21, "BR": 32, "BG": 35, "KH": 40, "CA": 39,
    "CL": 46, "CN": 45, "CO": 51, "CR": 54, "HR": 108, "CY": 59, "CZ": 75, "DK": 61,
    "EC": 66, "EG": 67, "EE": 70, "FI": 77, "FR": 84, "GE": 88, "DE": 94, "GR": 98,
    "HK": 104, "HU": 109, "IS": 110, "IN": 113, "ID": 111, "IR": 116, "IQ": 121,
    "IE": 68, "IL": 117, "IT": 118, "JP": 122, "JO": 126, "KZ": 137, "KE": 129,
    "KR": 134, "KW": 136, "LV": 140, "LB": 139, "LT": 141, "LU": 147, "MY": 167,
    "MX": 166, "MD": 152, "MN": 154, "MA": 159, "NP": 178, "NL": 176, "NZ": 183,
    "NG": 175, "NO": 177, "OM": 164, "PK": 190, "PA": 192, "PE": 187, "PH": 201,
    "PL": 191, "PT": 193, "QA": 197, "RO": 200, "RU": 203, "SA": 205, "RS": 271,
    "SG": 215, "SK": 143, "SI": 212, "ZA": 209, "ES": 217, "LK": 42, "SE": 221,
    "CH": 223, "TW": 237, "TH": 227, "TR": 235, "UA": 241, "AE": 224, "GB": 242,
    "US": 244, "UY": 246, "UZ": 247, "VE": 249, "VN": 251
}

# نگاشت کد کشور به Regional Format استاندارد ویندوز (LocaleName)
COUNTRY_TO_LOCALE = {
    "US": "en-US", "GB": "en-GB", "CA": "en-CA", "AU": "en-AU", "NZ": "en-NZ",
    "NL": "nl-NL", "DE": "de-DE", "AT": "de-AT", "CH": "de-CH", "FR": "fr-FR",
    "BE": "nl-BE", "ES": "es-ES", "IT": "it-IT", "PT": "pt-PT", "BR": "pt-BR",
    "SE": "sv-SE", "NO": "nb-NO", "DK": "da-DK", "FI": "fi-FI", "PL": "pl-PL",
    "CZ": "cs-CZ", "HU": "hu-HU", "RO": "ro-RO", "GR": "el-GR", "TR": "tr-TR",
    "RU": "ru-RU", "UA": "uk-UA", "AE": "ar-AE", "SA": "ar-SA", "QA": "ar-QA",
    "KW": "ar-KW", "BH": "ar-BH", "OM": "ar-OM", "IQ": "ar-IQ", "EG": "ar-EG",
    "IR": "fa-IR", "AF": "fa-AF", "JP": "ja-JP", "KR": "ko-KR", "CN": "zh-CN",
    "TW": "zh-TW", "HK": "zh-HK", "SG": "en-SG", "IN": "en-IN", "MY": "ms-MY",
    "TH": "th-TH", "VN": "vi-VN", "ID": "id-ID", "IL": "he-IL", "GE": "ka-GE",
    "AM": "hy-AM", "AZ": "az-Latn-AZ"
}

APP_NAME = "AutoGeoTime"
MUTEX_NAME = "Local\\AutoGeoTime_SingleInstance_Mutex"
SHOW_EVENT_NAME = "Local\\AutoGeoTime_ShowFlyout_Event"
FONT_MAIN = "Segoe UI"


def check_single_instance():
    """جلوگیری از اجرای همزمان چند نسخه و باز کردن پنل نسخه قبلی"""
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    last_error = kernel32.GetLastError()
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        event = kernel32.OpenEventW(0x0002, False, SHOW_EVENT_NAME)  # EVENT_MODIFY_STATE
        if event:
            kernel32.SetEvent(event)
            kernel32.CloseHandle(event)
        sys.exit(0)
    return mutex


def get_resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_bundled_fonts():
    global FONT_MAIN
    FR_PRIVATE = 0x10
    loaded_any = False
    for font_file in ("Vazirmatn-Regular.ttf", "Vazirmatn-Bold.ttf"):
        font_path = get_resource_path(font_file)
        if os.path.exists(font_path):
            if ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0) > 0:
                loaded_any = True
    if loaded_any:
        FONT_MAIN = "Vazirmatn"


def broadcast_windows_time_update():
    """ارسال سیگنال سیستمی برای آپدیت فوری ساعت Taskbar بدون تأخیر"""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    WM_TIMECHANGE = 0x001E
    SMTO_ABORTIFHUNG = 0x0002
    user32 = ctypes.windll.user32
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_TIMECHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, None)
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "intl", SMTO_ABORTIFHUNG, 1000, None)


def render_app_icon(state="active", size=128):
    """آیکون گرافیکی: سبز (متصل/فعال)، قرمز (قطع/متوقف)، آبی (در حال تغییر)"""
    colors = {
        "active": (16, 185, 129, 255),   # #10B981 سبز
        "paused": (239, 68, 68, 255),    # #EF4444 قرمز
        "syncing": (59, 130, 246, 255),  # #3B82F6 آبی
    }
    bg = colors.get(state, colors["active"])
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = int(size * 0.25)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=bg)

    pad = int(size * 0.18)
    stroke_w = max(2, int(size * 0.065))
    draw.ellipse((pad, pad, size - pad, size - pad), outline=(255, 255, 255, 245), width=stroke_w)

    cx, cy = size // 2, size // 2
    if state == "paused":
        # علامت قطع (ضربدر ظریف داخل حلقه)
        d = int(size * 0.13)
        draw.line((cx - d, cy - d, cx + d, cy + d), fill="white", width=stroke_w)
        draw.line((cx + d, cy - d, cx - d, cy + d), fill="white", width=stroke_w)
    else:
        # عقربه‌های ساعت
        draw.line((cx, cy, cx, int(size * 0.30)), fill="white", width=stroke_w)
        draw.line((cx, cy, int(size * 0.66), int(size * 0.56)), fill="white", width=stroke_w)

    return img


def ensure_ico_file():
    if getattr(sys, "frozen", False):
        return
    ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")
    if not os.path.exists(ico_path):
        icon_img = render_app_icon("active", 256)
        icon_img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, initial=True, command=None, bg_color="#FFFFFF"):
        super().__init__(parent, width=38, height=20, bg=bg_color, highlightthickness=0, cursor="hand2")
        self.state = initial
        self.command = command
        self.bind("<Button-1>", self.toggle)
        self.draw()

    def draw(self):
        self.delete("all")
        track_color = "#10B981" if self.state else "#CBD5E1"
        self.create_oval(1, 1, 19, 19, fill=track_color, outline=track_color)
        self.create_oval(19, 1, 37, 19, fill=track_color, outline=track_color)
        self.create_rectangle(10, 1, 28, 19, fill=track_color, outline=track_color)
        knob_x = 20 if self.state else 3
        self.create_oval(knob_x, 3, knob_x + 14, 17, fill="#FFFFFF", outline="")

    def toggle(self, event=None):
        self.state = not self.state
        self.draw()
        if self.command:
            self.command(self.state)


class AutoGeoTimeFlyout:
    def __init__(self, root):
        self.root = root
        self.win_width = 320
        self.win_height = 420

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#CBD5E1")

        self.is_monitoring = True
        self.sync_locale_enabled = True
        self.last_ip = None
        self.current_ip = "در حال بررسی..."
        self.current_location_text = "---"
        self.current_tz = "---"
        self.tray_icon = None
        self.is_visible = True
        self.wake_event = threading.Event()

        self.build_ui()
        self.position_near_clock()
        self.root.bind("<FocusOut>", self.on_focus_out)

        # تردهای پس‌زمینه: پایش IP، رصد آداپتور شبکه و گوش دادن به سیگنال Single Instance
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        threading.Thread(target=self.network_route_watcher, daemon=True).start()
        threading.Thread(target=self.single_instance_listener, daemon=True).start()
        threading.Thread(target=self.setup_tray, daemon=True).start()

        if "--minimized" in sys.argv:
            self.root.after(50, self.hide_flyout)
        else:
            self.root.after(100, self.root.focus_force)

    def position_near_clock(self):
        SPI_GETWORKAREA = 0x0030
        rect = wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
        x = rect.right - self.win_width - 12
        y = rect.bottom - self.win_height - 10
        self.root.geometry(f"{self.win_width}x{self.win_height}+{x}+{y}")

    def build_ui(self):
        container = tk.Frame(self.root, bg="#FFFFFF", padx=14, pady=12)
        container.place(x=1, y=1, width=self.win_width - 2, height=self.win_height - 2)

        # هدر
        header = tk.Frame(container, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 8))

        self.badge_frame = tk.Frame(header, bg="#DCFCE7", padx=8, pady=2)
        self.badge_frame.pack(side="left")
        self.lbl_badge = tk.Label(
            self.badge_frame,
            text="● پایش فعال",
            bg="#DCFCE7",
            fg="#166534",
            font=(FONT_MAIN, 8, "bold")
        )
        self.lbl_badge.pack()

        btn_close = tk.Label(header, text="✕", bg="#FFFFFF", fg="#94A3B8", font=("Segoe UI", 9, "bold"), cursor="hand2")
        btn_close.pack(side="right", padx=(6, 0))
        btn_close.bind("<Button-1>", lambda e: self.hide_flyout())

        tk.Label(header, text="AutoGeoTime", bg="#FFFFFF", fg="#0F172A", font=(FONT_MAIN, 10, "bold")).pack(side="right")

        tk.Frame(container, bg="#E2E8F0", height=1).pack(fill="x", pady=(2, 10))

        # کارت اطلاعات زنده
        card = tk.Frame(container, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, padx=10, pady=9)
        card.pack(fill="x", pady=(0, 10))

        self.lbl_ip = self._add_info_row(card, ":آی‌پی عمومی", "در حال بررسی...")
        self.lbl_country = self._add_info_row(card, ":موقعیت سرور", "---")
        self.lbl_tz = self._add_info_row(card, ":منطقه زمانی", "---")

        # کلیدهای قطع و وصل
        toggles_frame = tk.Frame(container, bg="#FFFFFF")
        toggles_frame.pack(fill="x", pady=(2, 8))

        row_auto = tk.Frame(toggles_frame, bg="#FFFFFF")
        row_auto.pack(fill="x", pady=4)
        self.sw_auto = ToggleSwitch(row_auto, initial=True, command=self.on_toggle_monitoring)
        self.sw_auto.pack(side="left")
        tk.Label(row_auto, text="پایش خودکار تغییر VPN", bg="#FFFFFF", fg="#0F172A", font=(FONT_MAIN, 9)).pack(side="right")

        row_locale = tk.Frame(toggles_frame, bg="#FFFFFF")
        row_locale.pack(fill="x", pady=4)
        self.sw_locale = ToggleSwitch(row_locale, initial=True, command=self.on_toggle_locale)
        self.sw_locale.pack(side="left")
        tk.Label(row_locale, text="هماهنگی فرمت تاریخ و زبان (Locale)", bg="#FFFFFF", fg="#0F172A", font=(FONT_MAIN, 9)).pack(side="right")

        row_startup = tk.Frame(toggles_frame, bg="#FFFFFF")
        row_startup.pack(fill="x", pady=4)
        self.sw_startup = ToggleSwitch(row_startup, initial=self.is_in_startup(), command=self.on_toggle_startup)
        self.sw_startup.pack(side="left")
        tk.Label(row_startup, text="اجرای خودکار با ویندوز", bg="#FFFFFF", fg="#0F172A", font=(FONT_MAIN, 9)).pack(side="right")

        # دکمه‌های اقدام سریع
        actions_frame = tk.Frame(container, bg="#FFFFFF")
        actions_frame.pack(fill="x", pady=(8, 10))

        btn_sync = tk.Button(
            actions_frame,
            text="↻ همگام‌سازی فوری",
            bg="#0F172A",
            fg="#FFFFFF",
            activebackground="#1E293B",
            activeforeground="#FFFFFF",
            relief="flat",
            font=(FONT_MAIN, 8, "bold"),
            cursor="hand2",
            pady=5,
            command=self.force_sync
        )
        btn_sync.pack(side="right", expand=True, fill="x", padx=(4, 0))

        btn_iran = tk.Button(
            actions_frame,
            text="↺ بازگشت به ایران",
            bg="#F1F5F9",
            fg="#0F172A",
            activebackground="#E2E8F0",
            activeforeground="#0F172A",
            relief="flat",
            font=(FONT_MAIN, 8, "bold"),
            cursor="hand2",
            pady=5,
            command=self.reset_to_iran
        )
        btn_iran.pack(side="left", expand=True, fill="x", padx=(0, 4))

        # فوتر وضعیت
        tk.Frame(container, bg="#E2E8F0", height=1).pack(fill="x", pady=(4, 6))
        footer = tk.Frame(container, bg="#FFFFFF")
        footer.pack(fill="x")

        tk.Label(footer, text="v2.0 Smart", bg="#FFFFFF", fg="#94A3B8", font=(FONT_MAIN, 7)).pack(side="left")
        self.lbl_footer = tk.Label(footer, text="آماده پایش...", bg="#FFFFFF", fg="#64748B", font=(FONT_MAIN, 8))
        self.lbl_footer.pack(side="right")

    def _add_info_row(self, parent, label_text, initial_val):
        row = tk.Frame(parent, bg="#F8FAFC")
        row.pack(fill="x", pady=3)
        val_lbl = tk.Label(row, text=initial_val, bg="#F8FAFC", fg="#0F172A", font=(FONT_MAIN, 8, "bold"))
        val_lbl.pack(side="left")
        tk.Label(row, text=label_text, bg="#F8FAFC", fg="#64748B", font=(FONT_MAIN, 8)).pack(side="right")
        return val_lbl

    def set_visual_state(self, state):
        def _update():
            if state == "syncing":
                self.badge_frame.config(bg="#DBEAFE")
                self.lbl_badge.config(text="● در حال اعمال...", bg="#DBEAFE", fg="#1D4ED8")
            elif state == "active":
                self.badge_frame.config(bg="#DCFCE7")
                self.lbl_badge.config(text="● متصل و فعال", bg="#DCFCE7", fg="#166534")
            else:
                self.badge_frame.config(bg="#FEE2E2")
                self.lbl_badge.config(text="● متوقف / قطع", bg="#FEE2E2", fg="#B91C1C")

            if self.tray_icon:
                self.tray_icon.icon = render_app_icon(state, 64)

        self.root.after(0, _update)

    def get_ip_info(self):
        apis = [
            "http://ip-api.com/json/?fields=status,countryCode,city,timezone,query",
            "https://ipapi.co/json/"
        ]
        for url in apis:
            try:
                resp = requests.get(url, timeout=4)
                if resp.status_code == 200:
                    data = resp.json()
                    ip = data.get("query") or data.get("ip")
                    country = data.get("countryCode") or data.get("country_code")
                    city = data.get("city") or ""
                    tz = data.get("timezone")
                    if ip and country and tz:
                        return ip, country.upper(), city, tz
            except Exception:
                continue
        return None, None, None, None

    def apply_system_settings(self, ip, country, city, iana_tz):
        self.set_visual_state("syncing")
        win_tz = IANA_TO_WINDOWS_TZ.get(iana_tz)
        geo_id = COUNTRY_TO_GEOID.get(country)
        locale_name = COUNTRY_TO_LOCALE.get(country, "en-US")

        # ۱. تغییر منطقه زمانی ویندوز
        if win_tz:
            try:
                subprocess.run(["tzutil", "/s", win_tz], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["w32tm", "/resync"], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                pass

        # ۲. تغییر کشور/لوکیشن (GeoID)
        if geo_id:
            try:
                key_path = r"Control Panel\International\Geo"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "Nation", 0, winreg.REG_SZ, str(geo_id))
                    winreg.SetValueEx(key, "Name", 0, winreg.REG_SZ, country)
            except Exception:
                pass

        # ۳. تغییر Regional Format (LocaleName) در صورت فعال بودن
        if self.sync_locale_enabled and locale_name:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International", 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "LocaleName", 0, winreg.REG_SZ, locale_name)
            except Exception:
                pass

        # ۴. ارسال سیگنال آپدیت آنی ساعت نوار وظیفه ویندوز
        broadcast_windows_time_update()

        self.current_ip = ip
        loc_display = f"{city}, {country}" if city else country
        self.current_location_text = f"{loc_display} ({geo_id})" if geo_id else loc_display
        self.current_tz = win_tz if win_tz else iana_tz
        now_str = time.strftime("%H:%M:%S")

        def _refresh_labels():
            self.lbl_ip.config(text=self.current_ip)
            self.lbl_country.config(text=self.current_location_text)
            self.lbl_tz.config(text=self.current_tz)
            self.lbl_footer.config(text=f"آخرین تغییر: {now_str}")

        self.root.after(0, _refresh_labels)
        self.set_visual_state("active" if self.is_monitoring else "paused")
        self.update_tray_tooltip()

    def network_route_watcher(self):
        """رصد آنی تغییرات آداپتور شبکه و جدول مسیریابی (واکنش زیر ۱ ثانیه به قطع/وصل VPN)"""
        iphlpapi = ctypes.windll.iphlpapi
        while True:
            try:
                # مسدود شدن ترد تا لحظه تغییر کارت شبکه یا اتصال/قطع VPN
                iphlpapi.NotifyRouteChange(None, None)
                if self.is_monitoring:
                    time.sleep(0.8)  # فرصت کوتاه برای تثبیت مسیر تونل VPN
                    self.last_ip = None
                    self.wake_event.set()
            except Exception:
                time.sleep(3)

    def monitor_loop(self):
        while True:
            if self.is_monitoring:
                ip, country, city, tz = self.get_ip_info()
                if ip and ip != self.last_ip:
                    self.apply_system_settings(ip, country, city, tz)
                    self.last_ip = ip
            # انتظار تا ۱۰ ثانیه یا بیدار شدن فوری توسط رویداد تغییر شبکه
            self.wake_event.wait(timeout=10)
            self.wake_event.clear()

    def single_instance_listener(self):
        """گوش دادن به درخواست باز کردن پنجره در صورت اجرای مجدد فایل EXE"""
        kernel32 = ctypes.windll.kernel32
        event = kernel32.CreateEventW(None, False, False, SHOW_EVENT_NAME)
        while True:
            res = kernel32.WaitForSingleObject(event, 0xFFFFFFFF)
            if res == 0:
                self.root.after(0, self.show_flyout)

    def force_sync(self):
        self.last_ip = None
        threading.Thread(target=self._single_check, daemon=True).start()

    def _single_check(self):
        self.set_visual_state("syncing")
        ip, country, city, tz = self.get_ip_info()
        if ip:
            self.apply_system_settings(ip, country, city, tz)
            self.last_ip = ip
        else:
            self.root.after(0, lambda: self.lbl_footer.config(text="خطا در دریافت اطلاعات IP"))
            self.set_visual_state("active" if self.is_monitoring else "paused")

    def reset_to_iran(self):
        threading.Thread(
            target=self.apply_system_settings,
            args=(self.current_ip, "IR", "Tehran", "Asia/Tehran"),
            daemon=True
        ).start()

    def on_toggle_monitoring(self, state):
        self.is_monitoring = state
        if self.is_monitoring:
            self.set_visual_state("active")
            self.last_ip = None
            self.wake_event.set()
        else:
            self.set_visual_state("paused")
        self.update_tray_tooltip()

    def on_toggle_locale(self, state):
        self.sync_locale_enabled = state
        if state and self.is_monitoring:
            self.force_sync()

    def is_in_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False

    def on_toggle_startup(self, state):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if state:
                exe_path = (
                    f'"{sys.executable}" --minimized'
                    if getattr(sys, "frozen", False)
                    else f'"{sys.executable}" "{os.path.abspath(__file__)}" --minimized'
                )
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception:
            pass

    def setup_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem("باز / بسته کردن پنل", self.toggle_flyout_from_tray, default=True),
            pystray.MenuItem("همگام‌سازی فوری", lambda: self.root.after(0, self.force_sync)),
            pystray.MenuItem("بازگشت به ایران", lambda: self.root.after(0, self.reset_to_iran)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("خروج کامل", self.quit_app)
        )
        self.tray_icon = pystray.Icon(APP_NAME, render_app_icon("active", 64), "AutoGeoTime - متصل", menu)
        self.tray_icon.run()

    def update_tray_tooltip(self):
        if self.tray_icon:
            status_txt = "متصل" if self.is_monitoring else "قطع/متوقف"
            self.tray_icon.title = f"AutoGeoTime ({status_txt})\n{self.current_location_text} | {self.current_ip}"

    def toggle_flyout_from_tray(self, icon=None, item=None):
        if self.is_visible:
            self.root.after(0, self.hide_flyout)
        else:
            self.root.after(0, self.show_flyout)

    def show_flyout(self):
        self.position_near_clock()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.is_visible = True

    def hide_flyout(self):
        self.root.withdraw()
        self.is_visible = False

    def on_focus_out(self, event):
        if self.root.focus_get() is None:
            self.hide_flyout()

    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)
        os._exit(0)


if __name__ == "__main__":
    _mutex = check_single_instance()
    ensure_ico_file()
    load_bundled_fonts()
    root = tk.Tk()
    app = AutoGeoTimeFlyout(root)
    root.mainloop()