import json
import uuid

import digitalocean
from decouple import config
from django.db import models
from django.contrib.postgres.fields import JSONField

# from frontend.models import candidatesprojects as CandidateProjects
from frontend.models import Assessment as CandidateProjects
# from transactions.models import EnterpriseCandidateProjects

# Create your models here.
DO_TOKEN = config('DO_TOKEN', default='DO_TOKEN')
DO_DOMAIN = config('DO_DOMAIN', default='DO_DOMAIN')


class ServerConfig(models.Model):
    TYPE_CHOICES = (
        ('ide_server_config', 'IDE server config'),
    )
    snapshot_image = models.CharField(max_length=140, blank=True)
    region = models.CharField(max_length=140, blank=True)
    size_slug = models.CharField(max_length=140, blank=True)
    type = models.CharField(max_length=140, default='ide_server_config', choices=TYPE_CHOICES, unique=True)

    # def create_server(self, workspace_name):su - codeln
    # export HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
    # export PUBLIC_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
    # cd /home/codeln/chuck/
    # source venv/bin/activate
    # git pull
    # pip install -r requirements.txt
    # python manage.py migrate
    # echo \"
    # HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
    # ALLOWED_HOSTS=.codeln.com,localhost,.codeln.com,$PUBLIC_IPV4\" > /home/codeln/chuck/.env
    # sudo systemctl start gunicorn
    # sudo systemctl enable gunicorn
    # echo \"
    # server {
    #    listen 80;
    #    server_name $PUBLIC_IPV4 $HOSTNAME;
    #    location = /favicon.ico { access_log off; log_not_found off; }
    #    location /static/ {
    #        root /home/codeln/chuck;
    #    }
    #    location / {
    #        include proxy_params;
    #        proxy_pass http://unix:/home/codeln/chuck/chuck.sock;
    #    }
    # }\" > /etc/nginx/sites-available/chuck
    # sudo ln -s /etc/nginx/sites-available/chuck /etc/nginx/sites-enabled
    # sudo systemctl restart nginx
    # sudo ufw allow 'Nginx Full'
    # echo Codeln_2018# | sudo -S ufw allow ssh
    # export HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
    # export PUBLIC_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
    # cd /home/codeln/chuck/
    # git pull
    # echo \"
    # HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
    # ALLOWED_HOSTS=.codeln.com,localhost,.codeln.com,$PUBLIC_IPV4
    # MACHINE=127.0.0.1
    # PASW=Codeln_2018#
    # DB_NAME=idedatabase
    # DB_USER=codelncandidate
    # DB_PASSWORD=wzxykb1gslvP&7$nd
    # DB_HOST=localhost
    # DB_PORT=5432
    # SECRET_KEY =@lgy8ec_h @5hjhrmqx$t(d1!v__soufztb85jfe$-v6d$$lqk(
    # DEBUG=True
    # JENKINS_IP=178.62.235.155
    # JENKINS_PATH=/var/lib/jenkins/workspace
    # JENKINS_PORT=22
    # JENKINS_USER=root
    # JENKINS_PASW=Codeln_2018#
    # JENKINS_TOKEN=113e1546e2c0046919b7434d8326adcc94
    # JENKINS_URL=phil.codeln.com
    # JENKINS_USER_ID=ide
    # ROOT_IMAGE_NAME=eclipse/che
    # IDE_PASSWORD=plx&*$ja\" > /home/codeln/chuck/.env
    # sudo systemctl restart gunicorn
    # sudo ufw default deny incoming
    # sudo ufw default allow outgoing
    # sudo ufw --force enable
    # sudo ufw allow http
    # sudo ufw allow https
    # sudo ufw allow 32768:65535/tcp
    # sudo curl -sSL https://get.docker.com/ | sh
    # sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -v ~:/data eclipse/che:6.7.0 start
    # echo Completed
    def create_server(self):
        domain_name = uuid.uuid4()
        droplet = digitalocean.Droplet(token=DO_TOKEN,
                                       name=f'{domain_name}.{DO_DOMAIN}',
                                       image=self.snapshot_image,
                                       region='nyc1',
                                       size_slug=self.size_slug,
                                       user_data=
"""#!/bin/bash
su - codeln
export HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
export PUBLIC_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
cd /home/codeln/chuck/
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
echo \"
HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
ALLOWED_HOSTS=.codeln.com,localhost,.cesithompson.com,$PUBLIC_IPV4\" > /home/codeln/chuck/.env
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
echo \"
server {
 listen 80;
   server_name $PUBLIC_IPV4 $HOSTNAME *.codeln.com *.goodtalent.dev;
 location = /favicon.ico { access_log off; log_not_found off; }
 location /static/ {
 root /home/codeln/chuck;
 }
 location / {
 include proxy_params;
 proxy_pass http://unix:/home/codeln/chuck/chuck.sock;
 }
}\" > /etc/nginx/sites-available/chuck
sudo ln -s /etc/nginx/sites-available/chuck /etc/nginx/sites-enabled
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
echo Codeln_2018# | sudo -S ufw allow ssh
export HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
export PUBLIC_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
cd /home/codeln/chuck/
git pull
echo \"
HOSTNAME=$(curl -s http://169.254.169.254/metadata/v1/hostname)
ALLOWED_HOSTS=.codeln.com,localhost,.cesithompson.com,$PUBLIC_IPV4
MACHINE=127.0.0.1
PASW=Codeln_2018#
DB_NAME=idedatabase
DB_USER=codelncandidate
DB_PASSWORD=wzxykb1gslvP&7$nd
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY =@lgy8ec_h @5hjhrmqx$t(d1!v__soufztb85jfe$-v6d$$lqk(
DEBUG=True
JENKINS_IP=178.62.235.155
JENKINS_PATH=/var/lib/jenkins/workspace
JENKINS_PORT=22
JENKINS_USER=root
JENKINS_PASW=Codeln_2018#
JENKINS_TOKEN=113e1546e2c0046919b7434d8326adcc94
JENKINS_URL=phil.codeln.com
JENKINS_USER_ID=ide
ROOT_IMAGE_NAME=eclipse/che
IDE_PASSWORD=plx&*$ja\" > /home/codeln/chuck/.env
sudo systemctl restart gunicorn
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw --force enable
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 32768:65535/tcp
sudo curl -sSL https://get.docker.com/ | sh
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -v ~:/data eclipse/che:6.7.0 start
echo Completed""")
        droplet.create()
        return droplet.id, domain_name

    def __str__(self):
        return self.get_type_display()


class Server(models.Model):
    url = models.URLField(blank=True, unique=True)
    is_free = models.BooleanField(default=True)
    ip_address = models.CharField(max_length=140, blank=True)
    machine_id = models.CharField(max_length=140, blank=True)
    setup_code = models.CharField(max_length=140, blank=True, unique=True)
    decommissioned = models.BooleanField(default=False)

    def get_create_status(self):
        manager = digitalocean.Manager(token=DO_TOKEN)
        droplet = manager.get_droplet(self.machine_id)
        if droplet.ip_address is not None:
            self.ip_address = droplet.ip_address
            self.save()
            return True
        else:
            return False

    def assign_domain(self, domain_name):
        domain = digitalocean.Domain(token=DO_TOKEN, name=DO_DOMAIN)
        domain.create_new_domain_record(type='A', name=domain_name, data=self.ip_address)

    def unassign_domain(self, domain_name):
        domain = digitalocean.Domain(token=DO_TOKEN, name=DO_DOMAIN)
        records = domain.get_records()
        for record in records:
            if record.name == domain_name:
                record.destroy()
                return True
            else:
                return False

    def shutdown_droplet(self):
        manager = digitalocean.Manager(token=DO_TOKEN)
        droplet = manager.get_droplet(self.machine_id)
        droplet.shutdown()

    def delete_droplet(self):
        manager = digitalocean.Manager(token=DO_TOKEN)
        droplet = manager.get_droplet(self.machine_id)
        droplet.destroy()
        self.decommissioned = True

    def __str__(self):
        return f'{self.url} - {self.ip_address}'


class IdeFactory(models.Model):
    STACK_CHOICES = (
        ('node-js', 'NodeJS'),
        ('python', 'Python'),
        ('android', 'Android'),
        ('angular', 'Angular'),
        ('php', 'PHP'),
    )
    stack = models.CharField(max_length=140, default='node-js', choices=STACK_CHOICES)
    workspace_config = JSONField(default=dict)

    def __str__(self):
        return f'{self.stack} factory'


class CandidateSetup(models.Model):
    # TODO: make this a foreign key to candidate project
    project = models.ForeignKey(CandidateProjects, on_delete=models.CASCADE, null=True, blank=True)
    project_name = models.CharField(max_length=140, blank=True)
    setup_code = models.CharField(max_length=140, blank=True, unique=True)
    #  make this a foreign key
    candidate_id = models.CharField(max_length=140, blank=True)
    workspace_data = JSONField(default=dict, blank=True)
    workspace_url = models.URLField(blank=True)
    report = JSONField(default=dict, blank=True)
    server_created = models.BooleanField(default=False)
    domain_created = models.BooleanField(default=False)
    workspace_created = models.BooleanField(default=False)
    candidate_notified = models.BooleanField(default=False)
    project_completed = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    formatted_report = JSONField(default=dict, blank=True)

    # create a field track if candidate has started project

    def set_end_time(self):
        self.end_time = self.start_time + self.project.transaction.project.duration

    def set_report(self):
        my_report = {}
        if self.report != 'null':
            for metric_list in self.report['component']['measures']:
                if metric_list['metric'] == 'quality_gate_details':
                    new_value = json.loads(metric_list['value'])
                    my_report[metric_list['metric']] = new_value['level']
                else:
                    my_report[metric_list['metric']] = metric_list['value']
        self.formatted_report = my_report

    def save(self, *args, **kwargs):
        self.set_end_time()
        super(CandidateSetup, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.candidate.first_name}+{self.project.candidate.last_name}- {self.project_name} - {self.start_time} - {self.end_time}'


class Job(models.Model):
    TYPE_CHOICES = (
        ('create_server', 'Create server'),
        ('create_workspace', 'Create Workspace'),
        ('send_mail', 'Send Mail'),
        ('monitor_workspace', 'Monitor Workspace'),
        ('start_analysis', 'Start Analysis'),
        ('transfer_files', 'Transfer Files'),
        ('get_analysis', 'Get Analysis'),
        ('clean_up', 'Clean Up'),
    )
    # my_data = {
    #     'project_id': project_id,
    #     'project_name': project.transaction.project.name,
    #     'candidate_id': request.user.id,
    #     'server_type': 'ide_server_config',
    #     'setup_code': str(uuid.uuid4())
    # }
    type = models.CharField(max_length=140, default='create_server', choices=TYPE_CHOICES, null=True, blank=True)
    project = models.ForeignKey(CandidateProjects, on_delete=models.CASCADE, null=True, blank=True)
    has_executed = models.BooleanField(default=False)
    time = models.DateTimeField(null=True, blank=True)
    # data = JSONField()
    setup_code = models.UUIDField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - {self.created}'

    # Enterprise models


# class EnterpriseCandidateSetup(models.Model):
#     # TODO: make this a foreign key to candidate project
#     project = models.ForeignKey(EnterpriseCandidateProjects, on_delete=models.CASCADE, null=True, blank=True)
#     project_name = models.CharField(max_length=140, blank=True)
#     setup_code = models.CharField(max_length=140, blank=True, unique=True)
#     #  make this a foreign key
#     workspace_data = JSONField(default=dict, blank=True)
#     workspace_url = models.URLField(blank=True)
#     report = JSONField(default=dict, blank=True)
#     candidate_notified = models.BooleanField(default=False)
#     project_completed = models.BooleanField(default=False)
#     start_time = models.DateTimeField(blank=True, null=True)
#     end_time = models.DateTimeField(blank=True, null=True)
#
#     # create a field track if candidate has started project
#
#     def set_end_time(self):
#         self.end_time = self.start_time + self.project.enterprise_project.project.duration
#
#     def save(self, *args, **kwargs):
#         self.set_end_time()
#         super(EnterpriseCandidateSetup, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return f'{self.project.enterprise_candidate.candidate.username}-{self.project_name} - {self.start_time} - {self.end_time}'


# class EnterpriseJob(models.Model):
#     TYPE_CHOICES = (
#         ('create_server', 'Create server'),
#         ('create_workspace', 'Create Workspace'),
#         ('send_mail', 'Send Mail'),
#         ('monitor_workspace', 'Monitor Workspace'),
#         ('start_analysis', 'Start Analysis'),
#         ('transfer_files', 'Transfer Files'),
#         ('get_analysis', 'Get Analysis'),
#         ('clean_up', 'Clean Up'),
#     )
#     project = models.ForeignKey(EnterpriseCandidateProjects, on_delete=models.CASCADE, null=True, blank=True)
#     has_executed = models.BooleanField(default=False)
#     time = models.DateTimeField(null=True, blank=True)
#     type = models.CharField(max_length=140, default='create_server', choices=TYPE_CHOICES)
#     data = JSONField(default="null", blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.type} - {self.created}'


# class EnterpriseReport(models.Model):
#     enterprise_candidate = models.ForeignKey(EnterpriseCandidateSetup, on_delete=models.CASCADE, blank=True)
#     #     classes = models.
#     #     comment_lines
#     #     directories
#     #     files
#     #     ncloc
#     #     functions
#     violations = models.CharField(max_length=140, blank=True)
#     code_smells = models.CharField(max_length=140, blank=True)
#     sqale_rating = models.CharField(max_length=140, blank=True)
#     #     coverage
#     #     complexity
#     #     cognitive_complexity
#     duplicated_blocks = models.CharField(max_length=140, blank=True)
#     duplicated_lines = models.CharField(max_length=140, blank=True)
#     duplicated_files = models.CharField(max_length=140, blank=True)
#     #     duplicated_lines_density
#     sqale_index = models.CharField(max_length=140, blank=True)
#     vulnerabilities = models.CharField(max_length=140, blank=True)
#     alert_status = models.CharField(max_length=140, blank=True)
#     quality_gate_details = models.CharField(max_length=140, blank=True)
#     bugs = models.CharField(max_length=140, blank=True)
#     security_rating = models.CharField(max_length=140, blank=True)
#     tests
#     test_failures
#     test_errors
#     class_complexity
