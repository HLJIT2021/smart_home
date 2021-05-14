



class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'user'

    def __str__(self):
        return self.username


class UserInfo(models.Model):
    uid = models.OneToOneField(User, models.CASCADE, db_column='uid')
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)

    class Meta:
        managed = True
        db_table = 'user_info'


class UserAppRelation(models.Model):
    app_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, models.CASCADE, db_column='uid')
    app_name = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, blank=True, null=True)


class Meta:
    managed = True
    db_table = 'user_userapprelation'


class Type(models.Model):
    tid = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'type'


class AppRelation(models.Model):
    sid = models.AutoField(primary_key=True)
    app = models.ForeignKey('UserAppRelation', models.CASCADE, db_column='app_id')
    sno = models.CharField(max_length=50)
    tid = models.ForeignKey('Type', models.CASCADE, db_column='tid')
    kind = models.CharField(max_length=4)
    port = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'app_relation'


class Data(models.Model):
    sid = models.ForeignKey(AppRelation, models.CASCADE, db_column='sid')
    value = models.FloatField()
    dt = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'data'


class AppControl(models.Model):
    ssid = models.ForeignKey('AppRelation', models.CASCADE, db_column='ssid')
    dsid = models.ForeignKey('AppRelation', related_name='AppRelation1', on_delete=models.CASCADE, db_column='dsid')
    used = models.CharField(max_length=3)
    threshold_low = models.FloatField(blank=True, null=True)
    threshold_high = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'app_control'



class ControlState(models.Model):
    sid = models.OneToOneField(AppRelation, models.CASCADE, db_column='sid', primary_key=True)
    state = models.CharField(max_length=1, blank=True, null=True)


class Meta:
    managed = True
    db_table = 'control_state'
