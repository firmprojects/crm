from django.db import models
from django.conf import settings
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField





class Clients(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=20, blank=False, null=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    photo = models.ImageField(default='default.jpg', upload_to='clients_pics')
    clients_id = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.company_name

    @property
    def projects(self):
        return self.projects_set.all()

    def get_absolute_url(self):
        return reverse('project:clients')





class Projects(models.Model):
    PRIORITY = ( ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), )
    STATUS = ( ('working', 'Working'), ('pending', 'Pending'), ('suspended', 'Suspended'), ('cancelled', 'cancelled'),)

    clients = models.ForeignKey(Clients,  on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    project_cost = models.PositiveIntegerField()
    priority = models.CharField(max_length=50, choices=PRIORITY)
    status = models.CharField(max_length=50, choices=STATUS)
    project_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leader_set', blank=True, null=True)
    team_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_set', blank=True, null=True)

    description = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project:projects')



