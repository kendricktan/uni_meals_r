# Generates file path for image upload

def generate_directory_user(self, filename):
    id = self.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "user/%s/%s" % (str(id), filename)
    return url

def generate_directory_eatery(self, filename):
    id = self.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "eatery/%s/%s" % (str(id), filename)
    return url    
    
def generate_directory_food(self, filename):
    id = self.eatery.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "eatery/%s/food/%s" % (str(id), filename)
    return url
    
def generate_directory_specials(self, filename):
    id = self.eatery.id
    if id == None:
        id = max(map(lambda a:a.id,Theme.objects.all())) + 1    
    url = "eatery/%s/specials/%s" % (str(id), filename)
    return url