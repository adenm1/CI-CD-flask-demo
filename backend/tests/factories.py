"""Test data factories using factory_boy."""
import factory
from factory import Faker
from backend.api.models import AdminUser, Pipeline
from backend.utils.passwords import hash_password


class AdminUserFactory(factory.Factory):
    """Factory for creating AdminUser test instances."""

    class Meta:
        model = AdminUser

    username = factory.Faker('user_name')
    password_hash = factory.LazyFunction(lambda: hash_password('password123'))
    role = 'admin'
    is_active = True
    totp_secret = None


class PipelineFactory(factory.Factory):
    """Factory for creating Pipeline test instances."""

    class Meta:
        model = Pipeline

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    status = 'success'
    owner = factory.Faker('user_name')
    branch = 'main'
    commit_sha = factory.Faker('sha256')
    commit_message = factory.Faker('sentence')
