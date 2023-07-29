from django.contrib.sessions.models import Session

#verificar la sesion del usuario con su sesion id
def verificar_sesion(session_id):
    try:
        session = Session.objects.get(session_key=session_id)
        data = session.get_decoded()
        user_id = data.get('_auth_user_id', None)
        return user_id
    except Session.DoesNotExist:
        return None
