import tkinter as tk
import requests
import urllib.parse

root = tk.Tk()
root.title("Weather App")
root.geometry("430x260")
root.configure(bg="#102a43")

city = tk.StringVar()

def weather_text(code):
    mapping = {
        0: "صاف", 1: "کم‌ابری", 2: "قسمتی ابری", 3: "ابری",
        45: "مه‌آلود", 48: "مه‌آلود", 51: "نم‌نم", 53: "نم‌نم", 55: "باران ریز",
        56: "یخ‌زدگی", 57: "یخ‌زدگی", 61: "باران", 63: "باران شدید", 65: "باران شدید",
        66: "باران یخ‌زن", 67: "باران یخ‌زن", 71: "برف", 73: "برف", 75: "برف شدید",
        77: "دانه‌های برف", 80: "باران سبک", 81: "باران", 82: "باران سنگین",
        85: "برف سبک", 86: "برف سنگین", 95: "رعد و برق", 96: "رعد و برق", 99: "رعد و برق شدید"
    }
    return mapping.get(code, "نامشخص")


def show_weather():
    name = city.get().strip()
    if not name:
        status.config(text="لطفاً نام شهر را وارد کنید", fg="#ffb4b4")
        return
    try:
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(name)}&count=1&language=fa&format=json",
            timeout=10
        )
        geo.raise_for_status()
        data = geo.json()
        if "results" not in data or not data["results"]:
            status.config(text="شهر پیدا نشد", fg="#ffb4b4")
            return
        place = data["results"][0]
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={place['latitude']}&longitude={place['longitude']}&current=temperature_2m,weather_code&timezone=auto",
            timeout=10
        )
        weather.raise_for_status()
        w = weather.json()
        temp = w["current"]["temperature_2m"]
        code = w["current"]["weather_code"]
        result.config(text=f"{place['name']} | {temp}°C | {weather_text(code)}", fg="#ecfeff")
        status.config(text="اطلاعات هوا با موفقیت دریافت شد", fg="#9ae6b4")
    except Exception as e:
        result.config(text="خطا در دریافت اطلاعات", fg="#fdf2f8")
        status.config(text=f"مشکل: {str(e)[:80]}", fg="#ffb4b4")


tk.Label(root, text="نام شهر", bg="#102a43", fg="#e2e8f0", font=("Tahoma", 12, "bold")).pack(pady=(18, 6))
entry = tk.Entry(root, textvariable=city, width=22, font=("Tahoma", 12), bg="#dbeafe", fg="#0f172a")
entry.pack()
entry.bind("<Return>", lambda event: show_weather())

tk.Button(root, text="بررسی هوا", bg="#ef4444", fg="white", font=("Tahoma", 11, "bold"), command=show_weather, width=18).pack(pady=12)
result = tk.Label(root, text="", bg="#1d4ed8", fg="white", font=("Tahoma", 11), wraplength=330, justify="center")
result.pack(pady=(0, 8), padx=15)
status = tk.Label(root, text="", bg="#102a43", fg="#d1fae5", font=("Tahoma", 10))
status.pack()

if __name__ == "__main__":
    root.mainloop()
