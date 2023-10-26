from django.contrib import admin

from projectaccount.models import Semester, Subject
from store.models import Student, TheoryInternalMark
from store.serializer import TheoryInternalMarkSerializer

# Register your models here.



class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Semester, SemesterAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "semester","role")


admin.site.register(Subject, SubjectAdmin)



class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "register_number","roll_number","semester")


admin.site.register(Student, StudentAdmin)



class TheoryInternalMarkAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "subject", "semester", "average_internal_mark", "average_assignment_mark", "attendance_percentage_mark")

    def average_internal_mark(self, obj):
        serializer = TheoryInternalMarkSerializer()
        return serializer.get_average_internal_mark(obj)

    def average_assignment_mark(self, obj):
        serializer = TheoryInternalMarkSerializer()
        return serializer.get_average_assignment_mark(obj)

    def attendance_percentage_mark(self, obj):
        serializer = TheoryInternalMarkSerializer()
        return serializer.get_attendance_percentage_mark(obj)

    average_internal_mark.short_description = "Average Internal Mark"
    average_assignment_mark.short_description = "Average Assignment Mark"
    attendance_percentage_mark.short_description = "Attendance Percentage Mark"

admin.site.register(TheoryInternalMark, TheoryInternalMarkAdmin)