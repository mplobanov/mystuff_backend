from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=256)
    loc_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return "Loaction {} by {}".format(self.name, self.loc_owner.username)


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statuses"

    name = models.CharField(max_length=256)
    st_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='statuses')

    def __str__(self):
        return "Status {} by {}".format(self.name, self.st_owner.username)


class Group(models.Model):
    name = models.CharField(max_length=256)
    gr_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stuff_groups')

    def __str__(self):
        return "Group {} by {}".format(self.name, self.gr_owner.username)


class Item(models.Model):
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256, blank=True)
    color = models.CharField(max_length=256, blank=True)
    size = models.CharField(max_length=64, blank=True)
    volume = models.CharField(max_length=64, blank=True)

    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='items')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='items')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='items')

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        ans = []
        if self.group:
            ans.append("[{}]".format(self.group.name))
        if self.color:
            ans.append(self.color)
        ans.append(self.name)
        if self.brand:
            ans.append(self.brand)
        if self.size:
            ans.append(self.size)
        if self.volume:
            ans.append(self.volume)
        ans.append("({})".format(self.status.name))
        ans.append("- {}".format(self.location.name))
        ans.append(" by {}".format(self.owner.username))
        return " ".join(ans)


