from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker



from .config import settings



class DataBaseHelper:
    
    def __init__(self, url : str, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        
        self.AsyncSession = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autocommit=False,
        )
        
    async def get_db(self):
        async with self.AsyncSession() as session:
            yield session

db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.echo,
)