from django.contrib import admin
from .models import Quiz, Question, Option, Result


# Inline options inside question
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4   # 4 options ek sathe


# Question admin with inline options
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)