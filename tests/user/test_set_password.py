import pytest
from pysyncgateway.exceptions import InvalidPassword


def test(user):
    result = user.set_password('__PASSWORD__')

    assert result is None
    assert user.password == '__PASSWORD__'


# --- FAILURES ---


@pytest.mark.parametrize('password', ['', None, 1])
def test_empty(user, password):
    with pytest.raises(InvalidPassword) as excinfo:
        user.set_password(password)

    assert '"{}"'.format(password) in excinfo.value.args[0]
