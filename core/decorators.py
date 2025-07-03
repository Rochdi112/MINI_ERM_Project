from django.contrib.auth.decorators import user_passes_test

def role_required(role):
    """
    Décorateur pour n’autoriser que les utilisateurs authentifiés
    ayant un ProfilUtilisateur.role == role.
    """
    def check_role(user):
        return (
            user.is_authenticated
            and hasattr(user, 'profilutilisateur')
            and user.profilutilisateur.role == role
        )
    return user_passes_test(check_role)
