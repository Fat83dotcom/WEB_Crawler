from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from bd_connection import SitesData
from sqlalchemy import select
import os


class DBManager:
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_name = os.getenv('POSTGRES_DB')
    con_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(con_str, echo=True,  client_encoding='utf8')

    def insert_data(self, data: list):
        session_data = [
            SitesData(
                name_site=row[0],
                search_url=row[1],
                search_result_selector=row[2],
                title_selector=row[3],
                content_selector=row[4],
                topic=row[5],
                n_link=row[6],
                link_complement=row[7],
                is_absolute_url=row[8],
                url_pattern=row[9],
            ) for row in data
        ]
        try:
            with Session(self.engine) as session:

                session.add_all(session_data)

                session.commit()
        except Exception as e:
            raise e

    def select_data(self):
        with Session(self.engine) as session:
            result = session.query(SitesData).all()
        return result


if __name__ == '__main__':
    sites = [
        [
            'BBC',
            'https://www.bbc.com/portuguese/topics/c404v027pd4t',
            'li.bbc-t44f9r a',
            'h1.bbc-14gqcmb',
            'div.bbc-1cvxiy9',
            '',
            2,
            '',
            True,
            ''
        ],
        [
            'CNN',
            'https://www.cnnbrasil.com.br/?s=',
            'li.home__list__item a',
            'h1.post__title',
            'div.post__content',
            'marketing+digital',
            2,
            '',
            True,
            ''
        ],
        [
            'TECHTUDO',
            'https://www.techtudo.com.br/busca/?q=',
            'div.widget--info__text-container a',
            'div.title',
            'div.content-text p.content-text__container',
            'tecnologia',
            2,
            'https:',
            False,
            r"u=([^&]+)"
        ],
        [
            'G1',
            'https://g1.globo.com/busca/?q=',
            'div.widget--info__text-container a',
            'div.title h1.content-head__title',
            'div.content-text p.content-text__container',
            'tecnologia',
            2,
            'https:',
            False,
            r"u=([^&]+)"
        ],
        [
            'Economic News',
            'https://economicnewsbrasil.com.br/?s=',
            'article.jeg_post.jeg_pl_lg_2 a',
            'div.elementor-widget-container h1.elementor-heading-title',
            'div.elementor-element.elementor-element-c3e1609',
            'economia',
            2,
            '',
            True,
            ''
        ]
    ]

    db = DBManager()
    # ins = db.insert_data(sites)
    sel = db.select_data()
    print(len(sel))
    for p in sel:
        print(p.name_site)
        print(p.search_url)
        print(p.search_result_selector)
