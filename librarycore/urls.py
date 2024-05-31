from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_signup', views.admin_signup, name='admin'),
    path('student_signup', views.student_signup, name='student'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('view_books', views.view_books, name='view_books'),
    path('add_book', views.add_book, name='add_book'),
    path('view_students', views.view_students, name='view_students'),
    path('add_student', views.add_student, name='add_student'),
    path('view_issued_books', views.view_issued_books, name='view_issued_books'),
    path('issue_book', views.issue_book, name='issue_book'),
    path('logout', views.logout, name='logout'),
    path('edit_book/<int:id>', views.edit_book, name='edit_book'),
    path('delete_book/<int:id>', views.delete_book, name='delete_book'),
    path('edit_student/<int:id>', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>', views.delete_student, name='delete_student'),
    path('add_branch', views.add_branch, name='add_branch'),
    path('return_book', views.return_book, name='return_book'),
    path('edit_issue/<int:id>', views.edit_issue, name='edit_issue'),
    path('delete_issue/<int:id>', views.delete_issue, name='delete_issue'),
    path('modify_student', views.modify_student, name='modify_student'),
]