import contextlib
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, Query, scoped_session
import sqlalchemy.orm.exc

from genealogical_tree.app.config import config


class QueryForWeb(Query):
    def get_or_404(self, ident):
        """Return an instance based on the given primary key identifier,
                or raise rti_utils.errors.NotFoundError"""
        instance = self.get(ident)

        if not instance:
            raise print(f'object with id: {ident} not found')

        return instance

    def one_or_404(self):
        try:
            return self.one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise print('object not found')


engine = create_engine(
    config.DB_URL,
    pool_pre_ping=True,
    pool_recycle=60,
    echo=False,
    connect_args={"options": "-c timezone=utc"},
)

OurSession = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    query_cls=QueryForWeb,
)

ScopedSession = scoped_session(OurSession)

@contextlib.contextmanager
def session_scope(commit=True):
    session: Session = ScopedSession()

    try:
        yield session

        if commit:
            session.commit()
    except Exception as ex:
        session.rollback()

        raise ex
    finally:
        session.close()


def db_session(f=None, commit=True):
    """Альтернатива session_scope, для декорирования фнкции и автоматическим пробросом сессии в аргументы
        и последующим коммитом

    >>> @db_session
    >>> def update_entity(entity_id, session: Session):
    >>>     entity = session.query(Entity).filter_by(id=entity_id)
    >>>     entity.value = 'new-value'
    >>>     session.add(entity)
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if 'session' not in kwargs and all(not isinstance(arg, Session) for arg in args):
                with session_scope(commit=commit) as session:
                    return f(*args, session=session, **kwargs)
            else:
                return f(*args, **kwargs)

        return wrapper

    return decorator(f) if f is not None else decorator
