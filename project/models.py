from django.db import models
from django.conf import settings
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres import fields
from django.utils import timezone
from django.utils.crypto import get_random_string


def generate_project_id():
    id = get_random_string(length=4)
    return "PR-"+str(id)


def generate_client_id():
    id = get_random_string(length=4)
    return "CL-"+str(id)


class Clients(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=20, blank=False, null=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    photo = models.ImageField(default='clients_pics/passport.jpg',
                              upload_to='clients_pics', blank=True)
    clients_id = models.CharField(
        max_length=20, unique=True, default=generate_client_id)
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)

    def __str__(self):
        return self.company_name

    @property
    def projects(self):
        return self.projects_set.all()

    def get_absolute_url(self):
        return reverse('project:clients')


class Projects(models.Model):
    PRIORITY = (('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), )
    STATUS = (('working', 'Working'), ('pending', 'Pending'),
              ('suspended', 'Suspended'), ('cancelled', 'cancelled'),)

    clients = models.ForeignKey(
        Clients,  on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    project_cost = models.FloatField(blank=True, null=True)
    budget = models.FloatField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, blank=True)
    project_leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leader_set', blank=True, null=True)
    team_member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='team_set', blank=True)
    planning = models.ForeignKey(
        'Planning', on_delete=models.CASCADE, blank=True, null=True)
    design = models.ForeignKey(
        'Design', on_delete=models.CASCADE, blank=True, null=True)
    development = models.ForeignKey(
        'Development', on_delete=models.CASCADE, blank=True, null=True)
    testing = models.ForeignKey(
        'Testing', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project_id = models.CharField(
        unique=True, default=generate_project_id, max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project:projects')

    def get_task_number(self):
        complete = self.milestone_set.all().filter(completed=True)
        in_complete = self.milestone_set.all().filter(completed=False)
        return {"complete": len(complete), "in_complete": len(in_complete)}

    def get_progress(self):
        try:

            return min(max(((timezone.localdate() - self.start_date).total_seconds()/(self.end_date - self.start_date).total_seconds())*100, 0), 100)
        except ZeroDivisionError:
            return 0

    def get_tasks(self):
        d = {'completed': 0, 'in_complete': 0}
        for i in self.milestone_set.all():
            if i.completed:
                d['completed'] += 1
            else:
                d['in_complete'] += 1

        return d


class Comment(models.Model):
    text = models.TextField()
    commented_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commented_on = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)


class ImageUpload(models.Model):
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to='images/')


class DocUpload(models.Model):
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    doc = models.FileField(blank=True, null=True, upload_to='document/')


class Milestone(models.Model):
    task = models.CharField(max_length=200)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)
    milestone_followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='milestone_followers',)
    milestone_assignes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='milestone_assignes',)

    def __str__(self):
        return self.task

    def assigned_to(self):
        name = f'{self.task} assigned to: '
        for i in self.milestone_assignes.all():
            name += f"{i.username}  "
        print(name)
        return name

    def followers_to(self):
        name = f'{self.task} followed by: '
        for i in self.milestone_followers.all():
            name += f"{i.username}  "
        print(name)
        return name


class IssuesTable(models.Model):
    project = models.ManyToManyField(Projects)
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="staff_issues")
    client = models.ManyToManyField(Clients, related_name="client_issues")
    issues_start_date = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.project.name} issues"

    class Meta:
        verbose_name = 'Issues Table'
        verbose_name_plural = 'Issues Table'


class RiskTable(models.Model):
    project = models.ManyToManyField(Projects)
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="staff_risk")
    client = models.ManyToManyField(Clients, related_name="client_risks")
    issues_start_date = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.project.name} Risks"

    class Meta:
        verbose_name = 'Risk Table'
        verbose_name_plural = 'Risk Table'


class BudgetRisk(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    amount_budgetted = models.FloatField()
    amount_spent = models.FloatField()
    amount_over_budget = models.FloatField()

    def __str__(self):
        return f"{self.project.name} amount budgeted - {self.amount_budgetted}"


class Planning(models.Model):
    PLANNING_STATUS = (
        ('not_set', 'Not Set'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    )
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=150, choices=PLANNING_STATUS, default="not_set")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.deadline

    class Meta:
        verbose_name = 'Planning'
        verbose_name_plural = 'Plannings'


class Design(models.Model):
    DESIGN_STATUS = (
        ('not_set', 'Not Set'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    )
    deadline = models.DateTimeField()
    status = models.CharField(max_length=150, choices=DESIGN_STATUS)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.deadline

    class Meta:
        verbose_name = 'Design'
        verbose_name_plural = 'Design'


class Development(models.Model):
    DEVELOPMENT_STATUS = (
        ('not_set', 'Not Set'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    )
    deadline = models.DateTimeField()
    status = models.CharField(max_length=150, choices=DEVELOPMENT_STATUS)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.deadline

    class Meta:
        verbose_name = 'Development'
        verbose_name_plural = 'Development'


class Testing(models.Model):
    TESTING_STATUS = (
        ('not_set', 'Not Set'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    )
    deadline = models.DateTimeField()
    status = models.CharField(max_length=150, choices=TESTING_STATUS)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.deadline

    class Meta:
        verbose_name = 'Testing'
        verbose_name_plural = 'Testing'
