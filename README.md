<div align="center" dir="rtl">

<img src="assets/logo.svg" alt="AutoGeoTime Logo" width="88" height="88" />

# AutoGeoTime
**همگام‌ساز هوشمند و خودکار ساعت، منطقه زمانی، موقعیت مکانی و مختصات GPS ویندوز با IP**

[![Build Windows EXE](https://github.com/mostafa5804/AutoGeoTime/actions/workflows/build-windows.yml/badge.svg)](https://github.com/mostafa5804/AutoGeoTime/actions/workflows/build-windows.yml)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Privilege](https://img.shields.io/badge/UAC-Administrator-F59E0B)
![License](https://img.shields.io/badge/License-MIT-10B981)

</div>

---

<div dir="rtl">

## معرفی پروژه
هنگام استفاده از ابزارهای تغییر IP و VPN روی ویندوز، اختلاف بین **ساعت سیستم (Time Zone)**، **موقعیت منطقه‌ای (Location / Region)** و **مختصات جغرافیایی (GPS)** با IP سرور مقصد، یکی از اصلی‌ترین دلایل شناسایی موقعیت واقعی توسط وب‌سایت‌ها، برنامه‌های ویندوزی و ایجاد خطا در گواهی‌های امنیتی مرورگرهاست.

**AutoGeoTime** یک ابزار سبک، پرتابل و بومی برای ویندوز ۱۰ و ۱۱ است که در کنار ساعت ویندوز (System Tray) مستقر می‌شود و به محض اتصال، تغییر سرور یا قطع شدن VPN، تمامی لایه‌های زمانی و مکانی ویندوز را به صورت خودکار و در کمتر از یک ثانیه با شهر و کشور مقصد همگام می‌کند.

---

## ویژگی‌های کلیدی

* **واکنش آنی به تغییرات شبکه (زیر ۱ ثانیه):** اتصال مستقیم به هسته شبکه ویندوز (`iphlpapi`) برای تشخیص لحظه‌ای تغییر کارت شبکه و جدول مسیریابی هنگام قطع و وصل شدن هر نوع VPN.
* **همگام‌سازی همزمان ۴ لایه زمانی و مکانی در ویندوز:**
  1. **منطقه زمانی (`Time Zone`):** نگاشت خودکار بیش از ۱۰۰ منطقه زمانی استاندارد IANA به فرمت ویندوز و همگام‌سازی فوری ساعت.
  2. **مختصات جغرافیایی GPS (`DefaultLocation`):** استخراج طول و عرض جغرافیایی (`Latitude` و `Longitude`) شهر سرور VPN و ثبت مستقیم آن در رجیستری سرویس موقعیت‌یابی ویندوز (`HKLM`) تا برنامه‌هایی که از Location ویندوز استفاده می‌کنند مختصات همان شهر را دریافت کنند.
  3. **کشور و منطقه (`Home Location / GeoID`):** به‌روزرسانی کد کشور در رجیستری ویندوز برای بیش از ۹۵ کشور جهان.
  4. **فرمت منطقه‌ای و زبان تقویم (`Regional Format / Locale`):** هماهنگ‌سازی اختیاری فرمت تاریخ و زبان سیستم (مانند `en-US`، `nl-NL`، `de-DE` و `fa-IR`).
* **به‌روزرسانی فوری ساعت Taskbar:** ارسال سیگنال‌های سیستمی `WM_TIMECHANGE` و `WM_SETTINGCHANGE` تا ساعت نوار وظیفه بدون تأخیر تغییر کند.
* **پنل بازشو جمع‌وجور کنار ساعت (Flyout UI):** رابط گرافیکی مدرن، سبک و مجهز به فونت فارسی **Vazirmatn** با کلیدهای کنترل مجزا برای پایش خودکار، GPS و Locale.
* **نشانگر بصری وضعیت در System Tray:**
  * 🟢 **سبز:** پایش خودکار فعال و متصل
  * 🔵 **آبی:** در حال تشخیص تغییر IP و اعمال تنظیمات
  * 🔴 **قرمز:** پایش متوقف / قطع شده توسط کاربر
* **اجرای تک‌نمونه‌ای (Single Instance):** جلوگیری از باز شدن نسخه‌های تکراری در پس‌زمینه.

---

## پیش‌نیاز دسترسی ادمین (UAC)
برای ثبت خودکار مختصات جغرافیایی (`Latitude` و `Longitude`) در شاخه سیستمی رجیستری ویندوز (`HKEY_LOCAL_MACHINE`)، برنامه به صورت خودکار هنگام اجرا دسترسی **Administrator** درخواست می‌کند.

> **نکته برای استفاده از قابلیت GPS:** برای اینکه برنامه‌های ویندوز از مختصات ثبت‌شده استفاده کنند، مطمئن شوید گزینه **Location services** در مسیر `Settings > Privacy & security > Location` روشن است. در غیر این صورت، با خاموش کردن کلید GPS در پنل برنامه، سایر بخش‌ها (Time Zone، GeoID و Locale) بدون نیاز به سرویس Location کار خواهند کرد.

---

## نصب و اجرا

### روش اول: دانلود نسخه آماده و پرتابل (پیشنهادی)
1. به بخش [**Releases**](https://github.com/mostafa5804/AutoGeoTime/releases) در همین مخزن بروید و فایل **`AutoGeoTime.exe`** را دانلود کنید.
2. فایل را در یک مسیر ثابت (مثلاً `C:\Tools\AutoGeoTime.exe`) قرار داده و اجرا کنید (پنجره تایید UAC را تایید نمایید).
3. از داخل پنل کنار ساعت، کلیدهای مورد نظر خود را تنظیم کنید.

### روش دوم: اجرا و بیلد از سورس کد
```bash
git clone [https://github.com/mostafa5804/AutoGeoTime.git](https://github.com/mostafa5804/AutoGeoTime.git)
cd AutoGeoTime
pip install -r requirements.txt
python AutoGeoTime.py
