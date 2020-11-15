from genealogical_tree.app.models import PersonModel
from sqlalchemy.orm import Session
from genealogical_tree.app.db import db_session


@db_session(commit=False)
def main(session: Session):
    persons = session.query(PersonModel).order_by(PersonModel.columns.parent_id).all()
    res = {}
    for person in persons:

        a = 1
        # if person.parent_id:
        #     a = session.query(PersonModel).filter(PersonModel.columns.family_id == person.parent_id).all()
        #     person['parent'] = a
    print(f'Hi, ')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

