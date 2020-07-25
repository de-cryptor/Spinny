from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAuthentication(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.user.username + self.auth_token)


class Box(models.Model):
    '''
    Domensions of the box.
    Assuming the dimension having floating point values
    Assumed dimmesion having max value of 100,000 with a resolution of 2 decimal places
    '''

    length = models.IntegerField(help_text="Length of Box",default=0)
    width = models.IntegerField(help_text="Width of Box",default=0)
    height = models.IntegerField(help_text="Height of Box",default=0)
    area = models.IntegerField(help_text="Area of Box",default=0)
    volume = models.IntegerField(help_text="Volume of Box",default=0)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,help_text="User Created")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def get_area(self):

        return 2*( (self.length * self.width) + (self.length * self.height) + (self.width * self.height) )

    def get_volume(self):

        return (self.length * self.width * self.height)

    def custom_serializer(self):
        data = dict()
        data['id'] = self.id
        data['length'] = str(self.length)
        data['width'] = str(self.width)
        data['height'] = str(self.height)
        data['area'] = str(self.area)
        data['volume'] = str(self.volume)
        data['created_by'] = self.created_by.username
        data['updated_on'] = self.created_on

        return data


    




