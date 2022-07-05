from datetime import date, datetime

today = date.today()
now = datetime.now()

tanggal_absensi = today.strftime("%B %d, %Y")
check_in = now.strftime("%H:%M:%S")
check_out = now.strftime("%H:%M:%S")

tanggal_absensi2 = today.strftime("%Y-%d-%b")

print(tanggal_absensi)
print(check_in)
print(check_out)

print(now)