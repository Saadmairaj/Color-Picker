from setuptools import setup, find_packages
import meta

setup(
    name=meta.__title__,
    version=meta.__version__,
    description=meta.__description__,
    # long_description=long_description,
    url=meta.__url__,
    author=meta.__author__,
    author_email=meta.__author_email__,
    license=meta.__license__,
    copyright=meta.__copyright__,
    platform= meta.__platform__,
    # ...
    py_modules=['Kivy Color ids', 'meta'],
 )