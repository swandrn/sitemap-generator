import os
import sys
sys.path.append(os.getcwd())
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.sql.expression import func

db = SQLAlchemy()

class LandingPages(db.Model):
    __tablename__ = 'landing_pages'
    page_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_url = db.Column(db.String(1000), nullable=False)
    domain_name = db.Column(db.String(60), nullable=False)
    last_scraped = db.Column(db.Integer, nullable=False)

    pages_of_domain = db.relationship('PagesOfDomain', back_populates='landing_pages')

class PagesOfDomain(db.Model):
    __tablename__ = 'pages_of_domain'
    page_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    landing_page_id = db.Column(db.Integer, db.ForeignKey(LandingPages.page_id), nullable=False)
    page_url = db.Column(db.String(1000), nullable=False)
    parent_url = db.Column(db.String(1000), nullable=True)

    landing_pages = db.relationship('LandingPages', back_populates='pages_of_domain', lazy='joined')

def insert_landing_page(session, homepage_url: str, domain: str, last_scraped: int):
    lp = LandingPages()
    lp.page_url = homepage_url
    lp.domain_name = domain
    lp.last_scraped = last_scraped
    session.add(lp)
    session.commit()

def get_landing_page_id(session, url: str) -> int | None:
    query = session.query(func.max(LandingPages.page_id)).filter_by(page_url=url)
    landing_page_id = session.execute(query).scalar_one_or_none()
    return landing_page_id

def insert_pages_of_domain(session, sitemap: dict) -> None:
    objects = []
    landing_page_id = get_landing_page_id(session=session, url=list(sitemap)[0])
    for k, v in sitemap.items():
        pod = PagesOfDomain()
        pod.landing_page_id = landing_page_id
        pod.page_url = k
        pod.parent_url = v
        objects.append(pod)
    session.add_all(objects)
    session.commit()

def get_latest_timestamp(session, url: str) -> int | None:
    landing_page_id = get_landing_page_id(session=session, url=url)
    if not landing_page_id:
        return None
    query = session.query(LandingPages.last_scraped).filter_by(page_id=landing_page_id)
    last_scraped = session.execute(query).scalar_one_or_none()
    return last_scraped
        
def get_sitemap(session, homepage_url: str) -> dict | None:
    landing_page_id = get_landing_page_id(session=session, url=homepage_url)
    query = select(PagesOfDomain.page_url, PagesOfDomain.parent_url).join(LandingPages).where(LandingPages.page_id == landing_page_id)
    sitemap_as_tuple = session.execute(query).all()
    sitemap_as_dict = dict((k, v) for k, v in sitemap_as_tuple)
    return sitemap_as_dict