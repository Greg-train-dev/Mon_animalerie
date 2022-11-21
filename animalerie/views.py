from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipement
from .models import Animal
from .models import Image
from .forms import MoveForm

def animal_list(request):
    animaux = Animal.objects.order_by('id_animal')
    equipement = Equipement.objects.order_by('id_equip')
    return render(request, 'animalerie/animal_list.html', {'animaux': animaux, 'equipement': equipement})


def equipement_list(request):
    equipement = Equipement.objects.order_by('id_equip')
    return render(request, 'animalerie/animal_list.html', {'equipement': equipement})


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if request.method == "POST":
        form=MoveForm(request.POST, instance=animal)
        if form.is_valid():
            if form.data['lieu'] == "salle commune":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                form.save(commit=False)
                if animal.etat == "Endormi":
                    animal.etat = "Affamé"
                    animal.save()
                    return redirect('animal_detail', id_animal=id_animal)
                else:
                    animal.save()
                    return redirect('animal_detail', id_animal=id_animal)
                
            elif form.data['lieu'] == "salle d'entraînement":
                form.save(commit=False)
                if animal.etat == "Repus":
                    if animal.lieu.disponibilite == "libre":
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        animal.etat = "Fatigué"
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé la salle d'entraînement est occupée."})
                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} a trop faim pour s'entraîner."})

            elif form.data['lieu'] == "cantina":
                form.save(commit=False)
                if  animal.etat == "Affamé":
                    if animal.lieu.disponibilite == "libre":
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        animal.etat = "Repus"
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé la cantina est occupée."})

                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas faim."})


            else :
                form.save(commit=False)
                if animal.etat == "Fatigué":
                    if animal.lieu.disponibilite == "libre":
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        animal.etat = "Endormi"
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé le dortoir est occupé."})
                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas envie de se reposer."})

        else:
            form = MoveForm()
            return render(request,
                    'animalerie/animal_detail.html',
                    {'animal': animal, 'lieu': animal.lieu, 'form': form})
    else:
        form = MoveForm()
        return render(request,
                'animalerie/animal_detail.html',
                {'animal': animal, 'lieu': animal.lieu, 'form': form})
