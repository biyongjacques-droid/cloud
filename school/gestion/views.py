from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .form import Custom, NoteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def inscription(request):
    form = Custom()
    if request.method == 'POST':
        form = Custom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            role = form.cleaned_data['role']
            profil = Profil.objects.create(user=user)
            
            if role == 'student':
                profil.is_student = True
                profil.save()
                Etudiant.objects.create(user=user, matricule=f"M-{user.id}", Classe=form.cleaned_data.get('classe', ''))
            elif role == 'teacher':
                profil.is_teacher = True
                profil.save()
                Enseignant.objects.create(user=user, specialite="")
            messages.success(request, "compte créé avec succès!!! vous pouvez maintenant vous connecter")
            return redirect('connexion')
        else:
            messages.error(request, "veuillez corriger les erreurs ci dessous.")
    
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profil = Profil.objects.get(user=user)
            if profil.is_student:
                return redirect('student_dashboard')
            elif profil.is_teacher:
                return redirect('teacher_dashboard')
            messages.success(request, "Connexion réussie!")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')

@login_required
def student_dashboard(request):
    profil = Profil.objects.get(user=request.user)
    etudiant = Etudiant.objects.get(user=request.user)
    notes = Note.objects.filter(etudiant=etudiant)
    return render(request, 'student_dashboard.html', {'profil': profil, 'etudiant': etudiant, 'notes': notes})


@login_required
def teacher_dashboard(request):
    profil = Profil.objects.get(user=request.user)
    enseignant = Enseignant.objects.get(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            etudiant = form.cleaned_data.get('etudiant')
            matiere_name = form.cleaned_data.get('matiere')
            valeur = form.cleaned_data.get('valeur')
            
            matiere, _ = Matiere.objects.get_or_create(nom=matiere_name.strip(), enseignant=enseignant)
            note = Note.objects.create(etudiant=etudiant, matiere=matiere, Valeur=valeur)
            messages.success(request, "Note ajoutée avec succès!")
            return redirect('teacher_dashboard')
    else:
        form = NoteForm()

    return render(request, 'teacher_dashboard.html', {'profil': profil, 'enseignant': enseignant, 'form': form})        