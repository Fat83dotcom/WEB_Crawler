from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import os


db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT', '5432')
db_name = os.getenv('POSTGRES_DB')


class Base(DeclarativeBase):
    ...


class SitesData(Base):
    __tablename__ = 'sites'

    site_id: Mapped[int] = mapped_column(primary_key=True)
    name_site: Mapped[str] = mapped_column(String(255))
    search_url: Mapped[str] = mapped_column(String(255))
    search_result_selector: Mapped[str] = mapped_column(String(255))
    title_selector: Mapped[str] = mapped_column(String(255))
    content_selector: Mapped[str] = mapped_column(String(255))
    topic: Mapped[str] = mapped_column(String(100))
    n_link: Mapped[int] = mapped_column()
    link_complement: Mapped[str] = mapped_column(String(255))
    is_absolute_url: Mapped[bool] = mapped_column()
    url_pattern: Mapped[str] = mapped_column(String(255))

    def __iter__(self):
        return (
            i for i in (
                self.site_id,
                self.name_site,
                self.search_url,
                self.search_result_selector,
                self.title_selector,
                self.topic,
                self.n_link,
                self.link_complement,
                self.is_absolute_url,
                self.url_pattern
            )
        )


if __name__ == '__main__':
    con_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(con_str, echo=True,  client_encoding='utf8')
    Base.metadata.create_all(engine)
