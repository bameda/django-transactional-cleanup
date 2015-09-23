import pytest

from django.db import models

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


from django_transactional_cleanup import service

from .models import TestModel1, TestModel2


def test_models_with_filefield():
    models.get_models = Mock(return_value=[TestModel1, TestModel2])
    assert service._find_models_with_filefield() == [TestModel1]


@pytest.mark.django_db
def test_remove_files_on_change_same_file():
    test_obj = TestModel1()
    test_obj.test_file = "test_filename"
    test_obj.save()

    with patch('django_transactional_cleanup.service._delete_file') as mock:
        service.remove_files_on_change(TestModel1, test_obj)
        assert not mock.called


@pytest.mark.django_db
def test_remove_files_on_change_different_file():
    test_obj = TestModel1()
    test_obj.test_file = "test_filename1"
    test_obj.save()
    test_obj.test_file.storage = Mock()
    test_obj.test_file.storage.exists.return_value = True

    test_obj.test_file = Mock()
    test_obj.test_file.name = "test_filename2"

    with patch('django_transactional_cleanup.service._delete_file') as mock:
        service.remove_files_on_change(TestModel1, test_obj)
        assert mock.called


def test_remove_files_on_delete():
    test_obj = TestModel1()
    test_obj.test_file = Mock()
    test_obj.test_file.name = "test_filename"

    test_obj.test_file.storage = Mock()
    test_obj.test_file.storage.exists.return_value = True

    with patch('django_transactional_cleanup.service._delete_file') as mock:
        service.remove_files_on_delete(TestModel1, test_obj)
        assert mock.called


def test_custom_pre_delete_signals():
    test_obj = TestModel1()
    test_obj.test_file = Mock()
    test_obj.test_file.name = "test_filename"

    test_obj.test_file.storage = Mock()
    test_obj.test_file.storage.exists.return_value = True

    with patch('django_transactional_cleanup.signals.cleanup_pre_delete.send') as mock:
        service.remove_files_on_delete(TestModel1, test_obj)
        assert mock.called


def test_custom_post_delete_signals():
    test_obj = TestModel1()
    test_obj.test_file = Mock()
    test_obj.test_file.name = "test_filename"

    test_obj.test_file.storage = Mock()
    test_obj.test_file.storage.exists.return_value = True

    with patch('django_transactional_cleanup.signals.cleanup_post_delete.send') as mock:
        service.remove_files_on_delete(TestModel1, test_obj)
        assert mock.called
