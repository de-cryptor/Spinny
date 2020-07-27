from datetime import  datetime

def save_area_volume(sender,instance,created,**kwargs):
    try:
        if created:
            model_created = instance.__class__.__name__
            instance.area = instance.get_area()
            instance.volume = instance.get_volume()
            instance.updated_on = datetime.now()
            instance.save()
    except Exception as E:
        pass