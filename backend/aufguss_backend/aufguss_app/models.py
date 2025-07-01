from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
import uuid

class SaunaUser(models.Model):
    """
    Erweitertes Benutzerprofil für Saunamitarbeiter
    Jeder Benutzer erhält eine individuelle Farbe und optional einen Avatar
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = ColorField(default='#FF0000')  # Standardfarbe ist Rot
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Für Whitelist-Funktion
    is_permanent_admin = models.BooleanField(default=False)  # Für unveränderliche Admin-Rechte
    full_name = models.CharField(max_length=100)  # Echter Name für Anzeige
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.full_name

class AufgussSession(models.Model):
    """
    Repräsentiert einen einzelnen Sauna-Aufguss mit Zeitslot und Ersteller
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(SaunaUser, on_delete=models.CASCADE, related_name='aufguesse')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Aufguss'
        verbose_name_plural = 'Aufgüsse'
    
    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%d.%m.%Y, %H:%M')}"

class ChatMessage(models.Model):
    """
    Speichert Chat-Nachrichten zwischen Teammitgliedern
    """
    sender = models.ForeignKey(SaunaUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender} - {self.timestamp.strftime('%d.%m.%Y, %H:%M')}"
