import os
import json
from random import randint
from faker import Faker
from jobplus.models import db,User,Job,CompanyDetail


fake = Faker('zh-cn')

with open(os.path.join(os.path.dirname(__file__),'datas/company.json')) as f:
    data_company = json.load(f)

with open(os.path.join(os.path.dirname(__file__),'datas/job.json')) as f:
    data_job = json.load(f)

def iter_user():
    for i in data_company:
        yield User(
            name=i['name'],
            email=fake.email(),
            password=fake.password(),
            role = User.ROLE_COMPANY
        )
l = list(iter_user())
print(l)

def iter_companydetail():
    for u,d in zip(l,data_company):
        yield CompanyDetail(
            user = u,
            image_url = d['image_url'],
            finance = d['finance'],
            staff_num = d['staff_num'],
            type = d['type'],
            about = d['about']
        )


def iter_job():
    for i, u in enumerate(l):
        n = randint(2, 5)
        while n > 0:
            d = data_job[n + i * 5 - 1]
            yield Job(
                user=u,
                name=d['name'],
                salary=d['salary'],
                location=d['location'],
                experience_requirement=d['experience_requirement'],
                degree_requirement=d['degree_requirement'],
                tags=d['tags'],
                release_time=d['release_time']
            )
            n -= 1



def run():
    for user in l:
        db.session.add(user)

    for job in iter_job():
        db.session.add(job)

    for company_detail in iter_companydetail():
        db.session.add(company_detail)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
