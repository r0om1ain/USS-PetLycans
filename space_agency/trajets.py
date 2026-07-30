def assurer_coordonnees(missions):
    for mission in missions:
        lieu = mission.destination
        if lieu.x is None or lieu.y is None:
            lieu.x, lieu.y = lieu.coords_depuis_nom()
            lieu.save()


def optimiser_trajet(missions):
    if len(missions) == 0:
        return {"ordre": [], "distance_totale": 0, "etapes": []}

    assurer_coordonnees(missions)

    ordre = [missions[0]]
    restants = list(missions[1:])
    etapes = []
    distance_totale = 0

    while len(restants) > 0:
        actuel = ordre[-1]

        meilleure = restants[0]
        meilleure_distance = actuel.destination.distance_vers(meilleure.destination)

        for mission in restants:
            distance = actuel.destination.distance_vers(mission.destination)
            if distance < meilleure_distance:
                meilleure = mission
                meilleure_distance = distance

        etapes.append(
            {
                "de": actuel,
                "vers": meilleure,
                "distance": meilleure_distance,
            }
        )
        distance_totale = distance_totale + meilleure_distance
        ordre.append(meilleure)
        restants.remove(meilleure)

    return {
        "ordre": ordre,
        "distance_totale": distance_totale,
        "etapes": etapes,
    }


def resultat_en_dict(vaisseau, resultat):
    ordre = []
    for mission in resultat["ordre"]:
        lieu = mission.destination
        ordre.append(
            {
                "mission_id": mission.id,
                "lieu": lieu.nom,
                "x": lieu.x,
                "y": lieu.y,
                "statut": mission.statut,
            }
        )

    etapes = []
    for etape in resultat["etapes"]:
        etapes.append(
            {
                "de": etape["de"].destination.nom,
                "vers": etape["vers"].destination.nom,
                "distance": etape["distance"],
            }
        )

    return {
        "vaisseau_id": vaisseau.id,
        "vaisseau": vaisseau.nom,
        "ordre": ordre,
        "distance_totale": resultat["distance_totale"],
        "etapes": etapes,
    }
