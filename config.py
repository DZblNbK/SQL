from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        asynstr = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        #print(asynstr)
        return asynstr
    
    @property
    def DATABASE_URL_psycopg(self):
        psystr = f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        #print(psystr)
        return psystr

    model_config = SettingsConfigDict(env_file=".env")
    

settings = Settings()
#print(settings.DB_PASS)