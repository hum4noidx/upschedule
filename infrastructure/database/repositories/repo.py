class SQLAlchemyRepo:
    """Db abstraction layer"""

    def __init__(self, session):
        self.session = session
