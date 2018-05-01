from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.

class Profile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	phone = models.CharField(max_length=20,null=True)
	location = models.CharField(max_length=200, null=True)

	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)


class Item(models.Model):

	status_choices = (
			('rent','Rent'),
			('give', 'Give'),
			('share','Share'),
		)
	item_types = (
			('book','Book'),
			('movie','Movie',),
			('data','Data'),
			('other','Other'),
		)
	title = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, blank=True,unique=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL)
	cover = models.ImageField(upload_to='items/%Y/%m/%d',blank=True)
	link  = models.URLField(blank=True)
	description = models.TextField(max_length=500, blank=True)
	status = models.CharField(max_length=10,choices=status_choices,default='Share')
	item = models.CharField(max_length=10, choices=item_types,default='Data', verbose_name='Item Type')
	publish = models.DateTimeField(auto_now=True,null=True)

	class Meta:
		ordering = ('-publish',)
		index_together = (('id', 'slug'),)

	def __str__(self):
		return '{} : <{}> for {}'.format(self.title,self.item,self.status)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Item, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('item_edit', kwargs={'slug':self.slug})
