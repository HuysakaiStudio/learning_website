# Script kiểm tra môn học trong database
from apps.kien_thuc.models import Mon

print("=" * 50)
print("DANH SACH MON HOC")
print("=" * 50)
print(f"\nTong so mon: {Mon.objects.count()}\n")

for i, mon in enumerate(Mon.objects.all(), 1):
    print(f"{i}. {mon.ten}")
    print(f"   Mo ta: {mon.mo_ta[:50]}...")
    print()

print("=" * 50)
print("HOAN TAT!")
print("=" * 50)
