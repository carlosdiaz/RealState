from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import join
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:////tmp/propertyRS.db")
Base = declarative_base()
Base.metadata.reflect(engine)



class User(Base):
    __table__ = Base.metadata.tables['user']

class Property(Base):
    __table__ = Base.metadata.tables['property']

class Image(Base):
	__table__ = Base.metadata.tables['image']


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    #for prop in db_session.query(Property).join(Image).filter((Property.typeprop == 'Casa').order_by(Property.id.asc()).limit(1)):
    #	print prop.__dict__
    #for prop in db_session.query(Property).join(Image.property_id, Property.id == Image.property_id):
    #	print prop.__dict__


#    for item in db_session.query(User.id, User.email):
#        print item
#	seq = db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).order_by(Property.id.asc()).limit(4)

    #for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).order_by(Property.id.asc()).limit(4):
    propertyRecords = []
    propertyDict = {}
    for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).order_by(Property.id.desc()).limit(4):
        #print prop
        #print prop[0]
        #print prop[1]
        print "***********************************+"
        propertyDict = dict(id=prop[0], price=prop[1], type=prop[2], contract=prop[3] , location=prop[4], description=prop[5], imagetodisplay=prop[6], area=prop[7], bathrooms=prop[8], bedrooms=prop[9])
        
    	propertyRecords.append(propertyDict) 
    	print propertyDict
    	#print propertyRecords
    x = 1

    print propertyRecords

        #propertyRecords = [dict(id=prop[0], price=prop[1], type=prop[2], contract=prop[3] , location=prop[4], description=prop[5], imagetodisplay=prop[6], area=prop[7], bathrooms=prop[8], bedrooms=prop[9])    
#propertyRecords = [dict(id=row[0], price=row[1], type=row[2], contract=row[3] , location=row[4], description=row[5], imagetodisplay=row[6], area=row[7], bathrooms=row[8], bedrooms=row[9])  for prop in db_session.query(Property.id, Property.price, Property.typeprop,Property.contract, Property.location, Property.description, Image.path, Property.area, Property.bathrooms, Property.bedrooms).join(Image).order_by(Property.id.asc()).limit(4):
#select property.id, price, typeprop, contract, location, description, image.path, area, bathrooms , bedrooms from property inner join image on property.id = image.property_id order by property.id desc limit 4

#    for prop in db_session.query(Property).filter(Property.typeprop == 'Casa').order_by(Property.id.asc()):
#    	print prop.__dict__
#    for prop in db_session.query(Property.description).join(Image).filter(Property.typeprop == 'Casa').order_by(Property.id.asc()).limit(1):
		#print prop.__dict__ 
#		print prop