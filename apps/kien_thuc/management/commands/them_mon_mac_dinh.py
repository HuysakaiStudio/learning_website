from django.core.management.base import BaseCommand
from apps.kien_thuc.models import Mon

MON_HOC = [
    {
        'icon': '🧮',
        'ten': 'Toán',
        'mo_ta': 'Đại số, Hình học, Giải tích, Xác suất thống kê',
    },
    {
        'icon': '⚛️',
        'ten': 'Vật lý',
        'mo_ta': 'Cơ học, Nhiệt học, Điện học, Quang học, Vật lý hiện đại',
    },
    {
        'icon': '⚗️',
        'ten': 'Hóa học',
        'mo_ta': 'Hóa đại cương, Hóa vô cơ, Hóa hữu cơ',
    },
    {
        'icon': '🌿',
        'ten': 'Sinh học',
        'mo_ta': 'Tế bào, Di truyền, Tiến hóa, Sinh thái học',
    },
    {
        'icon': '📖',
        'ten': 'Ngữ văn',
        'mo_ta': 'Đọc hiểu, Nghị luận xã hội, Nghị luận văn học',
    },
    {
        'icon': '🌍',
        'ten': 'Tiếng Anh',
        'mo_ta': 'Ngữ pháp, Từ vựng, Đọc hiểu, Viết, Nghe nói',
    },
    {
        'icon': '🗺️',
        'ten': 'Địa lý',
        'mo_ta': 'Địa lý tự nhiên, Địa lý kinh tế, Địa lý Việt Nam',
    },
    {
        'icon': '🏛️',
        'ten': 'Lịch sử',
        'mo_ta': 'Lịch sử thế giới, Lịch sử Việt Nam hiện đại',
    },
    {
        'icon': '⚖️',
        'ten': 'GDCD',
        'mo_ta': 'Pháp luật, Đạo đức, Kinh tế, Chính trị',
    },
    {
        'icon': '💻',
        'ten': 'Tin học',
        'mo_ta': 'Thuật toán, Lập trình, Cơ sở dữ liệu, Mạng máy tính',
    },
]

class Command(BaseCommand):
    help = 'Thêm các môn học cơ bản cho THPTQG'

    def handle(self, *args, **kwargs):
        da_them = 0
        bo_qua = 0

        for mon in MON_HOC:
            obj, created = Mon.objects.get_or_create(
                ten=mon['ten'],
                defaults={
                    'icon': mon['icon'],
                    'mo_ta': mon['mo_ta'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Đã thêm: {mon["icon"]} {mon["ten"]}'))
                da_them += 1
            else:
                self.stdout.write(self.style.WARNING(f'  ⏭️  Bỏ qua (đã có): {mon["ten"]}'))
                bo_qua += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Hoàn tất! Đã thêm {da_them} môn, bỏ qua {bo_qua} môn đã tồn tại.'
        ))