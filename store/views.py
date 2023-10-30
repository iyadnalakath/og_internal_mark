from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from projectaccount.models import Account, Subject,Semester
from store.models import LabInternalMark, Student, TheoryInternalMark
from store.serializer import LabInternalMarkSerializer, RegisterStudentSerializer, RegisterTeacherSerializer, SemesterCountSerializer, SemesterSerializer, SubjectSerializer, TheoryInternalMarkSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from rest_framework.views import APIView
# Create your views here.


class SubjectViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        semester_id = self.request.query_params.get('semester_id')
        if semester_id:
            queryset = self.get_queryset().filter(semester_id=semester_id)
        else:
            if self.request.user.role == "teacher":
                queryset = self.request.user.subject.all()
            else:
                queryset = self.get_queryset()

        serializer = SubjectSerializer(
            queryset, many=True, context={"request": self.request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class SemesterViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SemesterSerializer

    def get_queryset(self):
        user = self.request.user

        # Check if the user has an admin role
        if user.role == 'admin':
            return Semester.objects.all()

        # Get the subjects associated with the teacher
        subjects = user.subject.all()

        # Get the semesters associated with those subjects
        semesters = Semester.objects.filter(semester_subject__in=subjects).distinct()

        return semesters
    # def list(self, request, *args, **kwargs):
    #         queryset = self.get_queryset()

    #         if self.request.user.role == "teacher":
    #             # if self.request.GET.get("exam_name"):
    #                 # exam_name = self.request.GET.get("exam_name")
    #             # queryset = queryset.filter(exam_name=exam_name)

    #             queryset = queryset.filter(name=self.request.user.subject__semester.name)
    #             serializer = SemesterSerializer(
    #                 queryset, many=True, context={"request": self.request}
    #             )
    #             return Response(serializer.data, status=status.HTTP_200_OK)

    #         else:
    #             return super().list(request, *args, **kwargs)
          



class TeacherRegistrationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = Account.objects.all()
    serializer_class = RegisterTeacherSerializer

    def get_queryset(self):
        return Account.objects.filter(role="teacher")


class StudentRegistrationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = Student.objects.all()
    serializer_class = RegisterStudentSerializer

    def get_queryset(self):
        semester_id = self.request.query_params.get('semester_id')

        if semester_id:
            return Student.objects.filter(semester_id=semester_id)

        return Student.objects.all()



class TheoryInternalMarkViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = TheoryInternalMark.objects.all()
    serializer_class = TheoryInternalMarkSerializer

    def get_queryset(self):
            queryset = TheoryInternalMark.objects.all()
            student_id = self.request.query_params.get('student_id')
            subject_id = self.request.query_params.get('subject_id')

            if student_id and subject_id:
                queryset = queryset.filter(student=student_id, subject=subject_id)

            return queryset


class LabInternalMarkViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset = LabInternalMark.objects.all()
    serializer_class = LabInternalMarkSerializer

    def get_queryset(self):
        queryset = LabInternalMark.objects.all()
        student_id = self.request.query_params.get('student_id')
        subject_id = self.request.query_params.get('subject_id')

        if student_id and subject_id:
            queryset = queryset.filter(student=student_id, subject=subject_id)

        return queryset




# class StudentSubjectMarksViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TheoryInternalMarkSerializer
#     queryset = TheoryInternalMark.objects.all()
#     def list(self, request, *args, **kwargs):
#         semester_id = self.request.query_params.get('semester_id')
        
#         # Get all students for the given semester
#         students = Student.objects.filter(semester=semester_id)

#         student_data = []

#         for student in students:
#             # Get theory internal marks for the student in the given semester
#             theory_marks = TheoryInternalMark.objects.filter(student=student, semester=semester_id)

#             # Get lab internal marks for the student in the given semester
#             lab_marks = LabInternalMark.objects.filter(student=student, semester=semester_id)

#             # Serialize the data
#             theory_serializer = TheoryInternalMarkSerializer(theory_marks, many=True)
#             lab_serializer = LabInternalMarkSerializer(lab_marks, many=True)

#             student_data.append({
#                 'student_name': student.name,
#                 'register_number': student.register_number,
#                 'theory_marks': theory_serializer.data,
#                 'lab_marks': lab_serializer.data,
#             })

#         return Response(student_data)

#
class StudentSubjectMarks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        semester_id = self.request.query_params.get('semester_id')

        students = Student.objects.filter(semester=semester_id)

        student_data = []

        for student in students:
            theory_marks = TheoryInternalMark.objects.filter(student=student, semester=semester_id)
            lab_marks = LabInternalMark.objects.filter(student=student, semester=semester_id)

            theory_serializer = TheoryInternalMarkSerializer(theory_marks, many=True)
            lab_serializer = LabInternalMarkSerializer(lab_marks, many=True)

            student_data.append({
                'student': RegisterStudentSerializer(student).data,
                'theory_marks': theory_serializer.data,
                'lab_marks': lab_serializer.data,
            })

        return Response(student_data)
    

class SemesterCountAPIView(APIView):
    def get(self, request, format=None):
        semesters = Semester.objects.all()
        counts = []

        for semester in semesters:
            teachers_count = Account.objects.filter(role='teacher', subject__semester=semester).count()
            students_count = Student.objects.filter(semester=semester).count()
            subjects_count = Subject.objects.filter(semester=semester).count()

            counts.append({
                'semester_name': semester.name,
                'semester_id': semester.id,
                'teachers_count': teachers_count,
                'students_count': students_count,
                'subjects_count': subjects_count
            })

        serializer = SemesterCountSerializer(counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)