from django.urls import path
from django.views.defaults import permission_denied
from . import views

handler403 = permission_denied
urlpatterns = [
    path("", 
         views.get_inbox, 
         name="inbox"
         ),
    path("outbox/", 
         views.get_outbox, 
         name="outbox"
         ),
    path("important/", 
         views.get_important, 
         name="important"
         ),
    path("delete/<int:id>", 
         views.delete_email, 
         name="delete_email"
         ),
    path("important/<int:id>", 
         views.email_is_important, 
         name="email_is_important"
         ),
    path("detail/<int:id>", 
         views.get_email_details, 
         name="email_detail"
         ),
    path(
        "sent_detail/<int:id>", 
        views.get_sent_email_details, 
        name="sent_email_detail"
    ),
    path("new_email/", 
         views.create_email, 
         name="create_email"
         ),
]
