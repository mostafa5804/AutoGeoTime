<div align="center" dir="rtl">

<img src="assets/logo.svg" alt="AutoGeoTime Logo" width="88" height="88" />

# AutoGeoTime
**همگام‌ساز هوشمند و خودکار ساعت، منطقه زمانی و موقعیت جغرافیایی ویندوز با IP**

[![Build Windows EXE](https://github.com/mostafa5804/AutoGeoTime/actions/workflows/build-windows.yml/badge.svg)](https://github.com/mostafa5804/AutoGeoTime/actions/workflows/build-windows.yml)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10B981)

</div>

---

<div dir="rtl">

## معرفی پروژه
هنگام استفاده از ابزارهای تغییر IP و VPN روی ویندوز، اختلاف بین **ساعت سیستم (Time Zone)** و **موقعیت جغرافیایی ویندوز (Location / Region)** با IP سرور مقصد، یکی از اصلی‌ترین دلایل شناسایی موقعیت واقعی توسط وب‌سایت‌ها، سرویس‌های آنلاین و ایجاد خطا در گواهی‌های امنیتی مرورگرهاست.

**AutoGeoTime** یک ابزار سبک، پرتابل و بومی برای ویندوز ۱۰ و ۱۱ است که در کنار ساعت ویندوز (System Tray) مستقر می‌شود و به محض اتصال، تغییر سرور یا قطع شدن VPN، تنظیمات زمانی و مکانی ویندوز را به صورت خودکار و در کمتر از یک ثانیه با کشور مقصد همگام می‌کند.

---

## ویژگی‌های کلیدی

* **واکنش آنی به تغییرات شبکه (زیر ۱ ثانیه):** اتصال مستقیم به هسته شبکه ویندوز (`iphlpapi`) برای تشخیص لحظه‌ای تغییر کارت شبکه و جدول مسیریابی هنگام قطع و وصل شدن هر نوع VPN.
* **تغییر همزمان ۳ پارامتر کلیدی ویندوز:**
  1. **منطقه زمانی (`Time Zone`):** نگاشت خودکار بیش از ۱۰۰ منطقه زمانی استاندارد IANA به فرمت ویندوز و همگام‌سازی فوری ساعت.
  2. **موقعیت جغرافیایی (`Home Location / GeoID`):** به‌روزرسانی کد کشور در رجیستری ویندوز برای بیش از ۹۵ کشور جهان.
  3. **فرمت منطقه‌ای و زبان تقویم (`Regional Format / Locale`):** هماهنگ‌سازی اختیاری فرمت تاریخ و زبان سیستم (مانند `en-US`، `nl-NL`، `de-DE` و `fa-IR`).
* **به‌روزرسانی فوری ساعت Taskbar:** ارسال سیگنال‌های سیستمی `WM_TIMECHANGE` و `WM_SETTINGCHANGE` تا ساعت نوار وظیفه بدون تأخیر تغییر کند.
* **پنل بازشو جمع‌وجور کنار ساعت (Flyout UI):** رابط گرافیکی مدرن، سبک و مجهز به فونت فارسی **Vazirmatn** بدون اشغال فضای دسکتاپ.
* **نشانگر بصری وضعیت در System Tray:**
  * 🟢 **سبز:** پایش خودکار فعال و متصل
  * 🔵 **آبی:** در حال تشخیص تغییر IP و اعمال تنظیمات
  * 🔴 **قرمز:** پایش متوقف / قطع شده توسط کاربر
* **اجرای خودکار و تک‌نمونه‌ای (Single Instance):** پشتیبانی از اجرای مخفی در Startup ویندوز و جلوگیری از باز شدن نسخه‌های تکراری.

---

## نصب و اجرا

### روش اول: دانلود نسخه آماده و پرتابل (پیشنهادی)
1. به بخش [**Releases**](https://github.com/mostafa5804/AutoGeoTime/releases) در همین مخزن بروید و فایل **`AutoGeoTime.exe`** را دانلود کنید.
2. فایل را در یک مسیر ثابت (مثلاً `C:\Tools\AutoGeoTime.exe`) قرار داده و اجرا کنید.
3. از داخل پنل کنار ساعت، گزینه **«اجرای خودکار با ویندوز»** را فعال کنید.

### روش دوم: اجرا و بیلد از سورس کد
```bash
git clone [https://github.com/mostafa5804/AutoGeoTime.git](https://github.com/mostafa5804/AutoGeoTime.git)
cd AutoGeoTime
pip install -r requirements.txt
python AutoGeoTime.py