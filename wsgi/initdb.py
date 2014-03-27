from main import *
from models import *
def dbinit():
    db.drop_all()
    db.create_all()

    user = Users(username='ekowibowo', fullname='Eko Suprapto Wibowo', password=hash_string('rahasia'),
                         email='swdev.bali@gmail.com',
                         tagline='A cool coder and an even cooler Capoeirista',
                         bio = 'I love Python very much!',
                         avatar = '/static/avatar.png',
                         active = True)
    user.portfolio.append(Portfolio(title = 'FikrPOS',
                                    description = 'An integrated POS solution using cloud concept',
                                    tags='python,c#,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    user.portfolio.append(Portfolio(title = 'Bio Application',
                                    description = 'An autobiography publisher',
                                    tags='python,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    user.portfolio.append(Portfolio(title = 'Project Management',
                                    description = 'Internal company project management tool',
                                    tags='extjs,python,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    dbinit()