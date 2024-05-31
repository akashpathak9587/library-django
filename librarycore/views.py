from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Student, Branch, Book, Issue
from datetime import date

admin = False
login_id = None

def index(request):
    global admin, login_id
    admin = False
    login_id = None
    return render(request, 'index.html')

def admin_signup(request):
    global admin, login_id
    admin = False
    login_id = None
    if request.method == 'POST':
        try:
            name = request.POST['name']
            password = request.POST['password']
            user = User.objects.create_user(username=name, email=name, password=password)
            user.save()
            return redirect('login')
        except:
            return render(request, 'admin_signup.html', {'error':'User already exists'})
    else:
        return render(request, 'admin_signup.html')

def student_signup(request):
    global admin, login_id
    admin = False
    login_id = None
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            branch = request.POST['branch']
            semester = request.POST['semester']
            password = request.POST['password']
            branch = Branch.objects.get(name=branch)
            s1 = Student(name=name, email=email, branch=branch, password=password, semester=semester)
            s1.save()
            return redirect('login')
        except Exception as e:
            branches = Branch.objects.all()
            return render(request, 'student_signup.html', {'error':e, 'branches':branches})
    else:
        branches = Branch.objects.all()
        return render(request, 'student_signup.html', {'branches':branches})

def login(request):
    global admin, login_id
    admin = False
    login_id = None
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                admin = True
                login_id = user.id
                return redirect('dashboard')
            student = Student.objects.get(email=username, password=password)
            if student is not None:
                login_id = student.id
                return redirect('dashboard')
        except Exception as e:
                return render(request, 'login.html', {'error':e})
    else:
        return render(request, 'login.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    global admin, login_id
    if admin:
        try:
            user = User.objects.get(id=login_id)
            return render(request, 'dashboard.html', {'user':user})
        except Exception as e:
            return render(request, 'login.html', {'error':e})
    elif login_id is not None:
        try:
            student = Student.objects.get(id=login_id)
            return render(request, 'student_dashboard.html', {'student':student})
        except Exception as e:
            return render(request, 'login.html', {'error':e})
    else:
        return redirect('login')

def add_book(request):
    global admin
    if admin:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                author = request.POST['author']
                branch = request.POST['branch']
                branch = Branch.objects.get(name=branch)
                b1 = Book(name=name, author=author, branch=branch)
                b1.save()
                branches = Branch.objects.all()
                return render(request, 'add_book.html', {'success':'Book added successfully', 'branches':branches})
            except Exception as e:
                branches = Branch.objects.all()
                return render(request, 'add_book.html', {'error':e, 'branches':branches})
        else:
            branches = Branch.objects.all()
            return render(request, 'add_book.html', {'branches': branches})
    else:
        return redirect('login')

def add_student(request):
    global admin
    if admin:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                email = request.POST['email']
                branch = request.POST['branch']
                semester = request.POST['semester']
                password = request.POST['password']
                branch = Branch.objects.get(name=branch)
                s1 = Student(name=name, email=email, branch=branch, password=password, semester=semester)
                s1.save()
                branches = Branch.objects.all()
                return render(request, 'add_student.html', {'success':'Student added successfully', 'branches':branches})
            except Exception as e:
                branches = Branch.objects.all()
                return render(request, 'add_student.html', {'error':e, 'branches':branches})
        else:
            branches = Branch.objects.all()
            return render(request, 'add_student.html', {'branches': branches})
    else:
        return redirect('login')

def add_branch(request):
    global admin
    if admin:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                branch = Branch(name=name)
                branch.save()
                return render(request, 'add_branch.html', {'success':'Branch added successfully'})
            except Exception as e:
                return render(request, 'add_branch.html', {'error':e})
        else:
            return render(request, 'add_branch.html')
    else:
        return redirect('login')
    
def issue_book(request):
    global admin
    if admin:
        if request.method == 'POST':
            try:
                book = request.POST['book']
                student = request.POST['student']
                return_date = request.POST['date']
                book = Book.objects.get(name=book)
                student = Student.objects.get(email=student)
                issue = Issue(book=book, student=student, return_date=return_date)
                issue.issue_date = date.today()
                issue.save()
                return render(request, 'issue_book.html', {'success':'Book issued successfully'})
            except Exception as e:
                students = Student.objects.all()
                books = Book.objects.all()
                return render(request, 'issue_book.html', {'error':e,'students':students, 'books':books})
        else:
            return render(request, 'issue_book.html')
    else:
        return redirect('login')

def view_books(request):
    global admin, login_id
    if admin:
        books= Book.objects.all()
        return render(request, 'view_books.html', {'books': books})
    elif login_id is not None:
        books = Book.objects.all()
        return render(request, 'student_view_books.html', {'books': books})
    else:
        return redirect('login')

def view_students(request):
    global admin
    if admin:
        students = Student.objects.all()
        return render(request, 'view_students.html', {'students': students})
    else:
        return redirect('login')

def view_issued_books(request):
    global admin, login_id
    if admin:
        issues = Issue.objects.all()
        return render(request, 'view_issued_books.html', {'issues':issues})
    elif login_id is not None:
        issues = Issue.objects.filter(student=login_id)
        return render(request, 'view_student_issued_books.html', {'issues':issues})
    else:
        return redirect('login')

def edit_book(request, id):
    global admin
    if admin:
        if request.method == 'POST':
            name = request.POST['name']
            author = request.POST['author']
            branch = request.POST['branch']
            branch = Branch.objects.get(name=branch)
            book = Book.objects.get(id=id)
            book.name = name
            book.author = author
            book.branch = branch
            book.save()
            return redirect('view_books')
        else:
            book = Book.objects.get(id=id)
            branches = Branch.objects.all()
        return render(request, 'edit_book.html', {'book':book, 'branches':branches})
    else:
        return redirect('login')

def edit_student(request, id):
    global admin
    if admin:
        if request.method == 'POST':
            name = request.POST['name']
            branch = request.POST['branch']
            semester = request.POST['semester']
            branch = Branch.objects.get(name=branch)
            student = Student.objects.get(id=id)
            student.name = name
            student.branch = branch
            student.semester = semester
            student.save()
            return redirect('view_students')
        else:
            student = Student.objects.get(id=id)
            branches = Branch.objects.all()
            return render(request, 'edit_student.html', {'student':student, 'branches':branches})
    else:
        return redirect('login')

def edit_issue(request, id):
    global admin
    if admin:
        if request.method == 'POST':
            book = request.POST['book']
            student = request.POST['student']
            return_date = request.POST['date']
            book = Book.objects.get(name=book)
            student = Student.objects.get(email=student)
            issue = Issue.objects.get(id=id)
            issue.book = book
            issue.student = student
            issue.return_date = return_date
            issue.save()
            return redirect('view_issued_books')
        else:
            issue = Issue.objects.get(id=id)
            students = Student.objects.all()
            books = Book.objects.all()
            return render(request, 'edit_issue.html', {'issue':issue,'students':students, 'books':books})
    else:
        return redirect('login')

def delete_book(request, id):
    global admin
    if admin:
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('view_books')
    else:
        return redirect('login')

def delete_student(request, id):
    global admin
    if admin:
        student = Student.objects.get(id=id)
        student.delete()
        return redirect('view_students')
    else:
        return redirect('login')

def delete_issue(request, id):
    global admin
    if admin:
        issue = Issue.objects.get(id=id)
        issue.delete()
        return redirect('view_issued_books')
    else:
        return redirect('login')

def return_book(request):
    global admin
    if admin:
        if request.method == 'POST':
            try:
                book = request.POST['book']
                student = request.POST['student']
                book = Book.objects.get(name=book)
                student = Student.objects.get(email=student)
                issue = Issue.objects.get(book=book, student=student)
                issue.delete()
                return render(request,'return_book.html', {'success':'Book returned successfully'})
            except Exception as e:
                return render(request,'return_book.html', {'error':e})
        else:
            return render(request,'return_book.html')
    else:
        return redirect('login')

def modify_student(request):
    global login_id
    if login_id is not None:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                branch = request.POST['branch']
                semester = request.POST['semester']
                branch = Branch.objects.get(name=branch)
                student = Student.objects.get(id=login_id)
                student.name = name
                student.branch = branch
                student.semester = semester
                student.save()
                branches = Branch.objects.all()
                return render(request, 'modify_student.html', {'success':'Student edited successfully', 'branches':branches, 'student':student})
            except Exception as e:
                branches = Branch.objects.all()
                student = Student.objects.get(id=login_id)
                return render(request,'modify_student.html', {'error':e, 'branches':branches, 'student':student})
        else:
            student = Student.objects.get(id=login_id)
            branches = Branch.objects.all()
            return render(request, 'modify_student.html', {'student':student, 'branches':branches})
    else:
        return redirect('login')