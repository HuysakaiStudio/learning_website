from django import forms
from .models import DeThi, CauHoi
from apps.kien_thuc.models import Mon

class DeThiForm(forms.ModelForm):
    class Meta:
        model = DeThi
        fields = ['ten', 'mon', 'mo_ta', 'thoi_gian_phut']
        labels = {
            'ten': 'Tên đề thi',
            'mon': 'Môn học',
            'mo_ta': 'Mô tả',
            'thoi_gian_phut': 'Thời gian (phút)',
        }
        widgets = {
            'ten': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập tên đề thi'
            }),
            'mon': forms.Select(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;'
            }),
            'mo_ta': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập mô tả đề thi (tùy chọn)'
            }),
            'thoi_gian_phut': forms.NumberInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'min': '1'
            }),
        }

class ImportDeThiForm(forms.Form):
    ten = forms.CharField(
        max_length=200,
        label='Tên đề thi',
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
            'placeholder': 'Nhập tên đề thi'
        })
    )
    mon = forms.ModelChoiceField(
        queryset=Mon.objects.all(),
        empty_label="-- Chọn môn học --",
        label="Môn học",
        widget=forms.Select(attrs={
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;'
        })
    )
    csv_file = forms.FileField(
        label='File CSV',
        help_text='Định dạng: Cột đầu tiên là loại (tn/ds/dien), sau đó là nội dung và các trường khác',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;'
        })
    )

class TracNghiemForm(forms.ModelForm):
    dap_an_dung = forms.ChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        label='Đáp án đúng',
        widget=forms.Select(attrs={
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;'
        })
    )
    
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'giai_thich', 'dap_an_a', 'dap_an_b', 'dap_an_c', 'dap_an_d', 'dap_an_dung']
        labels = {
            'noi_dung': 'Nội dung câu hỏi',
            'giai_thich': 'Giải thích',
            'dap_an_a': 'Đáp án A',
            'dap_an_b': 'Đáp án B',
            'dap_an_c': 'Đáp án C',
            'dap_an_d': 'Đáp án D',
            'dap_an_dung': 'Đáp án đúng',
        }
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập nội dung câu hỏi'
            }),
            'giai_thich': forms.Textarea(attrs={
                'rows': 2,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập giải thích (tùy chọn)'
            }),
            'dap_an_a': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án A'
            }),
            'dap_an_b': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án B'
            }),
            'dap_an_c': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án C'
            }),
            'dap_an_d': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án D'
            }),
        }

class BulkAddQuestionsForm(forms.Form):
    LOAI_CAU_CHOICES = [
        ('tn', '📌 Trắc nghiệm ABCD (4 đáp án)'),
        ('ds', '✅ Trắc nghiệm Đúng/Sai (4 ý)'),
        ('dien', '🔢 Trả lời ngắn (Điền số)'),
    ]
    
    loai = forms.ChoiceField(
        choices=LOAI_CAU_CHOICES,
        label='Loại câu hỏi',
        widget=forms.RadioSelect(attrs={
            'style': 'margin: 12px 0;'
        })
    )
    questions_text = forms.CharField(
        label='Nhập câu hỏi',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
            'placeholder': 'Ví dụ:\nCâu 1 là gì?|Đáp án A|Đáp án B|Đáp án C|Đáp án D|A|Giải thích'
        })
    )

class TracNghiemForm(forms.ModelForm):
    dap_an_dung = forms.ChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        label='Đáp án đúng',
        widget=forms.Select(attrs={
            'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;'
        })
    )
    
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'giai_thich', 'dap_an_a', 'dap_an_b', 'dap_an_c', 'dap_an_d', 'dap_an_dung']
        labels = {
            'noi_dung': 'Nội dung câu hỏi',
            'giai_thich': 'Giải thích',
            'dap_an_a': 'Đáp án A',
            'dap_an_b': 'Đáp án B',
            'dap_an_c': 'Đáp án C',
            'dap_an_d': 'Đáp án D',
            'dap_an_dung': 'Đáp án đúng',
        }
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập nội dung câu hỏi'
            }),
            'giai_thich': forms.Textarea(attrs={
                'rows': 2,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập giải thích (tùy chọn)'
            }),
            'dap_an_a': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án A'
            }),
            'dap_an_b': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án B'
            }),
            'dap_an_c': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án C'
            }),
            'dap_an_d': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án D'
            }),
        }

class DungSaiForm(forms.ModelForm):
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'giai_thich', 'y_a', 'y_b', 'y_c', 'y_d', 'dung_sai_a', 'dung_sai_b', 'dung_sai_c', 'dung_sai_d']
        labels = {
            'noi_dung': 'Nội dung câu hỏi',
            'giai_thich': 'Giải thích',
            'y_a': 'Ý A',
            'y_b': 'Ý B',
            'y_c': 'Ý C',
            'y_d': 'Ý D',
            'dung_sai_a': 'Ý A (Đúng/Sai)',
            'dung_sai_b': 'Ý B (Đúng/Sai)',
            'dung_sai_c': 'Ý C (Đúng/Sai)',
            'dung_sai_d': 'Ý D (Đúng/Sai)',
        }
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập nội dung câu hỏi'
            }),
            'giai_thich': forms.Textarea(attrs={
                'rows': 2,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập giải thích (tùy chọn)'
            }),
            'y_a': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập ý A'
            }),
            'y_b': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập ý B'
            }),
            'y_c': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập ý C'
            }),
            'y_d': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập ý D'
            }),
            'dung_sai_a': forms.CheckboxInput(attrs={
                'style': 'width: 20px; height: 20px; cursor: pointer;'
            }),
            'dung_sai_b': forms.CheckboxInput(attrs={
                'style': 'width: 20px; height: 20px; cursor: pointer;'
            }),
            'dung_sai_c': forms.CheckboxInput(attrs={
                'style': 'width: 20px; height: 20px; cursor: pointer;'
            }),
            'dung_sai_d': forms.CheckboxInput(attrs={
                'style': 'width: 20px; height: 20px; cursor: pointer;'
            }),
        }

class DienSoForm(forms.ModelForm):
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'giai_thich', 'dap_an_so']
        labels = {
            'noi_dung': 'Nội dung câu hỏi',
            'giai_thich': 'Giải thích',
            'dap_an_so': 'Đáp án số',
        }
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập nội dung câu hỏi'
            }),
            'giai_thich': forms.Textarea(attrs={
                'rows': 2,
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập giải thích (tùy chọn)'
            }),
            'dap_an_so': forms.TextInput(attrs={
                'type': 'number',
                'step': 'any',
                'style': 'width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px;',
                'placeholder': 'Nhập đáp án số'
            }),
        }
