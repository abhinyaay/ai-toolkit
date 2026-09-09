"""Inspect real Security.framework ACLs without reading or writing Keychain items."""

from __future__ import annotations

import ctypes
import sys
from ctypes import byref, c_long, c_uint32, c_ulong, c_void_p

import pytest

pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="Security.framework")


@pytest.fixture
def darwin():
    from pipefy_auth import wrapping_key_darwin

    return wrapping_key_darwin


def _bind(library, name, arguments, result):
    function = getattr(library, name)
    function.argtypes = arguments
    function.restype = result
    return function


def test_allow_all_access_trusts_all_readers_but_preserves_acl_owner(darwin):
    pointer = ctypes.POINTER(c_void_p)
    copy_matching = _bind(
        darwin._sec, "SecAccessCopyMatchingACLList", [c_void_p, c_void_p], c_void_p
    )
    copy_contents = _bind(
        darwin._sec,
        "SecACLCopyContents",
        [c_void_p, pointer, pointer, ctypes.POINTER(c_uint32)],
        ctypes.c_int32,
    )
    count = _bind(darwin._found, "CFArrayGetCount", [c_void_p], c_long)
    get = _bind(darwin._found, "CFArrayGetValueAtIndex", [c_void_p, c_long], c_void_p)
    release = _bind(darwin._found, "CFRelease", [c_void_p], None)
    access = darwin._allow_all_access()
    try:
        for authorization in (
            "kSecACLAuthorizationDecrypt",
            "kSecACLAuthorizationChangeACL",
        ):
            acls = copy_matching(access, darwin._k(authorization))
            try:
                assert count(acls) > 0
                for index in range(count(acls)):
                    apps, description, prompt = c_void_p(), c_void_p(), c_uint32()
                    assert (
                        copy_contents(
                            get(acls, index),
                            byref(apps),
                            byref(description),
                            byref(prompt),
                        )
                        == 0
                    )
                    try:
                        if authorization == "kSecACLAuthorizationDecrypt":
                            assert apps.value is None, (
                                "decrypt must trust every application"
                            )
                            assert prompt.value == 0
                        else:
                            assert apps.value is not None
                            assert count(apps) == 0, (
                                "changing the ACL must still require consent"
                            )
                    finally:
                        if apps:
                            release(apps)
                        if description:
                            release(description)
            finally:
                release(acls)
    finally:
        release(access)


@pytest.mark.parametrize("value", [True, False])
def test_cf_boolean_uses_boolean_type_required_by_security_queries(darwin, value):
    get_type = _bind(darwin._found, "CFGetTypeID", [c_void_p], c_ulong)
    boolean_type = _bind(darwin._found, "CFBooleanGetTypeID", [], c_ulong)
    release = _bind(darwin._found, "CFRelease", [c_void_p], None)
    converted = darwin._cf(value)
    try:
        assert get_type(converted) == boolean_type()
    finally:
        release(converted)
