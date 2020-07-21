import os
import pytest

from tests.support.configure_test import app
from application import db

import application.models.item as item
from config import TestingConfig


def test_db_create(app):
    app = app(TestingConfig)

    test_model_to_insert = item.Item(
        description="Vintage wood rocking chair",
        donor="Demo McDemoFace",
        price=40.00,
        status="For Sale",
        title="Rocking Chair",
        category="Big Cat Rescue",
        image="img.ul"
    )
    test_model_to_insert.save()
    db.session.commit()

    assert db.session.query(item.Item).one()
