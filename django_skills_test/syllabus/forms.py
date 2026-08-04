from django import forms
from .models import Review, Course

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'おすすめ度',
            'comment': 'コメント',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'teacher', 'department', 'description', 'exam_ratio', 'report_ratio']
        labels = {
            'title': '講義名',
            'teacher': '担当教員',
            'department': '学部・学科',
            'description': '講義概要',
            'exam_ratio': 'テスト割合(%)',
            'report_ratio': 'レポート割合(%)',
        }

    def clean(self):
        cleaned_data = super().clean()
        exam_ratio = cleaned_data.get('exam_ratio')
        report_ratio = cleaned_data.get('report_ratio')

        if exam_ratio is not None and report_ratio is not None:
            if exam_ratio < 0 or report_ratio < 0 or (exam_ratio + report_ratio) > 100:
                raise forms.ValidationError("評価割合の合計は100%以下（マイナス不可）で設定してください")
        return cleaned_data