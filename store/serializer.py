from rest_framework import serializers
from projectaccount.models import Account, Subject ,Semester
from .models import LabInternalMark, Student, TheoryInternalMark



class SemesterSerializer(serializers.ModelSerializer):

    total_semester_count = serializers.SerializerMethodField()
    class Meta:
        model = Semester
        fields = ('id', 'name', 'total_semester_count')

    def get_total_semester_count(self, obj):
        return Semester.objects.count()

    

class SubjectSerializer(serializers.ModelSerializer):
    # semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all(), many=True)
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    total_subject_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ('id', 'name','semester','semester_name','role','total_subject_count')


    def get_total_subject_count(self, obj):
        return Subject.objects.count()




class RegisterTeacherSerializer(serializers.ModelSerializer):
    # subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    # subject_name = serializers.CharField(source="subject.name", read_only=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True)
    subject_name = serializers.StringRelatedField(source="subject", many=True, read_only=True)

    password = serializers.CharField(write_only=True)
    copy_pass = serializers.CharField(read_only=True)
    total_teachers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = ["id", "full_name", "username", "password", "subject", "subject_name", "copy_pass","total_teachers_count"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }

    def create(self, validated_data):
        subject = validated_data.pop('subject', None)
        # semester = validated_data.pop('semester', None)
        password = validated_data.pop('password')  
        user = Account.objects.create(
            username=validated_data["username"],
            full_name=validated_data["full_name"],
            role="teacher",
            copy_pass=password,  # Set copy_pass here
        )
        user.set_password(password)  

        # if subject:
        #     user.subject = subject

        if subject:
            user.subject.set(subject)  # Set multiple semesters

        
        user.save()

        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['copy_pass'] = instance.copy_pass  # Include copy_pass in the response
        return ret
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject_name'] = [subject.name for subject in instance.subject.all()]
        return ret
    
    def get_total_teachers_count(self, obj):
        return Account.objects.filter(role="teacher").count()


    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['copy_pass'] = instance.copy_pass  # Include copy_pass in the response
    #     return ret


class RegisterStudentSerializer(serializers.ModelSerializer):

    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    total_students_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "register_number",
            "roll_number",
            "semester",
            "semester_name",
            "total_students_count"
        ]


    def get_total_students_count(self, obj):
        return Student.objects.count()

class PostTheoryInternalMarkSerializer(serializers.ModelSerializer):
    student_name = RegisterStudentSerializer(source="student",read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    average_internal_mark = serializers.SerializerMethodField()
    average_assignment_mark = serializers.SerializerMethodField()

    # subject = SubjectSerializer()
    
    attendance_percentage_mark = serializers.SerializerMethodField()
    total_internal_mark = serializers.SerializerMethodField()

    class Meta:
        model = TheoryInternalMark
        fields = [
            "id",
            "student",
            "student_name",
            "subject",
            "subject_name",
            "semester",
            "se1",
            "se2",
            "se3",
            "average_internal_mark", 

            "assignment1",
            "assignment2",
            "assignment3",
            "average_assignment_mark",

            "attendance_percentage",
            "attendance_percentage_mark",
            "total_internal_mark"
        ]

    def get_average_internal_mark(self, obj):
        se1 = obj.se1 or 0
        se2 = obj.se2 or 0
        se3 = obj.se3 or 0

        total_marks = se1 + se2 + se3
        return total_marks / 3
    

    def get_average_assignment_mark(self, obj):
        assignment1 = obj.assignment1 or 0
        assignment2 = obj.assignment2 or 0
        assignment3 = obj.assignment3 or 0

        total_marks = assignment1 + assignment2 + assignment3
        return total_marks / 3
    
    def get_attendance_percentage_mark(self, obj):
        attendance_percentage = obj.attendance_percentage

        if attendance_percentage is not None:
            if 90 <= attendance_percentage <= 100:
                return 10
            elif 80 <= attendance_percentage < 90:
                return 9
            elif 70 <= attendance_percentage < 80:
                return 8
            elif 60 <= attendance_percentage < 70:
                return 7
            else:
                return 6
        else:
            return 0

        
    def get_total_internal_mark(self, obj):
        average_internal_mark = self.get_average_internal_mark(obj)
        average_assignment_mark = self.get_average_assignment_mark(obj)
        attendance_percentage_mark = self.get_attendance_percentage_mark(obj)

        total_internal_mark = average_internal_mark + average_assignment_mark + attendance_percentage_mark

        return total_internal_mark



class PostLabInternalMarkSerializer(serializers.ModelSerializer):

    student_name = RegisterStudentSerializer(source="student",read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    average_test_mark = serializers.SerializerMethodField() 
    # subject = SubjectSerializer()
    total_lab_mark = serializers.SerializerMethodField()

    class Meta:
        model = LabInternalMark
        fields = [
            
            'id',
            "student",
            "student_name",
            "subject",
            "subject_name",
            "semester",

            "test1",
            "test2",
            "average_test_mark",

            "rough_record_mark",
            "fair_record_mark",
            "lab_work_mark",
            "open_ended_mark",
            "attendance_mark",

            "total_lab_mark"

            ]
        
    def get_average_test_mark(self, obj):
        test1 = obj.test1 or 0
        test2 = obj.test2 or 0

        total_marks = test1 + test2
        return total_marks / 2
    
    
    def get_total_lab_mark(self, obj):
        average_test_mark = self.get_average_test_mark(obj)
        rough_record_mark = obj.rough_record_mark or 0
        fair_record_mark = obj.fair_record_mark or 0
        lab_work_mark = obj.lab_work_mark or 0
        open_ended_mark = obj.open_ended_mark or 0
        attendance_mark = obj.attendance_mark or 0


        total_internal_mark = average_test_mark + rough_record_mark + lab_work_mark + fair_record_mark + open_ended_mark + attendance_mark

        return total_internal_mark



class RegisterStudentSerializer(serializers.ModelSerializer):

    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    total_students_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "register_number",
            "roll_number",
            "semester",
            "semester_name",
            "total_students_count"
        ]


    def get_total_students_count(self, obj):
        return Student.objects.count()

class TheoryInternalMarkSerializer(serializers.ModelSerializer):
    student_name = RegisterStudentSerializer(source="student",read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    average_internal_mark = serializers.SerializerMethodField()
    average_assignment_mark = serializers.SerializerMethodField()

    subject = SubjectSerializer()
    
    attendance_percentage_mark = serializers.SerializerMethodField()
    total_internal_mark = serializers.SerializerMethodField()

    class Meta:
        model = TheoryInternalMark
        fields = [
            "id",
            "student",
            "student_name",
            "subject",
            "subject_name",
            "semester",
            "se1",
            "se2",
            "se3",
            "average_internal_mark", 

            "assignment1",
            "assignment2",
            "assignment3",
            "average_assignment_mark",

            "attendance_percentage",
            "attendance_percentage_mark",
            "total_internal_mark"
        ]

    def get_average_internal_mark(self, obj):
        se1 = obj.se1 or 0
        se2 = obj.se2 or 0
        se3 = obj.se3 or 0

        total_marks = se1 + se2 + se3
        return total_marks / 3
    

    def get_average_assignment_mark(self, obj):
        assignment1 = obj.assignment1 or 0
        assignment2 = obj.assignment2 or 0
        assignment3 = obj.assignment3 or 0

        total_marks = assignment1 + assignment2 + assignment3
        return total_marks / 3
    
    def get_attendance_percentage_mark(self, obj):
        attendance_percentage = obj.attendance_percentage

        if attendance_percentage is not None:
            if 90 <= attendance_percentage <= 100:
                return 10
            elif 80 <= attendance_percentage < 90:
                return 9
            elif 70 <= attendance_percentage < 80:
                return 8
            elif 60 <= attendance_percentage < 70:
                return 7
            else:
                return 6
        else:
            return 0

        
    def get_total_internal_mark(self, obj):
        average_internal_mark = self.get_average_internal_mark(obj)
        average_assignment_mark = self.get_average_assignment_mark(obj)
        attendance_percentage_mark = self.get_attendance_percentage_mark(obj)

        total_internal_mark = average_internal_mark + average_assignment_mark + attendance_percentage_mark

        return total_internal_mark



class LabInternalMarkSerializer(serializers.ModelSerializer):

    student_name = RegisterStudentSerializer(source="student",read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    average_test_mark = serializers.SerializerMethodField() 
    subject = SubjectSerializer()
    total_lab_mark = serializers.SerializerMethodField()

    class Meta:
        model = LabInternalMark
        fields = [
            
            'id',
            "student",
            "student_name",
            "subject",
            "subject_name",
            "semester",

            "test1",
            "test2",
            "average_test_mark",

            "rough_record_mark",
            "fair_record_mark",
            "lab_work_mark",
            "open_ended_mark",
            "attendance_mark",

            "total_lab_mark"

            ]
        
    def get_average_test_mark(self, obj):
        test1 = obj.test1 or 0
        test2 = obj.test2 or 0

        total_marks = test1 + test2
        return total_marks / 2
    
    
    def get_total_lab_mark(self, obj):
        average_test_mark = self.get_average_test_mark(obj)
        rough_record_mark = obj.rough_record_mark or 0
        fair_record_mark = obj.fair_record_mark or 0
        lab_work_mark = obj.lab_work_mark or 0
        open_ended_mark = obj.open_ended_mark or 0
        attendance_mark = obj.attendance_mark or 0


        total_internal_mark = average_test_mark + rough_record_mark + lab_work_mark + fair_record_mark + open_ended_mark + attendance_mark

        return total_internal_mark




class SemesterCountSerializer(serializers.Serializer):
    semester_name = serializers.CharField()
    semester_id = serializers.IntegerField()
    teachers_count = serializers.IntegerField()
    students_count = serializers.IntegerField()
    subjects_count = serializers.IntegerField()