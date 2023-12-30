from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy import create_engine , String , Column  , Integer , Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session

D = 'sqlite:///./pizza.db'
e = create_engine(D,connect_args={"check_same_thread":False})
l = sessionmaker(autocommit=False, autoflush=False, bind=e)
B = declarative_base()

class p(B):
    __tablename__ = "p"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, index=True)
    pizza_name = Column(String, unique=True, index=True)
    pizza_dis = Column(String, index=True)
    pizza_price = Column(Integer , index= True)


B.metadata.create_all(bind = e)

app = FastAPI()


def get_db():
    db = l()
    try:
        yield db
    finally:
        db.close()



@app.post('/u/')
def u(pizza_name : str , pizza_dis : str , pizza_price : int , db:  Session = Depends(get_db)):
    try:
        new_user = p(pizza_name = pizza_name  , pizza_dis = pizza_dis  , pizza_price = pizza_price)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500 , detail=str(e))
    

@app.get('/d/{item_id}')
def d(item_id : int , db :  Session = Depends(get_db)):
    try:
        n = db.query(p).filter(p.id == item_id ).first()
        if n is None:
            raise HTTPException(status_code=404,detail="no pizza")
        
        return n
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))


@app.delete('/del/{item_id}')
def dell(item_id : int , db : Session = Depends(get_db)):
    try:
        n = db.query(p).filter(p.id == item_id).first()
        if n is None:
            raise HTTPException(status_code=404, detail="no pizza avalible to sell")
        
        db.delete(n)
        db.commit()
        return n
    except Exception as e:
        raise HTTPException(status_code=500 , detail=(get_db))  