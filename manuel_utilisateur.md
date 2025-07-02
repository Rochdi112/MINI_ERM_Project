# Manuel Utilisateur – MINI ERP MIF Maroc

## 🔐 Connexion
- Accès via `/admin/` pour administrateur
- Accès technicien/client via interfaces dédiées (HTMX)

## 👤 Gestion des Clients
- Ajouter / Modifier / Supprimer
- Accès à l’historique des interventions

## 👨‍🔧 Techniciens
- Liste des techniciens
- Gestion des compétences
- Assignation aux interventions

## 🧰 Matériels
- Suivi des matériels par référence
- Statut (disponible, affecté, en panne…)

## 📅 Interventions
- Planifier intervention (date, lieu, technicien)
- Suivi et état (en cours / terminée)
- Historique interventions client

## 📝 Rapports
- Formulaire post-intervention
- Génération automatique PDF
- Stockage dans `media/rapports/`

## 📊 Dashboard
- Vue globale : nb interventions, clients, techniciens
- Statistiques & KPIs

## 📁 Export
- Export PDF par intervention
- Historique accessible client

---

**Astuce :** Toutes les actions s’effectuent sans rechargement grâce à HTMX.