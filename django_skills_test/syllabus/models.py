from django.db import models
#学部
class Department(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
#講義
class Course(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    exam_ratio = models.IntegerField()
    report_ratio = models.IntegerField()
    def __str__(self):
        return self.title

#口コミ
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.course.title} のレビュー"