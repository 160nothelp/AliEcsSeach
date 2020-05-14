from django.contrib import admin

from .models import TicketType, WorkTicket, TicketComment, TicketEnclosure


admin.site.register(TicketType)
admin.site.register(WorkTicket)
admin.site.register(TicketComment)
admin.site.register(TicketEnclosure)
